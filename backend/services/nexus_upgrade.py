"""
CYBER-SPECTRE-NEXUS v2.5: Real-Data Upgrade Router (/api/v2/*)
Zero simulation. Every endpoint is backed by an authentic public provider:
  NASA FIRMS (MAP_KEY), EPA AirNow (key), OpenRouteService (key), OpenSky (OAuth2),
  NOAA NDBC, USGS Volcano/Water, GDACS (UN/EU), DWD OpenData, CelesTrak (SGP4), SMARD, NOAA SWPC.
All secrets are read from the SQLite3 vault (backend/services/vault.py) - never from code or JSON.
"""

import os
import io
import re
import csv
import json
import math
import time
import sqlite3
import logging
import datetime
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import APIRouter, Query, Body, HTTPException

from backend.services.vault import get_vault_key

logger = logging.getLogger("NexusUpgrade")
router = APIRouter(prefix="/api/v2", tags=["nexus-v2"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_DB = os.path.join(BASE_DIR, "data", "audit_log.db")
UA = {"User-Agent": "CyberSpectreNexus/2.5 (open-data research client)"}

_client: Optional[httpx.AsyncClient] = None


def _http() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(25.0, connect=8.0), headers=UA, follow_redirects=True)
    return _client


# ---------------------------------------------------------------- cache ------
_CACHE: Dict[str, Tuple[float, Any]] = {}


def _cget(key: str, ttl: float):
    e = _CACHE.get(key)
    if e and time.time() - e[0] < ttl:
        return e[1]
    return None


def _cstale(key: str):
    e = _CACHE.get(key)
    return e[1] if e else None


def _cset(key: str, val: Any):
    _CACHE[key] = (time.time(), val)
    return val


def _bbox(bbox: Optional[str]) -> Optional[Tuple[float, float, float, float]]:
    """bbox = minLon,minLat,maxLon,maxLat"""
    if not bbox:
        return None
    try:
        a = [float(x) for x in bbox.split(",")]
        if len(a) == 4:
            return a[0], a[1], a[2], a[3]
    except ValueError:
        pass
    raise HTTPException(400, "bbox must be minLon,minLat,maxLon,maxLat")


def _in(b, lat, lon):
    if b is None:
        return True
    if b[2] - b[0] >= 359:
        return b[1] <= lat <= b[3]
    return b[1] <= lat <= b[3] and b[0] <= lon <= b[2]


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


# --------------------------------------------------------------- FIRMS -------
FIRMS_SOURCES = ["VIIRS_NOAA21_NRT", "VIIRS_NOAA20_NRT", "VIIRS_SNPP_NRT", "MODIS_NRT"]


async def _firms_world(day_range: int) -> List[Dict[str, Any]]:
    """Authentic NASA FIRMS area API. NOTE: 'world' keyword returns empty - explicit bbox required."""
    ck = f"firms_world_{day_range}"
    hit = _cget(ck, 600)
    if hit is not None:
        return hit
    key = get_vault_key("firms_map_key")
    if not key:
        raise HTTPException(503, "firms_map_key missing in vault")
    out: List[Dict[str, Any]] = []
    seen = set()
    for src in FIRMS_SOURCES:
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{src}/-180,-90,180,90/{day_range}"
        try:
            r = await _http().get(url, timeout=60.0)
            if r.status_code != 200 or r.text.startswith(("Invalid", "Error")) or "latitude" not in r.text[:200]:
                logger.warning("FIRMS %s -> HTTP %s %s", src, r.status_code, r.text[:80])
                continue
            for row in csv.DictReader(io.StringIO(r.text)):
                try:
                    lat = float(row["latitude"]); lon = float(row["longitude"])
                except (KeyError, ValueError):
                    continue
                # de-duplicate overlapping satellites on ~375 m grid + date + hour
                k = (round(lat, 2), round(lon, 2), row.get("acq_date"), (row.get("acq_time") or "")[:2])
                if k in seen:
                    continue
                seen.add(k)
                conf = row.get("confidence", "")
                frp = float(row.get("frp") or 0.0)
                bright = float(row.get("bright_ti4") or row.get("brightness") or 0.0)
                out.append({
                    "lat": lat, "lon": lon, "frp": frp, "brightness": bright,
                    "confidence": conf, "acq_date": row.get("acq_date"),
                    "acq_time": row.get("acq_time"), "satellite": row.get("satellite"),
                    "instrument": row.get("instrument"), "daynight": row.get("daynight"), "source": src,
                })
        except Exception as ex:
            logger.warning("FIRMS %s fetch failed: %s", src, ex)
    if out:
        return _cset(ck, out)
    stale = _cstale(ck)
    if stale is not None:
        return stale
    raise HTTPException(502, "NASA FIRMS unavailable")


def _firms_conf_ok(c: str, min_conf: str) -> bool:
    if min_conf == "all":
        return True
    c = (c or "").lower()
    if c in ("l", "low"):
        return False
    if c.isdigit():
        return int(c) >= 30
    return True


@router.get("/firms")
async def firms(bbox: Optional[str] = None, days: int = Query(1, ge=1, le=3),
                limit: int = Query(6000, ge=100, le=30000), min_confidence: str = "nominal"):
    b = _bbox(bbox)
    data = await _firms_world(days)
    sel = [d for d in data if _in(b, d["lat"], d["lon"]) and _firms_conf_ok(d["confidence"], min_confidence)]
    total = len(sel)
    sel.sort(key=lambda d: -d["frp"])
    try:
        lim = int(limit)
    except (TypeError, ValueError):
        lim = int(getattr(limit, "default", 6000)) if hasattr(limit, "default") else 6000
    sel = sel[:lim]
    return {"provider": "NASA FIRMS (VIIRS NOAA-20/21, SNPP, MODIS) - authenticated MAP_KEY",
            "world_detections": len(data), "matched": total, "count": len(sel),
            "total_frp_mw": round(sum(d["frp"] for d in sel), 1), "hotspots": sel}


@router.get("/firms/status")
async def firms_status():
    key = get_vault_key("firms_map_key")
    r = await _http().get(f"https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY={key}")
    return r.json()


# -------------------------------------------------------------- AirNow -------
AQI_CATS = {1: ("GOOD", "#00e400"), 2: ("MODERATE", "#ffff00"), 3: ("USG", "#ff7e00"),
            4: ("UNHEALTHY", "#ff0000"), 5: ("VERY UNHEALTHY", "#8f3f97"), 6: ("HAZARDOUS", "#7e0023")}


@router.get("/airnow")
async def airnow(bbox: str = Query(..., description="minLon,minLat,maxLon,maxLat"),
                 parameters: str = "PM25,OZONE"):
    """EPA AirNow /aq/data (the /observation/ endpoints were retired 2026-10-01)."""
    b = _bbox(bbox)
    # snap bbox to 1 degree to maximise cache hits and protect the AirNow quota (500 calls/h)
    sb = (math.floor(b[0]), math.floor(b[1]), math.ceil(b[2]), math.ceil(b[3]))
    sb = (max(sb[0], -180), max(sb[1], -90), min(sb[2], 180), min(sb[3], 90))
    ck = f"airnow_{sb}_{parameters}"
    hit = _cget(ck, 1800)
    if hit is not None:
        return hit
    key = get_vault_key("airnow_api_key")
    if not key:
        raise HTTPException(503, "airnow_api_key missing in vault")
    end = _now().replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=1)
    start = end - datetime.timedelta(hours=2)
    params = {
        "startDate": start.strftime("%Y-%m-%dT%H"), "endDate": end.strftime("%Y-%m-%dT%H"),
        "parameters": parameters, "BBOX": ",".join(str(x) for x in sb), "dataType": "A",
        "format": "application/json", "verbose": 1, "monitorType": 0,
        "includerawconcentrations": 0, "API_KEY": key,
    }
    try:
        r = await _http().get("https://www.airnowapi.org/aq/data/", params=params, timeout=40.0)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:120]}")
        rows = r.json()
    except Exception as ex:
        stale = _cstale(ck)
        if stale is not None:
            return stale
        raise HTTPException(502, f"AirNow unavailable: {ex}")
    sites: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        sid = row.get("FullAQSCode") or f"{row['Latitude']},{row['Longitude']}"
        s = sites.setdefault(sid, {"id": sid, "lat": row["Latitude"], "lon": row["Longitude"],
                                   "name": row.get("SiteName"), "agency": row.get("AgencyName"),
                                   "readings": {}, "aqi": 0, "category": 1, "utc": row.get("UTC")})
        aqi = row.get("AQI", -999)
        if aqi is None or aqi < 0:
            continue
        s["readings"][row["Parameter"]] = {"aqi": aqi, "value": row.get("Value"), "unit": row.get("Unit"), "utc": row.get("UTC")}
        if aqi >= s["aqi"]:
            s["aqi"] = aqi
            s["category"] = row.get("Category") or s["category"]
            s["utc"] = row.get("UTC")
    out = []
    for s in sites.values():
        if not s["readings"]:
            continue
        label, color = AQI_CATS.get(int(s["category"]), ("N/A", "#9ca3af"))
        s["label"], s["color"] = label, color
        out.append(s)
    res = {"provider": "EPA AirNow /aq/data", "count": len(out), "bbox": list(sb), "stations": out}
    return _cset(ck, res)


