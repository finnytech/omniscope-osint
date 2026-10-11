"""
CYBER-SPECTRE-NEXUS: Historical Weather, Tornado and NOAA Extreme Storm Archive Engine
===================================================================================
Provides dual-tier historical meteorological reconstruction:
1. NOAA / IEM Local Storm Reports (LSR) Archive (USA exclusive):
   - Confirmed tornadoes with EF ratings, damage survey narratives, touchdown coords.
   - Severe thunderstorm wind gusts (mph/knots) and high sustained winds.
   - Large hail and flash flood reports.
2. Open-Meteo Historical Climate Archive (Global 1940 - Present):
   - Hourly and daily wind speeds, peak gusts, temperatures, surface pressure.
3. Multi-Lingual City Geocoding Search:
   - Resolves global and US cities to coordinates and administrative jurisdictions.
4. Curated Historical Outbreak Presets:
   - Moore OK (2013 EF5), Joplin MO (2011 EF5), 2011 Super Outbreak, etc.
"""

import os
import re
import time
import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("ArchiveEngine")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)

USER_AGENT = "CyberSpectreNexus/2.0 (contact@cyberspectre.net, historical-archive)"

HISTORIC_PRESETS = [
    {
        "id": "moore_2013",
        "title": "Moore, OK Violent EF5 Tornado Outbreak",
        "date": "2013-05-20",
        "location": "Moore, Oklahoma, USA",
        "state": "OK",
        "lat": 35.3395,
        "lon": -97.4867,
        "country": "US",
        "category": "EF5 Tornado // Supercell Outbreak",
        "description": "Peak winds estimated over 210 mph, 17-mile damage path through Newcastle, South Oklahoma City, and Moore."
    },
    {
        "id": "joplin_2011",
        "title": "Joplin, MO Catastrophic EF5 Multi-Vortex",
        "date": "2011-05-22",
        "location": "Joplin, Missouri, USA",
        "state": "MO",
        "lat": 37.0842,
        "lon": -94.5133,
        "country": "US",
        "category": "EF5 Tornado // Multi-Vortex",
        "description": "Deadliest single tornado in modern US history (158 casualties), rain-wrapped mile-wide wedge with >200 mph winds."
    },
    {
        "id": "super_outbreak_2011",
        "title": "2011 Super Outbreak (Tuscaloosa - Birmingham EF4)",
        "date": "2011-04-27",
        "location": "Tuscaloosa, Alabama, USA",
        "state": "AL",
        "lat": 33.2098,
        "lon": -87.5692,
        "country": "US",
        "category": "Historic Super Outbreak (360 Tornadoes)",
        "description": "Violent long-track wedge tornado through Tuscaloosa and northern Birmingham with 190 mph peak winds."
    },
    {
        "id": "el_reno_2013",
        "title": "El Reno, OK Record 2.6-Mile Wide Tornado",
        "date": "2013-05-31",
        "location": "El Reno, Oklahoma, USA",
        "state": "OK",
        "lat": 35.5323,
        "lon": -97.9550,
        "country": "US",
        "category": "Widest Tornado in History (2.6 mi / 295+ mph Radar)",
        "description": "Widest documented tornado on Earth with Doppler on Wheels mobile radar measuring 295-302 mph sub-vortices."
    },
    {
        "id": "rolling_fork_2023",
        "title": "Rolling Fork & Silver City, MS Violent EF4",
        "date": "2023-03-24",
        "location": "Rolling Fork, Mississippi, USA",
        "state": "MS",
        "lat": 32.9065,
        "lon": -90.8782,
        "country": "US",
        "category": "EF4 Violent Long-Track Nighttime Wedge",
        "description": "Intense 59-mile long-track tornado tearing through the Mississippi Delta with 170 mph winds."
    },
    {
        "id": "mayfield_2021",
        "title": "Quad-State Long-Track Tornado (Mayfield, KY EF4)",
        "date": "2021-12-10",
        "location": "Mayfield, Kentucky, USA",
        "state": "KY",
        "lat": 36.7417,
        "lon": -88.6367,
        "country": "US",
        "category": "Winter Quad-State Outbreak (165.7 mi Path)",
        "description": "Extraordinary December long-track nocturnal supercell traveling 165+ miles across Arkansas, Missouri, Tennessee, and Kentucky."
    },
    {
        "id": "bridge_creek_1999",
        "title": "Bridge Creek - Moore, OK Historic F5 Outbreak",
        "date": "1999-05-03",
        "location": "Bridge Creek, Oklahoma, USA",
        "state": "OK",
        "lat": 35.2339,
        "lon": -97.7289,
        "country": "US",
        "category": "F5 Highest Wind Speed Recorded on Earth (301 mph)",
        "description": "Mobile Doppler radar measured 301 ± 20 mph wind speeds, the highest atmospheric surface wind speed ever observed."
    },
    {
        "id": "storm_zeynep_2022",
        "title": "Orkan Zeynep / Storm Eunice (Europa-Orkan)",
        "date": "2022-02-18",
        "location": "Hamburg / Norddeutschland",
        "state": "HH",
        "lat": 53.5511,
        "lon": 9.9937,
        "country": "DE",
        "category": "Europäischer Orkan // Windspitzen > 196 km/h",
        "description": "Schwerster Nordsee-Orkan der Dekade mit Windspitzen von bis zu 196 km/h (The Needles) und orkanartigen Böen in Deutschland."
    }
]

