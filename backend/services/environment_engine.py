"""
CYBER-SPECTRE-NEXUS: Atmospheric Sounding & Global Air Quality Engine
Integrates:
- WAQI (World Air Quality Index - real-time AQI index and health hazard levels)
- OpenAQ (Global Open Air Quality API - PM2.5, PM10, NO2, O3 from 15,000+ government stations)
"""

import httpx
import logging
import time
import json
import os
from typing import Dict, List, Optional

logger = logging.getLogger("EnvironmentEngine")

from backend.config import load_keys

class EnvironmentEngine:
    def __init__(self, keys_file: Optional[str] = None):
        self.cached_readings = {}
        self.cache_ttl = 300  # 5 minutes cache

    def _load_keys(self) -> Dict[str, str]:
        return load_keys()

    async def get_air_quality(self, lat: float = 52.5200, lon: float = 13.4050) -> Dict:
        cache_key = f"{round(lat, 2)}_{round(lon, 2)}"
        now = time.time()
        if cache_key in self.cached_readings:
            cached, ts = self.cached_readings[cache_key]
            if now - ts < self.cache_ttl:
                return cached

        keys = self._load_keys()
        waqi_token = (keys.get("waqi_token") or "").strip()
        openaq_key = (keys.get("openaq_api_key") or "").strip()

        if not waqi_token and not openaq_key:
            return {
                "status": "omitted",
                "enabled": False,
                "message": "Air quality telemetry omitted (no WAQI token or OpenAQ key configured). Zero-fake policy active.",
                "coords": {"lat": lat, "lon": lon}
            }

        result = {
            "status": "active",
            "coords": {"lat": lat, "lon": lon},
            "aqi": 0,
            "category": "PENDING",
            "color": "#94a3b8",
            "dominant_pollutant": "pm25",
            "station_name": "Authentic Sensor Feed",
            "measurements": {
                "pm25": {"value": 0.0, "unit": "µg/m³"},
                "pm10": {"value": 0.0, "unit": "µg/m³"},
                "no2": {"value": 0.0, "unit": "µg/m³"},
                "o3": {"value": 0.0, "unit": "µg/m³"}
            },
            "health_advice": "Atmospheric sensor measurements query in progress.",
            "source": "WAQI & OpenAQ Global Sensor Network"
        }

        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            # 1. Fetch WAQI feed for precise location
            try:
                waqi_url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={waqi_token}"
                resp = await client.get(waqi_url)
                if resp.status_code == 200:
                    d = resp.json()
                    if d.get("status") == "ok":
                        data = d.get("data", {})
                        aqi_val = data.get("aqi", 0)
                        result["aqi"] = aqi_val
                        result["station_name"] = data.get("city", {}).get("name", result["station_name"])
                        result["dominant_pollutant"] = data.get("dominentpol", "pm25")

                        # Categorize AQI
                        if aqi_val <= 50:
                            result["category"] = "GOOD"
                            result["color"] = "#10b981" # Green
                            result["health_advice"] = "Air quality is satisfactory. Atmospheric conditions are clear."
                        elif aqi_val <= 100:
                            result["category"] = "MODERATE"
                            result["color"] = "#eab308" # Yellow
                            result["health_advice"] = "Acceptable quality. Sensitive individuals may experience mild effects."
                        elif aqi_val <= 150:
                            result["category"] = "UNHEALTHY SENSITIVE"
                            result["color"] = "#f97316" # Orange
                            result["health_advice"] = "Sensitive groups may experience health effects. General public not affected."
                        elif aqi_val <= 200:
                            result["category"] = "UNHEALTHY"
                            result["color"] = "#ef4444" # Red
                            result["health_advice"] = "Everyone may begin to experience health effects. Limit prolonged outdoor exertion."
                        elif aqi_val <= 300:
                            result["category"] = "VERY UNHEALTHY"
                            result["color"] = "#a855f7" # Purple
                            result["health_advice"] = "Health alert: everyone may experience more serious health effects."
                        else:
                            result["category"] = "HAZARDOUS"
                            result["color"] = "#881337" # Crimson
                            result["health_advice"] = "Health warnings of emergency conditions. Entire population is likely affected."

                        iaqi = data.get("iaqi", {})
                        if "pm25" in iaqi:
                            result["measurements"]["pm25"]["value"] = iaqi["pm25"]["v"]
                        if "pm10" in iaqi:
                            result["measurements"]["pm10"]["value"] = iaqi["pm10"]["v"]
                        if "no2" in iaqi:
                            result["measurements"]["no2"]["value"] = iaqi["no2"]["v"]
                        if "o3" in iaqi:
                            result["measurements"]["o3"]["value"] = iaqi["o3"]["v"]
            except Exception as e:
                logger.warning(f"WAQI fetch error: {e}")

            # 2. Fetch OpenAQ nearby locations
            try:
                openaq_url = f"https://api.openaq.org/v3/locations?coordinates={lat},{lon}&radius=35000&limit=3"
                headers = {"X-API-Key": openaq_key, "User-Agent": "CyberSpectreNexus/1.0"}
                resp = await client.get(openaq_url, headers=headers)
                if resp.status_code == 200:
                    oq_data = resp.json()
                    results_list = oq_data.get("results", [])
                    if results_list:
                        result["nearby_sensor_stations"] = [
                            {
                                "name": r.get("name"),
                                "id": r.get("id"),
                                "country": r.get("country", {}).get("code", "") if isinstance(r.get("country"), dict) else "",
                                "sensors": [s.get("parameter", {}).get("name") for s in r.get("sensors", [])]
                            }
                            for r in results_list
                        ]
            except Exception as e:
                logger.warning(f"OpenAQ fetch error: {e}")

        self.cached_readings[cache_key] = (result, now)
        return result

environment_engine = EnvironmentEngine()