# ---------------------------------------------- OpenRouteService isochrones --
@router.get("/isochrone")
async def isochrone(lat: float, lon: float, minutes: str = "15,30,60", profile: str = "driving-car"):
    if profile not in ("driving-car", "driving-hgv", "cycling-regular", "foot-walking"):
        raise HTTPException(400, "bad profile")
    try:
        mins = sorted({max(1, min(int(float(m)), 120)) for m in minutes.split(",")})[:5]
    except ValueError:
        raise HTTPException(400, "minutes must be comma separated numbers")
    ck = f"iso_{round(lat,3)}_{round(lon,3)}_{mins}_{profile}"
    hit = _cget(ck, 3600)
    if hit is not None:
        return hit
    key = get_vault_key("openrouteservice_key")
    if not key:
        raise HTTPException(503, "openrouteservice_key missing in vault")
    r = await _http().post(f"https://api.openrouteservice.org/v2/isochrones/{profile}",
                           headers={"Authorization": key, "Content-Type": "application/json"},
                           json={"locations": [[lon, lat]], "range": [m * 60 for m in mins], "range_type": "time"})
    if r.status_code != 200:
        raise HTTPException(502, f"OpenRouteService HTTP {r.status_code}: {r.text[:160]}")
    gj = r.json()
    for f in gj.get("features", []):
        f["properties"]["minutes"] = round(f["properties"].get("value", 0) / 60)
    gj["provider"] = "OpenRouteService"
    return _cset(ck, gj)


