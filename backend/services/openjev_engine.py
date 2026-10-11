"""
CYBER-SPECTRE-NEXUS: OpenJev 0.1 "System One" Visual Weather Verdict Engine
===========================================================================
Codiv (https://api.codiv.ai) serves open System One models that answer typed
questions about a state and return a calibrated probability for every option
in a single denoising step - there is no text generation and no parsing, so an
answer can never fall outside the schema.

This engine turns the fused meteorological state of a map sector the user has
selected (numerical models + multi-model supercomputer consensus + certified
ground weather stations) into a structured OpenJev query and returns a fully
calibrated visual verdict that the frontend paints directly onto the map.

The classical text-based Jev Forecast Mode (backend/services/jev_engine.py)
is left untouched - both AI modes coexist side by side.
"""

import os
import time
import asyncio
import logging
from typing import Dict, Any, Optional

import httpx

from backend.config import load_keys

logger = logging.getLogger("OpenJevEngine")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)

OPENJEV_BASE_URL = os.environ.get("CODIV_BASE_URL", "https://api.codiv.ai")
OPENJEV_MODEL = "openjev-latest"

CONDITION_COLORS = {
    "clear": "#38bdf8",
    "cloudy": "#94a3b8",
    "rain": "#0ea5e9",
    "showers": "#22d3ee",
    "storm": "#ef4444",
    "snow": "#e2e8f0",
    "fog": "#a855f7",
    "wind": "#f59e0b",
    "heat": "#f97316",
    "mixed": "#818cf8",
}

CONDITION_ICONS = {
    "clear": "\u2600\ufe0f",
    "cloudy": "\u2601\ufe0f",
    "rain": "\U0001f327\ufe0f",
    "showers": "\U0001f326\ufe0f",
    "storm": "\u26c8\ufe0f",
    "snow": "\u2744\ufe0f",
    "fog": "\U0001f32b\ufe0f",
    "wind": "\U0001f4a8",
    "heat": "\U0001f525",
    "mixed": "\U0001f328\ufe0f",
}


