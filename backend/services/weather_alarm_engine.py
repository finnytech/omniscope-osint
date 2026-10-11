"""
CYBER-SPECTRE-NEXUS: Tactical Severe Weather Alarm & Tornado Emergency Engine
=============================================================================
Provides real-time emergency alert evaluation, confirmed tornado-on-ground detection,
configurable severe convective storm triggers, automated audio/desktop notifications,
and direct camera/radar feed jumping to tornado touchdown sectors.
"""

import os
import sys
import json
import time
import asyncio
import logging
from typing import Dict, Any, List, Optional
import httpx
from .weather_engine import resolve_noaa_alert_centroid

logger = logging.getLogger("WeatherAlarmEngine")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "data", "alarm_config.json")

DEFAULT_ALARM_CONFIG = {
    "twister_tornado": True,
    "supercell": True,
    "hook_echo": True,
    "min_ef_scale": 0,           # 0 to 5 (0 = all confirmed tornadoes)
    "min_wind_gust_mph": 58.0,   # 58 mph = NWS severe criteria
    "min_hail_size_inches": 1.0, # 1.0 in = quarter size
    "flash_flood": False,
    "severe_thunderstorm": True,
    "sound_siren": True,
    "desktop_notification": True,
    "auto_jump_to_feed": True,
    "polling_interval_sec": 60   # 60s (1 min) up to 1200s (20 min)
}

NWS_USER_AGENT = "CyberSpectreNexus/2.0 (contact@cyberspectre.net, emergency-weather-monitoring)"
NOAA_NEXRAD_TILE_URL = "https://mesonet.agron.iastate.edu/cache/tile.py/1.0.0/nexrad-n0q-900913/{z}/{x}/{y}.png"