# --------------------------------------------------------- NDBC buoys --------
def _f(v):
    try:
        x = float(v)
        return None if x in (99.0, 999.0, 9999.0) or math.isnan(x) else x
    except (TypeError, ValueError):
        return None


@router.get("/buoys")
async def buoys(bbox: Optional[str] = None, limit: int = Query(1500, le=3000)):
    b = _bbox(bbox)
    ck = "ndbc_all"
    data = _cget(ck, 600)
    if data is None:
        try:
            r = await _http().get("https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt")
            r.raise_for_status()
            data = []
            for line in r.text.splitlines():
                if line.startswith("#") or not line.strip():
                    continue
                p = line.split()
                if len(p) < 19:
                    continue
                lat, lon = _f(p[1]), _f(p[2])
                if lat is None or lon is None:
                    continue
                wvht = _f(p[11])
                data.append({
                    "id": p[0], "lat": lat, "lon": lon,
                    "time": f"{p[3]}-{p[4]}-{p[5]}T{p[6]}:{p[7]}Z",
                    "wind_dir": _f(p[8]), "wind_ms": _f(p[9]), "gust_ms": _f(p[10]),
                    "wave_m": wvht, "wave_period_s": _f(p[12]), "pressure_hpa": _f(p[15]),
                    "air_c": _f(p[17]), "water_c": _f(p[18]),
                    "storm": bool((wvht or 0) >= 4.0 or (_f(p[10]) or 0) >= 20.0),
                })
            _cset(ck, data)
        except Exception as ex:
            data = _cstale(ck)
            if data is None:
                raise HTTPException(502, f"NDBC unavailable: {ex}")
    sel = [d for d in data if _in(b, d["lat"], d["lon"])][:limit]
    return {"provider": "NOAA NDBC", "count": len(sel), "buoys": sel}


