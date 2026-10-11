"""
OmniScope OSINT: Central Configuration & Secure Credentials Vault
Implements zero-mock policy: if an API key is absent, the provider is completely
omitted from the UI and backend routines without synthetic fallbacks.
"""

import os
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

def _load_env_file():
    """Lightweight zero-dependency .env reader."""
    if not os.path.exists(ENV_FILE):
        return
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass

_load_env_file()

from backend.services.vault import (
    get_vault_key,
    set_vault_key,
    get_all_vault_keys,
    delete_vault_key,
    VAULT_DB_PATH
)

KEY_ENV_MAPPINGS = {
    "nvidia_nim_key": ["NVIDIA_NIM_KEY", "NVIDIA_API_KEY", "NIM_API_KEY"],
    "opensky_client_id": ["OPENSKY_CLIENT_ID", "OPENSKY_USERNAME", "OPENSKY_USER"],
    "opensky_client_secret": ["OPENSKY_CLIENT_SECRET", "OPENSKY_PASSWORD"],
    "tomorrow_api_key": ["TOMORROW_API_KEY", "TOMORROW_IO_KEY"],
    "firms_map_key": ["FIRMS_MAP_KEY", "NASA_FIRMS_KEY"],
    "airnow_api_key": ["AIRNOW_API_KEY"],
    "openrouteservice_key": ["OPENROUTESERVICE_KEY", "ORS_KEY"],
    "codiv_api_key": ["CODIV_API_KEY"],
    "mapbox_token": ["MAPBOX_TOKEN", "MAPBOX_API_KEY"],
}

def get_key(name: str, default: str = "") -> str:
    """
    Retrieves key from vault.db first, falling back to environment variables / .env.
    """
    val = get_vault_key(name)
    if val:
        return val.strip()
    # Check env mappings
    env_vars = KEY_ENV_MAPPINGS.get(name, [name.upper()])
    for ev in env_vars:
        ev_val = os.environ.get(ev)
        if ev_val and ev_val.strip():
            return ev_val.strip()
    return default

def load_keys() -> Dict[str, str]:
    """Retrieves all active API keys and tokens."""
    vault_keys = get_all_vault_keys()
    merged = dict(vault_keys)
    for canonical_name, env_names in KEY_ENV_MAPPINGS.items():
        if canonical_name not in merged or not merged[canonical_name]:
            for ev in env_names:
                v = os.environ.get(ev)
                if v and v.strip():
                    merged[canonical_name] = v.strip()
                    break
    return merged

def save_keys(updated_keys: Dict[str, str]) -> Dict[str, str]:
    """Persists API keys into the SQLite 3 vault and updates active environment."""
    for k, v in updated_keys.items():
        if v is not None:
            clean_v = str(v).strip()
            set_vault_key(k, clean_v, "Configured via OmniScope OSINT Wizard")
            # Also update os.environ for instant runtime reflection
            env_vars = KEY_ENV_MAPPINGS.get(k, [k.upper()])
            for ev in env_vars:
                os.environ[ev] = clean_v
    return load_keys()

def get_capabilities() -> Dict[str, Any]:
    """
    Reports exact capabilities based on key presence.
    Zero-fake policy: features with missing keys are marked active=False and omitted.
    """
    keys = load_keys()
    
    keyed_providers = {
        "opensky_flights": bool(keys.get("opensky_client_id") and keys.get("opensky_client_secret")),
        "nvidia_nim": bool(keys.get("nvidia_nim_key")),
        "tomorrow_io": bool(keys.get("tomorrow_api_key")),
        "nasa_firms_vip": bool(keys.get("firms_map_key")),
        "airnow_epa": bool(keys.get("airnow_api_key")),
        "openrouteservice": bool(keys.get("openrouteservice_key")),
        "codiv_cloud": bool(keys.get("codiv_api_key")),
    }
    
    open_features = {
        "public_webcams": True,
        "weather_stations_spatial": True,
        "rainviewer_doppler": True,
        "noaa_nexrad_doppler": True,
        "usgs_earthquakes": True,
        "open_meteo_consensus": True,
        "digitraffic_maritime_ais": True,
        "european_transit_trains": True,
        "iss_orbital_tracker": True,
        "space_weather_solar": True,
        "panoramic_webcam_grid": True,
    }
    
    active_keyed = [p for p, active in keyed_providers.items() if active]
    omitted_keyed = [p for p, active in keyed_providers.items() if not active]
    
    return {
        "app_name": "OmniScope OSINT",
        "version": "2.0.0-oss",
        "zero_fake_policy": True,
        "open_features": open_features,
        "keyed_providers": keyed_providers,
        "active_keyed_count": len(active_keyed),
        "omitted_keyed_count": len(omitted_keyed),
        "active_keyed_list": active_keyed,
        "omitted_keyed_list": omitted_keyed,
    }