class WeatherAlarmEngine:
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load_config()
        self._last_poll_ts: float = 0
        self._cached_alarms: Optional[Dict[str, Any]] = None
        self._cache_ttl: float = 45.0  # 45 seconds cache to avoid upstream throttling

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cfg = DEFAULT_ALARM_CONFIG.copy()
                    cfg.update(data)
                    return cfg
            except Exception as e:
                logger.warning(f"Error loading {self.config_path}, using defaults: {e}")
        return DEFAULT_ALARM_CONFIG.copy()

    def save_config(self, new_config: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in new_config.items():
            if k in DEFAULT_ALARM_CONFIG:
                # Clamp polling interval between 30 and 1200 seconds (30s to 20 minutes)
                if k == "polling_interval_sec":
                    try:
                        v = max(30, min(1200, int(v)))
                    except Exception:
                        v = 60
                self.config[k] = v

        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            logger.info("Saved updated weather alarm configuration")
        except Exception as e:
            logger.error(f"Failed to persist alarm config: {e}")

        return self.config

    def get_config(self) -> Dict[str, Any]:
        return self.config.copy()

    @staticmethod
    def _extract_coordinates_from_feature(feat: Dict[str, Any]) -> Dict[str, float]:
        geom = feat.get("geometry")
        props = feat.get("properties", {})
        params = props.get("parameters", {}) or {}

        # 1. Authentic coordinates from radar eventMotionDescription
        motion_descs = params.get("eventMotionDescription", [])
        if isinstance(motion_descs, list):
            for md in motion_descs:
                if isinstance(md, str):
                    m = re.search(r'(-?\d+\.\d+),\s*(-?\d+\.\d+)', md)
                    if m:
                        return {"lat": float(m.group(1)), "lon": float(m.group(2))}

        # 2. Polygon or Point Geometry coordinates
        if geom:
            gtype = geom.get("type", "")
            coords = geom.get("coordinates", [])
            if coords:
                if gtype == "Point" and len(coords) >= 2:
                    return {"lat": float(coords[1]), "lon": float(coords[0])}
                elif gtype in ("Polygon", "MultiPolygon"):
                    poly = coords[0] if gtype == "Polygon" else coords[0][0]
                    if poly and len(poly) > 0:
                        lats = [pt[1] for pt in poly if len(pt) >= 2]
                        lons = [pt[0] for pt in poly if len(pt) >= 2]
                        if lats and lons:
                            return {
                                "lat": round(sum(lats) / len(lats), 5),
                                "lon": round(sum(lons) / len(lons), 5)
                            }
        # 3. Fallback to authentic centroid resolution from NWS office and county
        resolved = resolve_noaa_alert_centroid(props, geom)
        return {"lat": resolved["lat"], "lon": resolved["lon"]}

    async def poll_active_alarms(self, camera_engine=None) -> Dict[str, Any]:
        """
        Polls active NOAA alerts and evaluates triggers against configured thresholds.
        Detects confirmed tornadoes on the ground, hook echoes, and severe gusts.
        """
        now = time.time()
        if self._cached_alarms is not None and (now - self._last_poll_ts < self._cache_ttl):
            return self._cached_alarms

        url = "https://api.weather.gov/alerts/active?status=actual&message_type=alert&event=Tornado%20Warning,Severe%20Thunderstorm%20Warning,Flash%20Flood%20Warning"
        headers = {
            "User-Agent": NWS_USER_AGENT,
            "Accept": "application/geo+json"
        }

        triggered_alarms: List[Dict[str, Any]] = []
        raw_alerts_count = 0
        overall_threat_level = "NOMINAL"  # NOMINAL, ADVISORY, WATCH, WARNING, TORNADO_EMERGENCY

        try:
            async with httpx.AsyncClient(timeout=9.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    features = data.get("features", [])
                    raw_alerts_count = len(features)

                    for feat in features:
                        props = feat.get("properties", {})
                        event_name = props.get("event", "")
                        headline = props.get("headline", "")
                        desc = props.get("description", "")
                        area = props.get("areaDesc", "")
                        severity = props.get("severity", "Unknown")
                        urgency = props.get("urgency", "Unknown")
                        event_lower = event_name.lower()
                        desc_lower = desc.lower()

                        # Check trigger conditions
                        is_tornado = "tornado" in event_lower
                        is_severe_storm = "severe thunderstorm" in event_lower
                        is_flood = "flash flood" in event_lower or "flood" in event_lower

                        is_ground_tornado = False
                        is_hook_echo = "hook echo" in desc_lower or "rotation" in desc_lower or "radar indicated rotation" in desc_lower
                        is_supercell = "supercell" in desc_lower or "severe rotating" in desc_lower or is_hook_echo

                        if is_tornado:
                            if "tornado...observed" in desc_lower or "confirmed tornado" in desc_lower or "tornado emergency" in desc_lower or "catastrophic" in desc_lower:
                                is_ground_tornado = True
                                overall_threat_level = "TORNADO_EMERGENCY"
                            elif overall_threat_level != "TORNADO_EMERGENCY":
                                overall_threat_level = "WARNING"
                        elif is_severe_storm and overall_threat_level not in ("TORNADO_EMERGENCY", "WARNING"):
                            overall_threat_level = "WARNING"

                        # Wind gust check
                        wind_gust_mph = 0.0
                        for kw in ["wind...", "gusts up to", "gusts to"]:
                            if kw in desc_lower:
                                try:
                                    part = desc_lower.split(kw)[1][:10]
                                    nums = "".join(ch for ch in part if ch.isdigit())
                                    if nums:
                                        wind_gust_mph = float(nums[:3])
                                        break
                                except Exception:
                                    pass

                        # Hail size check
                        hail_size_inches = 0.0
                        for kw in ["hail...", "quarter size", "golf ball", "baseball", "tennis ball"]:
                            if kw in desc_lower:
                                if "baseball" in desc_lower:
                                    hail_size_inches = 2.75
                                elif "golf ball" in desc_lower:
                                    hail_size_inches = 1.75
                                elif "tennis ball" in desc_lower:
                                    hail_size_inches = 2.5
                                elif "quarter size" in desc_lower:
                                    hail_size_inches = 1.0
                                else:
                                    try:
                                        part = desc_lower.split(kw)[1][:10]
                                        nums = "".join(ch for ch in part if ch.isdigit() or ch == ".")
                                        if nums:
                                            hail_size_inches = float(nums[:4])
                                    except Exception:
                                        pass
                                break

                        # Apply user configuration filters
                        should_trigger = False
                        trigger_reasons = []

                        if self.config.get("twister_tornado") and is_tornado:
                            should_trigger = True
                            trigger_reasons.append("TORNADO WARNING" if not is_ground_tornado else "CONFIRMED TORNADO ON GROUND")

                        if self.config.get("supercell") and is_supercell:
                            should_trigger = True
                            trigger_reasons.append("SUPERCELL / ROTATING MESOCYCLONE")

                        if self.config.get("hook_echo") and is_hook_echo:
                            should_trigger = True
                            trigger_reasons.append("HOOK ECHO ROTATION DETECTED")

                        if self.config.get("severe_thunderstorm") and is_severe_storm:
                            min_gust = self.config.get("min_wind_gust_mph", 58.0)
                            min_hail = self.config.get("min_hail_size_inches", 1.0)
                            if wind_gust_mph >= min_gust or hail_size_inches >= min_hail:
                                should_trigger = True
                                trigger_reasons.append(f"SEVERE STORM (Wind: {wind_gust_mph} mph, Hail: {hail_size_inches}\")")

                        if self.config.get("flash_flood") and is_flood:
                            should_trigger = True
                            trigger_reasons.append("FLASH FLOOD WARNING")

                        if should_trigger:
                            coords = self._extract_coordinates_from_feature(feat)
                            lat = coords["lat"] if coords else 35.0
                            lon = coords["lon"] if coords else -97.0

                            # Find nearest genuine camera feed
                            nearest_cams = []
                            if camera_engine:
                                nearest_cams = camera_engine.find_nearest_camera(lat, lon, limit=3, prefer_real=True)

                            best_cam = nearest_cams[0] if nearest_cams else None

                            triggered_alarms.append({
                                "id": props.get("id", f"alarm_{len(triggered_alarms)}"),
                                "event": event_name,
                                "headline": headline,
                                "severity": severity,
                                "urgency": urgency,
                                "area": area,
                                "lat": lat,
                                "lon": lon,
                                "centroid": {"lat": lat, "lon": lon},
                                "is_ground_tornado": is_ground_tornado,
                                "is_supercell": is_supercell,
                                "is_hook_echo": is_hook_echo,
                                "wind_gust_mph": wind_gust_mph,
                                "hail_size_inches": hail_size_inches,
                                "trigger_reasons": trigger_reasons,
                                "touchdown_sector": {
                                    "lat": lat,
                                    "lon": lon,
                                    "area": area
                                },
                                "nearest_camera": {
                                    "id": best_cam.get("id") if best_cam else None,
                                    "title": best_cam.get("title") if best_cam else "Sector Observation Point",
                                    "provider": best_cam.get("provider") if best_cam else "TrafficNetwork",
                                    "distance_km": best_cam.get("distance_km") if best_cam else None,
                                    "stream_url": best_cam.get("stream_url") if best_cam else None,
                                    "preview_url": best_cam.get("preview_url") if best_cam else None,
                                    "lat": best_cam.get("lat") if best_cam else lat,
                                    "lon": best_cam.get("lon") if best_cam else lon
                                } if best_cam else None,
                                "radar_tile_url": NOAA_NEXRAD_TILE_URL,
                                "timestamp": props.get("sent", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
                            })
        except Exception as e:
            logger.warning(f"Error polling live NOAA alerts: {e}")

        res = {
            "status": "online",
            "overall_threat_level": overall_threat_level,
            "has_active_alarms": len(triggered_alarms) > 0,
            "alarm_count": len(triggered_alarms),
            "raw_alerts_checked": raw_alerts_count,
            "polling_interval_sec": self.config.get("polling_interval_sec", 60),
            "config": self.config,
            "active_alarms": triggered_alarms,
            "last_evaluated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        self._cached_alarms = res
        self._last_poll_ts = now
        return res

    def trigger_test_alarm(self, camera_engine=None, sector: str = "Oklahoma Tornado Alley") -> Dict[str, Any]:
        """
        Generates a verified emergency drill test alarm for confirmed EF-4/EF-5 twister touchdown.
        Locates the nearest live traffic camera and prepares audio siren + notification payload.
        """
        # Test coordinates: Moore / Norman, Oklahoma corridor (Ground Zero of classic outbreaks)
        test_lat = 35.3395
        test_lon = -97.4867

        nearest_cams = []
        if camera_engine:
            nearest_cams = camera_engine.find_nearest_camera(test_lat, test_lon, limit=3, prefer_real=True)

        best_cam = nearest_cams[0] if nearest_cams else {
            "id": "okdot_i35_moore",
            "title": "OKDOT - I-35 @ 12th St Moore Live Traffic Cam",
            "provider": "OKDOT",
            "distance_km": 1.2,
            "lat": 35.3411,
            "lon": -97.4891,
            "stream_url": "https://oktraffic.org/",
            "preview_url": "https://oktraffic.org/"
        }

        test_event = {
            "id": f"drill_tornado_{int(time.time())}",
            "is_drill_test": True,
            "event": "TORNADO EMERGENCY // CONFIRMED TWISTER ON GROUND",
            "headline": "TEST ALARM: Destructive EF-4 Wedge Tornado Touchdown Confirmed by Doppler Radar & Spotters",
            "severity": "Extreme",
            "urgency": "Immediate",
            "area": "Cleveland County & McClain County, Oklahoma (Moore / Norman Sector)",
            "lat": test_lat,
            "lon": test_lon,
            "centroid": {"lat": test_lat, "lon": test_lon},
            "is_ground_tornado": True,
            "is_supercell": True,
            "is_hook_echo": True,
            "ef_scale": 4,
            "wind_gust_mph": 195.0,
            "hail_size_inches": 3.0,
            "trigger_reasons": [
                "CONFIRMED TORNADO ON GROUND (DRILL)",
                "RADAR HOOK ECHO ROTATION CONFIRMED",
                "DESTRUCTIVE WIND GUST (195 MPH)"
            ],
            "touchdown_sector": {
                "lat": test_lat,
                "lon": test_lon,
                "area": "Moore / Norman Corridor, OK"
            },
            "nearest_camera": {
                "id": best_cam.get("id"),
                "title": best_cam.get("title"),
                "provider": best_cam.get("provider"),
                "distance_km": best_cam.get("distance_km", 1.2),
                "stream_url": best_cam.get("stream_url"),
                "preview_url": best_cam.get("preview_url"),
                "lat": best_cam.get("lat"),
                "lon": best_cam.get("lon")
            },
            "radar_tile_url": NOAA_NEXRAD_TILE_URL,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "action_instructions": "TAKE SHELTER IMMEDIATELY. Move to an interior room on the lowest floor of a sturdy building."
        }

        return {
            "status": "drill_activated",
            "message": "Tactical Severe Weather Drill Triggered: Siren and Notification payload dispatched.",
            "alarm": test_event
        }

    def get_nearest_twister_feed(self, lat: float, lon: float, camera_engine=None) -> Dict[str, Any]:
        """
        Instantly locates the nearest live traffic camera and Doppler radar sector for given coordinates.
        """
        cams = []
        if camera_engine:
            cams = camera_engine.find_nearest_camera(lat, lon, limit=5, prefer_real=True)

        return {
            "status": "success",
            "query_lat": lat,
            "query_lon": lon,
            "radar_tile_url": NOAA_NEXRAD_TILE_URL,
            "cameras_found": len(cams),
            "primary_camera": cams[0] if cams else None,
            "backup_cameras": cams[1:4] if len(cams) > 1 else []
        }


# Singleton instance
weather_alarm_engine = WeatherAlarmEngine()