# ------------------------------------------------------------ volcanoes ------
NVEWS = {1: ("NORMAL", "#22c55e"), 2: ("ADVISORY", "#facc15"), 3: ("WATCH", "#f97316"), 4: ("WARNING", "#dc2626")}


@router.get("/volcanoes")
async def volcanoes():
    ck = "usgs_volc"
    hit = _cget(ck, 1800)
    if hit is not None:
        return hit
    try:
        r = await _http().get("https://volcanoes.usgs.gov/vsc/api/volcanoApi/volcanoesUS")
        r.raise_for_status()
        raw = r.json()
    except Exception as ex:
        stale = _cstale(ck)
        if stale is not None:
            return stale
        raise HTTPException(502, f"USGS Volcano unavailable: {ex}")
    out = []
    for v in raw:
        try:
            lvl = int(v.get("NVEWS") or 1)
        except (TypeError, ValueError):
            lvl = 1
        label, color = NVEWS.get(lvl, ("UNASSIGNED", "#9ca3af"))
        out.append({"id": v.get("vnum"), "name": v.get("vName"), "lat": v.get("latitude"), "lon": v.get("longitude"),
                    "elevation_m": v.get("elevation_m"), "observatory": v.get("obsAbbr"), "region": v.get("subregion"),
                    "level": lvl, "alert": label, "color": color, "url": v.get("webpage")})
    return _cset(ck, {"provider": "USGS Volcano Hazards Program", "count": len(out),
                      "elevated": sum(1 for v in out if v["level"] >= 3), "volcanoes": out})


# --------------------------------------------------------------- GDACS -------
@router.get("/gdacs")
async def gdacs(days: int = Query(14, ge=1, le=60)):
    ck = f"gdacs_{days}"
    hit = _cget(ck, 900)
    if hit is not None:
        return hit
    to = _now().date(); fr = to - datetime.timedelta(days=days)
    url = ("https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=EQ,TC,FL,VO,DR,WF"
           f"&alertlevel=Green;Orange;Red&fromdate={fr}&todate={to}")
    try:
        r = await _http().get(url, timeout=40.0)
        r.raise_for_status()
        gj = r.json()
    except Exception as ex:
        stale = _cstale(ck)
        if stale is not None:
            return stale
        raise HTTPException(502, f"GDACS unavailable: {ex}")
    out = []
    for f in gj.get("features", []):
        p = f.get("properties", {}); g = f.get("geometry") or {}
        if g.get("type") != "Point":
            continue
        lon, lat = g["coordinates"][:2]
        out.append({"id": f"{p.get('eventtype')}{p.get('eventid')}", "type": p.get("eventtype"), "name": p.get("name"),
                    "alert": p.get("alertlevel"), "score": p.get("alertscore"), "country": p.get("country"),
                    "from": p.get("fromdate"), "to": p.get("todate"), "severity": (p.get("severitydata") or {}).get("severitytext"),
                    "lat": lat, "lon": lon, "url": (p.get("url") or {}).get("report")})
    order = {"Red": 0, "Orange": 1, "Green": 2}
    out.sort(key=lambda e: (order.get(e["alert"], 3), e["from"] or ""))
    return _cset(ck, {"provider": "GDACS (UN OCHA / EC JRC)", "count": len(out),
                      "red": sum(1 for e in out if e["alert"] == "Red"),
                      "orange": sum(1 for e in out if e["alert"] == "Orange"), "events": out})