class ArchiveEngine:
    def __init__(self):
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._geo_cache: Dict[str, Tuple[float, Any]] = {}

    def get_presets(self) -> List[Dict[str, Any]]:
        return HISTORIC_PRESETS

    def search_cities(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        clean_q = query.strip().lower()
        if not clean_q or len(clean_q) < 2:
            return []

        now = time.time()
        if clean_q in self._geo_cache:
            ts, val = self._geo_cache[clean_q]
            if now - ts < 3600.0:
                return val

        encoded = urllib.parse.quote(query.strip())
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded}&count={limit}&language=de&format=json"
        results = []

        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=7.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("results", []):
                    c_code = (item.get("country_code") or "").upper()
                    results.append({
                        "name": item.get("name"),
                        "lat": item.get("latitude"),
                        "lon": item.get("longitude"),
                        "country": item.get("country"),
                        "country_code": c_code,
                        "state": item.get("admin1") or "",
                        "is_usa": (c_code == "US"),
                        "elevation": item.get("elevation"),
                        "timezone": item.get("timezone") or "UTC"
                    })
            self._geo_cache[clean_q] = (now, results)
        except Exception as e:
            logger.warning(f"City geocode query error for '{query}': {e}")

        return results

    def fetch_noaa_storm_reports(
        self,
        date_str: str,
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Queries NOAA/IEM Local Storm Reports (LSR) for official NWS confirmed tornadoes,
        severe thunderstorm wind gusts, hail, and flash floods.
        date_str: 'YYYY-MM-DD'
        """
        cache_key = f"noaa_lsr:{date_str}:{state or 'ALL'}"
        now = time.time()
        if cache_key in self._cache:
            ts, val = self._cache[cache_key]
            if now - ts < 1800.0:
                return val

        sts = f"{date_str}T00:00"
        ets = f"{date_str}T23:59"
        params = [f"sts={sts}", f"ets={ets}"]
        if state and len(state.strip()) == 2:
            params.append(f"states={state.strip().upper()}")

        query_str = "&".join(params)
        url = f"https://mesonet.agron.iastate.edu/geojson/lsr.php?{query_str}"

        tornadoes = []
        wind_gusts = []
        hail_reports = []
        floods = []
        total_reports = 0

        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=12.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                features = data.get("features", [])
                total_reports = len(features)

                for f in features:
                    props = f.get("properties", {})
                    geom = f.get("geometry", {})
                    coords = geom.get("coordinates", [])
                    if len(coords) < 2:
                        continue
                    lon, lat = coords[0], coords[1]

                    type_code = str(props.get("type") or "").strip().upper()
                    type_text = str(props.get("typetext") or "").strip().upper()
                    mag_val = props.get("mag")
                    remark = str(props.get("remark") or "").strip()
                    city = props.get("city") or "Unknown Location"
                    county = props.get("county") or ""
                    st = props.get("state") or ""
                    valid_ts = props.get("valid")
                    source = props.get("source") or "NWS"

                    # Check Tornado
                    if "TORNADO" in type_text or type_code == "T":
                        ef_rating = "TORNADO"
                        ef_match = re.search(r"\b(EF[- ]?[0-5]|F[- ]?[0-5])\b", f"{remark} {type_text}", re.I)
                        if ef_match:
                            ef_rating = ef_match.group(1).upper().replace(" ", "-")
                        elif mag_val is not None:
                            try:
                                m_int = int(mag_val)
                                if 0 <= m_int <= 5:
                                    ef_rating = f"EF{m_int}"
                            except Exception:
                                pass

                        tornadoes.append({
                            "id": f"tor_{len(tornadoes)+1}",
                            "type": "TORNADO",
                            "rating": ef_rating,
                            "lat": lat,
                            "lon": lon,
                            "city": city,
                            "county": county,
                            "state": st,
                            "timestamp": valid_ts,
                            "source": source,
                            "magnitude": mag_val,
                            "remark": remark
                        })

                    # Check Wind Gusts
                    elif "WND GST" in type_text or "WIND GUST" in type_text or type_code == "G":
                        mph = None
                        try:
                            mph = float(mag_val) if mag_val is not None else None
                        except Exception:
                            pass

                        wind_gusts.append({
                            "id": f"wnd_{len(wind_gusts)+1}",
                            "type": "WIND_GUST",
                            "speed_mph": mph,
                            "speed_kmh": round(mph * 1.60934, 1) if mph else None,
                            "lat": lat,
                            "lon": lon,
                            "city": city,
                            "county": county,
                            "state": st,
                            "timestamp": valid_ts,
                            "source": source,
                            "remark": remark
                        })

                    # Check Hail
                    elif "HAIL" in type_text or type_code == "H":
                        inches = None
                        try:
                            inches = float(mag_val) if mag_val is not None else None
                        except Exception:
                            pass

                        hail_reports.append({
                            "id": f"hail_{len(hail_reports)+1}",
                            "type": "HAIL",
                            "size_inches": inches,
                            "size_cm": round(inches * 2.54, 2) if inches else None,
                            "lat": lat,
                            "lon": lon,
                            "city": city,
                            "county": county,
                            "state": st,
                            "timestamp": valid_ts,
                            "source": source,
                            "remark": remark
                        })

                    # Check Flooding
                    elif "FLOOD" in type_text or type_code == "F":
                        floods.append({
                            "id": f"fld_{len(floods)+1}",
                            "type": "FLASH_FLOOD",
                            "lat": lat,
                            "lon": lon,
                            "city": city,
                            "county": county,
                            "state": st,
                            "timestamp": valid_ts,
                            "source": source,
                            "remark": remark
                        })

        except Exception as e:
            logger.warning(f"NOAA IEM LSR query failed for date {date_str}: {e}")

        result = {
            "date": date_str,
            "state_filter": state or "ALL_USA",
            "source": "NOAA / NWS Storm Prediction Center LSR Archive",
            "total_reports": total_reports,
            "tornado_count": len(tornadoes),
            "wind_gust_count": len(wind_gusts),
            "hail_count": len(hail_reports),
            "flood_count": len(floods),
            "max_wind_mph": max([w["speed_mph"] for w in wind_gusts if w.get("speed_mph")], default=None),
            "max_hail_inches": max([h["size_inches"] for h in hail_reports if h.get("size_inches")], default=None),
            "tornadoes": tornadoes,
            "wind_gusts": wind_gusts,
            "hail_reports": hail_reports,
            "floods": floods
        }

        self._cache[cache_key] = (now, result)
        return result

    def fetch_historical_weather(self, lat: float, lon: float, date_str: str) -> Dict[str, Any]:
        """
        Queries Open-Meteo Historical Climate Archive (1940 to present)
        for detailed hourly and daily atmospheric data.
        """
        cache_key = f"om_hist:{round(lat, 3)}:{round(lon, 3)}:{date_str}"
        now = time.time()
        if cache_key in self._cache:
            ts, val = self._cache[cache_key]
            if now - ts < 3600.0:
                return val

        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat}&longitude={lon}&start_date={date_str}&end_date={date_str}&"
            f"hourly=temperature_2m,relative_humidity_2m,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_gusts_10m&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,weather_code&"
            f"timezone=auto"
        )

        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self._cache[cache_key] = (now, data)
                return data
        except Exception as e:
            logger.error(f"Error querying Open-Meteo archive for ({lat}, {lon}) on {date_str}: {e}")
            return {"error": str(e), "latitude": lat, "longitude": lon, "date": date_str}

    def query_archive(
        self,
        date_str: str,
        lat: float,
        lon: float,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country_code: str = "US"
    ) -> Dict[str, Any]:
        """
        Combined master archive query.
        Returns:
        - Meteorological atmospheric profile (hourly & daily).
        - NOAA extreme storm reports (tornadoes, wind gusts, hail) if USA.
        """
        is_usa = (country_code.upper() in ("US", "USA")) or (-125.0 <= lon <= -66.0 and 24.0 <= lat <= 50.0)
        hist_weather = self.fetch_historical_weather(lat, lon, date_str)

        noaa_reports = None
        if is_usa:
            noaa_reports = self.fetch_noaa_storm_reports(date_str, state=state)

        # Parse daily highlights
        daily = hist_weather.get("daily", {})
        t_max = daily.get("temperature_2m_max", [None])[0] if daily.get("temperature_2m_max") else None
        t_min = daily.get("temperature_2m_min", [None])[0] if daily.get("temperature_2m_min") else None
        w_max_kmh = daily.get("wind_speed_10m_max", [None])[0] if daily.get("wind_speed_10m_max") else None
        g_max_kmh = daily.get("wind_gusts_10m_max", [None])[0] if daily.get("wind_gusts_10m_max") else None
        precip = daily.get("precipitation_sum", [0.0])[0] if daily.get("precipitation_sum") else 0.0

        w_max_mph = round(w_max_kmh / 1.60934, 1) if w_max_kmh is not None else None
        g_max_mph = round(g_max_kmh / 1.60934, 1) if g_max_kmh is not None else None

        # Build hourly curve
        hourly_raw = hist_weather.get("hourly", {})
        times = hourly_raw.get("time", [])
        temps = hourly_raw.get("temperature_2m", [])
        gusts = hourly_raw.get("wind_gusts_10m", [])
        winds = hourly_raw.get("wind_speed_10m", [])
        precips = hourly_raw.get("precipitation", [])

        hourly_series = []
        for i in range(len(times)):
            t_iso = times[i]
            hour_str = t_iso.split("T")[1] if "T" in t_iso else t_iso
            c_temp = temps[i] if i < len(temps) else None
            c_gust = gusts[i] if i < len(gusts) else None
            c_wind = winds[i] if i < len(winds) else None
            c_prec = precips[i] if i < len(precips) else 0.0

            hourly_series.append({
                "hour": hour_str,
                "time": t_iso,
                "temperature_c": c_temp,
                "temperature_f": round(c_temp * 9/5 + 32, 1) if c_temp is not None else None,
                "wind_speed_kmh": c_wind,
                "wind_speed_mph": round(c_wind / 1.60934, 1) if c_wind is not None else None,
                "wind_gust_kmh": c_gust,
                "wind_gust_mph": round(c_gust / 1.60934, 1) if c_gust is not None else None,
                "precipitation_mm": c_prec
            })

        return {
            "status": "success",
            "date": date_str,
            "location": {
                "city": city or "Selected Coordinates",
                "state": state or "",
                "country_code": country_code.upper(),
                "is_usa": is_usa,
                "lat": lat,
                "lon": lon
            },
            "atmospheric_summary": {
                "temperature_max_c": t_max,
                "temperature_max_f": round(t_max * 9/5 + 32, 1) if t_max is not None else None,
                "temperature_min_c": t_min,
                "temperature_min_f": round(t_min * 9/5 + 32, 1) if t_min is not None else None,
                "wind_speed_max_kmh": w_max_kmh,
                "wind_speed_max_mph": w_max_mph,
                "wind_gust_max_kmh": g_max_kmh,
                "wind_gust_max_mph": g_max_mph,
                "precipitation_sum_mm": precip
            },
            "hourly_series": hourly_series,
            "noaa_severe_archive": noaa_reports
        }

archive_engine = ArchiveEngine()