class OpenJevEngine:
    """Quota-friendly OpenJev 0.1 (Codiv System One) visual verdict engine."""

    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 600          # 10 minutes: System One answers are cheap but cache anyway
        self.max_retries = 3
        self.request_count = 0
        self.last_error: Optional[str] = None

    # ------------------------------------------------------------------ state
    @staticmethod
    def _build_state(jev: Dict[str, Any]) -> Dict[str, Any]:
        target = jev.get("target", {}) or {}
        nf = jev.get("numerical_forecast", {}) or {}
        conv = nf.get("atmospheric_convection", {}) or {}
        cons = jev.get("multi_engine_consensus", {}) or {}
        station = jev.get("ground_stations", {}) or {}
        dec = jev.get("jev_decision", {}) or {}
        return {
            "zone": {
                "center_lat": target.get("center_lat"),
                "center_lon": target.get("center_lon"),
                "area_km2": target.get("zone_area_km2"),
                "bounds": target.get("bounds"),
            },
            "forecast_horizon": {
                "target_date": target.get("target_date"),
                "days_ahead": target.get("days_ahead", 0),
            },
            "numerical_weather": {
                "condition": nf.get("condition"),
                "wmo_code": nf.get("wmo_code"),
                "temperature_max_c": nf.get("temp_max_c"),
                "temperature_min_c": nf.get("temp_min_c"),
                "precipitation_sum_mm": nf.get("precip_sum_mm"),
                "precipitation_probability_pct": nf.get("precip_probability_pct"),
                "wind_max_kmh": nf.get("wind_max_kmh"),
                "wind_gusts_max_kmh": nf.get("gusts_max_kmh"),
                "wind_direction_deg": nf.get("wind_direction_deg"),
                "uv_index_max": nf.get("uv_index_max"),
            },
            "atmospheric_instability": {
                "cape_j_kg": conv.get("max_cape_j_kg"),
                "surface_pressure_min_hpa": conv.get("min_surface_pressure_hpa"),
                "pressure_drop_hpa": conv.get("pressure_drop_hpa"),
                "dewpoint_max_c": conv.get("max_dewpoint_c"),
                "relative_humidity_pct": conv.get("avg_relative_humidity_pct"),
                "visibility_min_km": conv.get("min_visibility_km"),
                "cloud_cover_pct": conv.get("avg_cloud_cover_pct"),
            },
            "multi_model_consensus": {
                "models_compared": cons.get("models_compared"),
                "consensus_temp_c": cons.get("consensus_temp_c"),
                "model_spread_c": cons.get("model_spread_c"),
                "agreement": cons.get("confidence"),
            },
            "ground_station_network": {
                "stations_in_zone": station.get("count_in_zone"),
                "elevation_range_m": station.get("elevation_range_m"),
            },
            "internal_system1_verdict": {
                "primary_hazard": (dec.get("hazard_classification") or {}).get("primary_hazard"),
                "threat_status": (dec.get("threat_level") or {}).get("status"),
                "severe_risk_pct": (dec.get("severe_risk_binary") or {}).get("risk_probability_pct"),
                "flood_risk_pct": (dec.get("flood_risk") or {}).get("risk_probability_pct"),
                "aviation_safety_index": (dec.get("aviation_safety") or {}).get("safety_index"),
            },
            "internal_system1_briefing": dec.get("summary_briefing"),
        }

    @staticmethod
    def _questions(days_ahead: int) -> Dict[str, Any]:
        horizon = "the next 12 hours" if not days_ahead else ("day +%d of the forecast" % days_ahead)
        return {
            "condition": {
                "type": "choice",
                "instructions": "Dominant weather condition expected in this zone for %s" % horizon,
                "criteria": {
                    "clear": "clear or mainly clear sky",
                    "cloudy": "cloudy or overcast without significant precipitation",
                    "rain": "steady stratiform rain",
                    "showers": "showery or convective rain",
                    "storm": "thunderstorm or severe convection",
                    "snow": "snowfall",
                    "fog": "fog or very low visibility",
                    "wind": "dominant strong wind event",
                    "heat": "extreme heat dominance",
                    "mixed": "mixed or wintry mixed precipitation",
                },
            },
            "severity": {
                "type": "score",
                "instructions": "Overall severe weather severity for the zone and horizon",
                "criteria": ["benign", "minor", "moderate", "severe", "extreme"],
            },
            "storm_risk": {
                "type": "noul",
                "instructions": "Thunderstorm, supercell or severe convective risk for the horizon",
            },
            "precipitation_type": {
                "type": "choice",
                "instructions": "Expected precipitation type",
                "criteria": {
                    "none": "no precipitation",
                    "rain": "liquid rain",
                    "snow": "frozen snow",
                    "mixed": "mixed rain and snow",
                },
            },
            "flood_risk": {
                "type": "noul",
                "instructions": "Flash flood or excessive surface runoff risk",
            },
            "aviation": {
                "type": "choice",
                "instructions": "Operating conditions for aircraft and drones",
                "criteria": {
                    "go": "favorable, safe flight conditions",
                    "caution": "marginal, caution advised",
                    "nogo": "hazardous, flight operations not advised",
                },
            },
            "visibility": {
                "type": "choice",
                "instructions": "Prevailing visibility for ground operations",
                "criteria": {
                    "excellent": "more than 10 km",
                    "good": "5 to 10 km",
                    "moderate": "1 to 5 km",
                    "poor": "less than 1 km",
                },
            },
        }

    # --------------------------------------------------------------- http call
    async def _query_codiv(self, state: Dict[str, Any], questions: Dict[str, Any]) -> Dict[str, Any]:
        apikey = (load_keys().get("codiv_api_key") or "").strip()
        if not apikey:
            return {"status": "error", "error": "missing_api_key",
                    "detail": "codiv_api_key is not configured in the Secure Key Vault."}

        payload = {"model": OPENJEV_MODEL, "state": state, "questions": questions}
        headers = {"Authorization": "Bearer %s" % apikey, "Content-Type": "application/json"}
        timeout = httpx.Timeout(45.0, connect=10.0)
        delay = 1.0

        async with httpx.AsyncClient(timeout=timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    self.request_count += 1
                    r = await client.post(OPENJEV_BASE_URL + "/v1/systemone", headers=headers, json=payload)
                except Exception as e:
                    self.last_error = str(e)
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(delay); delay *= 2.0; continue
                    return {"status": "error", "error": "network", "detail": str(e)}

                if r.status_code == 200:
                    return {"status": "success", "raw": r.json()}

                # 429 / 529 -> exponential backoff, honouring retry-after
                if r.status_code in (429, 529) and attempt < self.max_retries - 1:
                    retry_after = r.headers.get("retry-after")
                    try:
                        wait = float(retry_after) if retry_after else delay
                    except Exception:
                        wait = delay
                    await asyncio.sleep(min(max(wait, 0.5), 8.0))
                    delay *= 2.0
                    continue

                self.last_error = "HTTP %s" % r.status_code
                return {"status": "error", "error": "HTTP %s" % r.status_code, "detail": r.text[:300]}

        return {"status": "error", "error": "retries_exhausted"}

    # --------------------------------------------------------------- transform
    @staticmethod
    def _to_visual(answers: Dict[str, Any]) -> Dict[str, Any]:
        def choice(q):
            a = answers.get(q) or {}
            return a.get("choice"), a.get("probabilities") or {}, a.get("confidence")

        def score(q):
            a = answers.get(q) or {}
            return a.get("score"), a.get("legend") or {}, a.get("probabilities") or {}, a.get("confidence")

        def noul(q):
            a = answers.get(q) or {}
            return a.get("noul")

        cond, cond_p, cond_conf = choice("condition")
        sev, sev_legend, sev_p, sev_conf = score("severity")
        prec, prec_p, _ = choice("precipitation_type")
        avia, avia_p, _ = choice("aviation")
        vis, vis_p, _ = choice("visibility")

        sev_label = None
        if sev is not None and sev_legend:
            idx = int(round(sev))
            sev_label = sev_legend.get(str(idx)) or sev_legend.get(idx)

        storm = noul("storm_risk")
        flood = noul("flood_risk")

        return {
            "dominant_condition": cond,
            "condition_color": CONDITION_COLORS.get(cond, "#38bdf8"),
            "condition_icon": CONDITION_ICONS.get(cond, "\U0001f321"),
            "condition_probabilities": cond_p,
            "condition_confidence": cond_conf,
            "severity_score": sev,
            "severity_label": sev_label,
            "severity_legend": sev_legend,
            "severity_probabilities": sev_p,
            "severity_confidence": sev_conf,
            "precipitation_type": prec,
            "precipitation_probabilities": prec_p,
            "storm_risk_pct": round((storm or 0.0) * 100.0, 1),
            "flood_risk_pct": round((flood or 0.0) * 100.0, 1),
            "aviation": avia,
            "aviation_probabilities": avia_p,
            "visibility": vis,
            "visibility_probabilities": vis_p,
        }

    # ----------------------------------------------------------------- public
    async def verdict(self, lat: Optional[float] = None, lon: Optional[float] = None,
                      radius_km: Optional[float] = None,
                      north: Optional[float] = None, south: Optional[float] = None,
                      east: Optional[float] = None, west: Optional[float] = None,
                      target_date: Optional[str] = None) -> Dict[str, Any]:
        """Visual weather prediction for the selected map sector via OpenJev 0.1."""
        t0 = time.time()

        cache_key = "openjev_%s_%s_%s_%s_%s_%s_%s" % (
            round(lat or 0.0, 3), round(lon or 0.0, 3),
            round(north or 0.0, 2), round(south or 0.0, 2),
            round(east or 0.0, 2), round(west or 0.0, 2),
            target_date or "today",
        )
        now = time.time()
        hit = self.cache.get(cache_key)
        if hit and now - hit["time"] < self.cache_ttl:
            return dict(hit["data"], cached=True)

        # 1. Reuse the classical Jev engine to assemble the fused meteorological state
        from backend.services.jev_engine import jev_engine
        jev = await jev_engine.predict_area_forecast(
            lat=lat, lon=lon, radius_km=radius_km,
            north=north, south=south, east=east, west=west, target_date=target_date
        )
        if not isinstance(jev, dict) or jev.get("status") != "success":
            return {"status": "error", "error": "jev_state_unavailable",
                    "detail": "Could not assemble the zone weather state for OpenJev."}

        state = self._build_state(jev)
        days_ahead = int((jev.get("target") or {}).get("days_ahead", 0) or 0)
        questions = self._questions(days_ahead)

        # 2. Ask OpenJev (System One) - one calibrated distribution per question
        resp = await self._query_codiv(state, questions)
        if resp.get("status") != "success":
            resp["target"] = jev.get("target")
            resp["state_summary"] = state
            return resp

        raw = resp["raw"]
        answers = raw.get("answers", {}) or {}
        result = {
            "status": "success",
            "engine": "OpenJev 0.1 (Codiv System One)",
            "mode": "visual_weather_prediction",
            "model": raw.get("model", "openjev-0.1"),
            "target": jev.get("target"),
            "state_summary": state,
            "ground_stations": jev.get("ground_stations", {}),
            "answers": answers,
            "visual": self._to_visual(answers),
            "usage": raw.get("usage", {}),
            "latency_ms": round((time.time() - t0) * 1000.0, 1),
            "quota_note": "Codiv public experiment: 100M System One tokens per account.",
        }
        self.cache[cache_key] = {"time": now, "data": result}
        return dict(result, cached=False)


openjev_engine = OpenJevEngine()