# ----------------------------------------------------- USGS river gauges -----
@router.get("/rivers")
async def rivers(bbox: str = Query(...)):
    b = _bbox(bbox)
    # USGS limits bBox to 25 square degrees
    if (b[2] - b[0]) * (b[3] - b[1]) > 25:
        raise HTTPException(400, "bbox too large (max 25 sq degrees) - zoom in")
    ck = f"usgs_water_{[round(x,1) for x in b]}"
    hit = _cget(ck, 600)
    if hit is not None:
        return hit
    url = ("https://waterservices.usgs.gov/nwis/iv/?format=json&parameterCd=00065,00060&siteStatus=active&bBox="
           + ",".join(f"{x:.4f}" for x in b))
    try:
        r = await _http().get(url, timeout=40.0)
        r.raise_for_status()
        series = r.json()["value"]["timeSeries"]
    except Exception as ex:
        stale = _cstale(ck)
        if stale is not None:
            return stale
        raise HTTPException(502, f"USGS Water unavailable: {ex}")
    sites: Dict[str, Dict[str, Any]] = {}
    for ts in series:
        si = ts["sourceInfo"]; code = si["siteCode"][0]["value"]
        s = sites.setdefault(code, {"id": code, "name": si["siteName"], "lat": si["geoLocation"]["geogLocation"]["latitude"],
                                    "lon": si["geoLocation"]["geogLocation"]["longitude"]})
        vals = ts["values"][0]["value"]
        if not vals:
            continue
        v = _f(vals[-1]["value"])
        if v is None or v < -900:
            continue
        pc = ts["variable"]["variableCode"][0]["value"]
        if pc == "00065":
            s["stage_ft"] = v; s["time"] = vals[-1]["dateTime"]
        else:
            s["discharge_cfs"] = v
    out = [s for s in sites.values() if "stage_ft" in s or "discharge_cfs" in s]
    return _cset(ck, {"provider": "USGS NWIS Instantaneous Values", "count": len(out), "gauges": out})


# ----------------------------------------------------------- DWD warnings ----
DWD_LEVEL = {1: "MINOR", 2: "MODERATE", 3: "SEVERE", 4: "EXTREME"}


@router.get("/dwd-warnings")
async def dwd_warnings(min_level: int = Query(2, ge=1, le=4)):
    ck = "dwd_warn"
    data = _cget(ck, 300)
    if data is None:
        try:
            r = await _http().get("https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json", timeout=40.0)
            r.raise_for_status()
            m = re.search(r"loadWarnings\((.*)\);?\s*$", r.text, re.S)
            data = json.loads(m.group(1) if m else r.text)
            _cset(ck, data)
        except Exception as ex:
            data = _cstale(ck)
            if data is None:
                raise HTTPException(502, f"DWD unavailable: {ex}")
    out = []
    for cell, ws in (data.get("warnings") or {}).items():
        for w in ws:
            if int(w.get("level", 0)) < min_level:
                continue
            out.append({"cell": cell, "region": w.get("regionName"), "state": w.get("state"), "event": w.get("event"),
                        "level": w.get("level"), "severity": DWD_LEVEL.get(w.get("level"), "?"),
                        "headline": w.get("headline"), "description": w.get("description"),
                        "start": w.get("start"), "end": w.get("end")})
    out.sort(key=lambda w: -int(w["level"] or 0))
    return {"provider": "Deutscher Wetterdienst OpenData", "issued": data.get("time"), "count": len(out), "warnings": out[:400]}


# --------------------------------------------------- Satellites (SGP4) -------
SAT_GROUPS = {"stations": "Space Stations", "weather": "Weather", "noaa": "NOAA", "geo": "Geostationary",
              "military": "Military", "resource": "Earth Resources", "gps-ops": "GPS"}


@router.get("/satellites")
async def satellites(group: str = "stations", track_minutes: int = Query(0, ge=0, le=180), limit: int = Query(120, le=400), norad: Optional[int] = None):
    if group not in SAT_GROUPS and norad is None:
        raise HTTPException(400, f"group must be one of {list(SAT_GROUPS)}")
    from sgp4.api import Satrec, jday, WGS84
    ck = f"tle_{group}"
    gp = _cget(ck, 7200)
    if gp is None:
        try:
            r = await _http().get(f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json")
            r.raise_for_status()
            gp = r.json()
            _cset(ck, gp)
        except Exception as ex:
            gp = _cstale(ck)
            if gp is None:
                raise HTTPException(502, f"CelesTrak unavailable: {ex}")

    def gmst(jd):
        t = (jd - 2451545.0) / 36525.0
        g = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t
        return math.radians(g % 360.0)

    def pos(sat, dt):
        jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond / 1e6)
        e, rv, vv = sat.sgp4(jd, fr)
        if e != 0:
            return None
        x, y, z = rv
        th = gmst(jd + fr)
        xe = x * math.cos(th) + y * math.sin(th)
        ye = -x * math.sin(th) + y * math.cos(th)
        lon = math.degrees(math.atan2(ye, xe))
        rr = math.sqrt(x * x + y * y + z * z)
        if rr <= 0:
            return None
        ratio = max(-1.0, min(1.0, z / rr))
        lat = math.degrees(math.asin(ratio))
        spd = math.sqrt(vv[0] ** 2 + vv[1] ** 2 + vv[2] ** 2)
        if math.isnan(lat) or math.isnan(lon) or math.isnan(spd) or math.isnan(rr):
            return None
        return lat, lon, rr - 6371.0, spd

    now = _now()
    out = []
    candidates = gp
    if norad is not None:
        candidates = [e for e in gp if e.get("NORAD_CAT_ID") == norad]
    for e in candidates[:limit]:
        try:
            sat = Satrec()
            ep_str = e["EPOCH"].replace("Z", "+00:00")
            ep = datetime.datetime.fromisoformat(ep_str)
            if ep.tzinfo is not None:
                ep = ep.astimezone(datetime.timezone.utc).replace(tzinfo=None)
            epoch_days = (ep - datetime.datetime(1949, 12, 31)).total_seconds() / 86400.0
            sat.sgp4init(WGS84, "i", e["NORAD_CAT_ID"], epoch_days, e.get("BSTAR", 0.0), e.get("MEAN_MOTION_DOT", 0.0),
                         e.get("MEAN_MOTION_DDOT", 0.0), e["ECCENTRICITY"], math.radians(e["ARG_OF_PERICENTER"]),
                         math.radians(e["INCLINATION"]), math.radians(e["MEAN_ANOMALY"]),
                         e["MEAN_MOTION"] * 2 * math.pi / 1440.0, math.radians(e["RA_OF_ASC_NODE"]))
            p = pos(sat, now)
            if not p:
                continue
            item = {"norad": e["NORAD_CAT_ID"], "name": e["OBJECT_NAME"], "lat": round(p[0], 4), "lon": round(p[1], 4),
                    "alt_km": round(p[2], 1), "speed_kms": round(p[3], 3), "inclination": e["INCLINATION"],
                    "period_min": round(1440.0 / e["MEAN_MOTION"], 1), "epoch": e["EPOCH"]}
            if track_minutes:
                trk = []
                for i in range(0, track_minutes + 1, 2):
                    q = pos(sat, now + datetime.timedelta(minutes=i))
                    if q:
                        trk.append([round(q[0], 3), round(q[1], 3)])
                item["track"] = trk
            out.append(item)
        except Exception:
            continue
    return {"provider": "CelesTrak GP + SGP4 propagation", "group": group, "label": SAT_GROUPS.get(group, "Custom"),
            "count": len(out), "time": now.isoformat(), "satellites": out}


# ------------------------------------------------------------ SMARD grid -----
@router.get("/grid/de")
async def grid_de():
    ck = "smard"
    hit = _cget(ck, 900)
    if hit is not None:
        return hit
    try:
        res = {}
        for fid, label in ((410, "load_mw"), (1223, "lignite_mw"), (4067, "wind_onshore_mw"), (4068, "solar_mw")):
            idx = (await _http().get(f"https://www.smard.de/app/chart_data/{fid}/DE/index_quarterhour.json")).json()
            ts = idx["timestamps"][-1]
            d = (await _http().get(f"https://www.smard.de/app/chart_data/{fid}/DE/{fid}_DE_quarterhour_{ts}.json")).json()
            series = [s for s in d["series"] if s[1] is not None]
            res[label] = {"value": series[-1][1], "time": datetime.datetime.fromtimestamp(series[-1][0] / 1000, datetime.timezone.utc).isoformat(),
                          "history": [s[1] for s in series[-96:]]}
    except Exception as ex:
        stale = _cstale(ck)
        if stale is not None:
            return stale
        raise HTTPException(502, f"SMARD unavailable: {ex}")
    return _cset(ck, {"provider": "Bundesnetzagentur SMARD", **res})


# ----------------------------------------------------------- Space weather ---
@router.get("/kp")
async def kp():
    ck = "kp"
    hit = _cget(ck, 600)
    if hit is not None:
        return hit
    try:
        k = (await _http().get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json")).json()
        sc = (await _http().get("https://services.swpc.noaa.gov/products/noaa-scales.json")).json()
    except Exception as ex:
        stale = _cstale(ck)
        if stale is not None:
            return stale
        raise HTTPException(502, f"SWPC unavailable: {ex}")
    cur = k[-1]
    return _cset(ck, {"provider": "NOAA SWPC", "kp": cur["Kp"], "time": cur["time_tag"],
                      "history": [{"t": x["time_tag"], "kp": x["Kp"]} for x in k[-24:]], "scales": sc.get("0", {})})


# ---------------------------------------------------- Health & threat --------
HEALTH_TARGETS = {
    "NASA FIRMS": "https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/{firms_map_key}/ALL",
    "OpenSky OAuth": "https://auth.opensky-network.org/auth/realms/opensky-network/.well-known/openid-configuration",
    "USGS Earthquakes": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson",
    "NOAA NWS": "https://api.weather.gov/",
    "NOAA NDBC": "https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt",
    "GDACS": "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=EQ,TC,FL,VO,DR,WF",
    "DWD": "https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json",
    "CelesTrak": "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json",
    "NOAA SWPC": "https://services.swpc.noaa.gov/products/noaa-scales.json",
    "RainViewer": "https://api.rainviewer.com/public/weather-maps.json",
    "USGS Volcano": "https://volcanoes.usgs.gov/vsc/api/volcanoApi/volcanoesUS",
    "SMARD": "https://www.smard.de/app/chart_data/410/DE/index_quarterhour.json",
    "Digitraffic AIS": "https://meri.digitraffic.fi/api/ais/v1/locations?from=0",
}


@router.get("/health")
async def provider_health():
    ck = "provider_health"
    hit = _cget(ck, 120)
    if hit is not None:
        return hit
    import asyncio
    keys = {"firms_map_key": get_vault_key("firms_map_key")}

    async def probe(name, url):
        url = url.format(**keys)
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=UA, follow_redirects=True) as c:
                async with c.stream("GET", url) as r:
                    ok = r.status_code < 400
                    code = r.status_code
        except Exception as ex:
            ok, code = False, str(type(ex).__name__)
        ms = round((time.time() - t0) * 1000)
        return {"name": name, "ok": ok, "status": code, "ms": ms, "level": "green" if ok and ms < 2500 else ("yellow" if ok else "red")}

    res = await asyncio.gather(*[probe(n, u) for n, u in HEALTH_TARGETS.items()])
    return _cset(ck, {"checked_at": _now().isoformat(), "up": sum(1 for r in res if r["ok"]), "total": len(res), "providers": res})


@router.get("/threat")
async def threat_matrix():
    """Global threat level 1-5 derived exclusively from live feeds."""
    import asyncio
    hit = _cget("threat_matrix", 120)
    if hit is not None:
        return hit

    score = 0.0
    parts: Dict[str, Any] = {}

    async def quakes():
        r = await asyncio.wait_for(_http().get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"), timeout=8.0)
        f = r.json()["features"]
        mx = max([x["properties"]["mag"] or 0 for x in f] or [0])
        return {"count_m45": len(f), "max_mag": mx, "pts": min(len(f) * 0.15 + max(0, mx - 5.5) * 1.5, 3)}

    async def gd():
        d = await asyncio.wait_for(gdacs(14), timeout=8.0)
        return {"red": d["red"], "orange": d["orange"], "pts": min(d["red"] * 0.8 + d["orange"] * 0.2, 3)}

    async def fires():
        d = await asyncio.wait_for(_firms_world(1), timeout=25.0)
        big = sum(1 for x in d if x["frp"] >= 100)
        return {"detections": len(d), "frp100": big, "pts": min(big / 150.0, 1.5)}

    async def vol():
        d = await asyncio.wait_for(volcanoes(), timeout=8.0)
        return {"watch_or_warning": d["elevated"], "pts": min(d["elevated"] * 0.3, 1.0)}

    async def alerts():
        r = await asyncio.wait_for(_http().get("https://api.weather.gov/alerts/active?status=actual&severity=Extreme"), timeout=8.0)
        n = len(r.json().get("features", []))
        return {"extreme_us": n, "pts": min(n * 0.25, 2.0)}

    names = ["earthquakes", "gdacs", "wildfires", "volcanoes", "nws_extreme"]
    results = await asyncio.gather(quakes(), gd(), fires(), vol(), alerts(), return_exceptions=True)
    for n, r in zip(names, results):
        if isinstance(r, Exception):
            parts[n] = {"error": str(r)[:80], "pts": 0}
        else:
            parts[n] = r
            score += r["pts"]
    level = 1 if score < 1.5 else 2 if score < 3.0 else 3 if score < 5.0 else 4 if score < 7.0 else 5
    labels = {1: "NORMAL", 2: "ERHÖHT", 3: "ANGESPANNT", 4: "KRITISCH", 5: "NOTSTAND"}
    res = {"level": level, "label": labels[level], "score": round(score, 2), "components": parts, "time": _now().isoformat()}
    return _cset("threat_matrix", res)


# ----------------------------------------------------------- Audit log -------
def _audit_conn():
    os.makedirs(os.path.dirname(AUDIT_DB), exist_ok=True)
    c = sqlite3.connect(AUDIT_DB, timeout=10)
    c.execute("""CREATE TABLE IF NOT EXISTS tactical_audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, session TEXT, action TEXT NOT NULL,
        target TEXT, lat REAL, lon REAL, detail TEXT)""")
    return c


@router.post("/audit")
async def audit_write(payload: Dict[str, Any] = Body(...)):
    c = _audit_conn()
    try:
        c.execute("INSERT INTO tactical_audit_log (ts,session,action,target,lat,lon,detail) VALUES (?,?,?,?,?,?,?)",
                  (_now().isoformat(timespec="milliseconds"), str(payload.get("session", ""))[:64],
                   str(payload.get("action", "unknown"))[:64], str(payload.get("target", ""))[:200],
                   payload.get("lat"), payload.get("lon"), json.dumps(payload.get("detail", ""))[:2000]))
        c.commit()
    finally:
        c.close()
    return {"ok": True}


@router.get("/audit")
async def audit_read(limit: int = Query(100, le=1000)):
    c = _audit_conn()
    try:
        rows = c.execute("SELECT id,ts,session,action,target,lat,lon,detail FROM tactical_audit_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    finally:
        c.close()
    return {"count": len(rows), "entries": [dict(zip(("id", "ts", "session", "action", "target", "lat", "lon", "detail"), r)) for r in rows]}


# ---------------------------------------------------- SITREP Report Generator (Feature 07) ----
@router.get("/report/sitrep")
async def generate_sitrep():
    """Generates an authentic Classified Tactical SITREP briefing dossier."""
    tm = await threat_matrix()
    grid = await grid_de()
    kp_info = await kp()
    dwd = await dwd_warnings(min_level=3)
    try:
        nws = await _http().get("https://api.weather.gov/alerts/active?status=actual&severity=Extreme")
        nws_cnt = len(nws.json().get("features", [])) if nws.status_code == 200 else 0
    except Exception:
        nws_cnt = 0
    now_utc = _now()
    return {
        "classification": "TOP SECRET // NOFORN // OSINT TACTICAL SITREP",
        "timestamp_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timestamp_iso": now_utc.isoformat(),
        "threat_level": tm["level"],
        "threat_label": tm["label"],
        "threat_score": tm["score"],
        "components": tm["components"],
        "grid": {
            "load_gw": round(grid["load_mw"]["value"] / 1000.0, 2) if grid.get("load_mw") else None,
            "solar_gw": round(grid["solar_mw"]["value"] / 1000.0, 2) if grid.get("solar_mw") else None,
            "wind_onshore_gw": round(grid["wind_onshore_mw"]["value"] / 1000.0, 2) if grid.get("wind_onshore_mw") else None,
        },
        "space_weather": {
            "kp_index": kp_info.get("kp", 0.0),
            "status": "GEOMAGNETIC STORM" if kp_info.get("kp", 0) >= 5 else "QUIET / NOMINAL"
        },
        "severe_alerts": {
            "dwd_level_3_plus": dwd.get("count", 0),
            "dwd_top_warnings": dwd.get("warnings", [])[:6],
            "nws_extreme_us": nws_cnt
        },
        "summary": f"DEFCON/THREAT LEVEL {tm['level']} ({tm['label']}) // SCORE {tm['score']}. Severe weather: {dwd.get('count', 0)} DWD zones, {nws_cnt} NWS extreme zones. Grid load: {round(grid['load_mw']['value'] / 1000.0, 1) if grid.get('load_mw') else 'N/A'} GW. Geomagnetic: Kp {kp_info.get('kp', 0)}."
    }

