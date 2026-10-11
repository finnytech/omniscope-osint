#!/usr/bin/env python3
"""
OmniScope OSINT - Interactive Setup & Configuration Wizard
Initializes local SQLite databases and optionally configures third-party API keys.
Strict Zero-Fake Policy: Any skipped API key cleanly omits the provider from UI and backend.
"""

import os
import sys
import json
import sqlite3
import time

# Ensure safe console encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DATA = os.path.join(BASE_DIR, "backend", "data")
DB_PATH = os.path.join(BACKEND_DATA, "omniscope_spatial.db")
ENV_PATH = os.path.join(BASE_DIR, ".env")
VAULT_DB_PATH = os.path.join(BACKEND_DATA, "vault.db")

ASCII_BANNER = r"""
  ___  __  __ _  _ ___ ___  ___ ___  ___ ___ 
 / _ \|  \/  | \| |_ _/ __|/ __/ _ \| _ \ __|
| (_) | |\/| | .` || |\__ \ (_| (_) |  _/ _| 
 \___/|_|  |_|_|\_|___|___/\___\___/|_| |___|
       O P E N - S O U R C E   O S I N T
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("\033[96m" + ASCII_BANNER + "\033[0m")
    print("\033[90m=================================================================================\033[0m")
    print("\033[92m[+] 100% FREE & LEGAL OPEN SENSOR GRID // ZERO HARDCODED PRIVATE KEYS\033[0m")
    print("\033[90m=================================================================================\033[0m\n")

def init_sqlite_database():
    """Initializes local SQLite spatial database with indices and seed nodes."""
    os.makedirs(BACKEND_DATA, exist_ok=True)
    print("\033[93m[1/3] Initialisiere lokale SQLite Spatial-Datenbank (omniscope_spatial.db)...\033[0m")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA synchronous = NORMAL;")
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS weather_stations (
            id TEXT PRIMARY KEY,
            name TEXT,
            lat REAL,
            lon REAL,
            elevation REAL,
            country TEXT,
            payload TEXT
        );
    ''')
    cur.execute("CREATE INDEX IF NOT EXISTS idx_weather_spatial ON weather_stations(lat, lon);")
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cameras (
            id TEXT PRIMARY KEY,
            title TEXT,
            lat REAL,
            lon REAL,
            provider TEXT,
            stream_type TEXT,
            payload TEXT
        );
    ''')
    cur.execute("CREATE INDEX IF NOT EXISTS idx_camera_spatial ON cameras(lat, lon);")
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS system_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    ''')
    cur.execute("INSERT OR REPLACE INTO system_metadata (key, value) VALUES ('initialized_at', datetime('now'));")
    cur.execute("INSERT OR REPLACE INTO system_metadata (key, value) VALUES ('app_version', '2.0.0-oss');")
    
    # Check if seed weather stations exist
    cur.execute("SELECT COUNT(*) FROM weather_stations;")
    st_count = cur.fetchone()[0]
    
    ws_json = os.path.join(BACKEND_DATA, "weather_stations.json")
    if st_count == 0 and os.path.exists(ws_json):
        print(f"      Importiere Wetterstationen aus weather_stations.json...")
        try:
            with open(ws_json, "r", encoding="utf-8") as f:
                raw = json.load(f)
            items = raw if isinstance(raw, list) else raw.get("stations", [])
            batch = []
            for s in items:
                sid = s.get("id") or s.get("station_id")
                lat = s.get("lat")
                lon = s.get("lon")
                if not sid or lat is None or lon is None:
                    continue
                name = s.get("name", "Weather Station")
                elev = s.get("elevation", 0.0)
                cc = s.get("country", "")
                payload_str = json.dumps(s)
                batch.append((str(sid), str(name), float(lat), float(lon), float(elev), str(cc), payload_str))
            
            cur.executemany(
                "INSERT OR IGNORE INTO weather_stations (id, name, lat, lon, elevation, country, payload) VALUES (?, ?, ?, ?, ?, ?, ?);",
                batch
            )
            conn.commit()
            print(f"      \033[92m[✓] {len(batch):,} Bodenwetterstationen erfolgreich indexiert.\033[0m")
        except Exception as e:
            print(f"      \033[91m[!] Hinweis beim Importieren der Wetterstationen: {e}\033[0m")
    else:
        print(f"      \033[92m[✓] Wetterstations-Index bereit ({st_count:,} Stationen).\033[0m")

    # Check if seed cameras exist
    cur.execute("SELECT COUNT(*) FROM cameras;")
    cam_count = cur.fetchone()[0]

    cams_json = os.path.join(BACKEND_DATA, "cameras_db.json")
    if cam_count == 0 and os.path.exists(cams_json):
        print("      Importiere Webcams & Verkehrssensoren aus cameras_db.json...")
        try:
            with open(cams_json, "r", encoding="utf-8") as f:
                cams_list = json.load(f)
            batch = []
            for c in cams_list:
                cid = c.get("id")
                lat = c.get("lat")
                lon = c.get("lon")
                if not cid or lat is None or lon is None:
                    continue
                title = c.get("title", "Camera")
                prov = c.get("provider", "OSINT")
                stype = c.get("stream_type", "image")
                batch.append((str(cid), str(title), float(lat), float(lon), str(prov), str(stype), json.dumps(c)))
                if len(batch) >= 20000:
                    cur.executemany("INSERT OR IGNORE INTO cameras (id, title, lat, lon, provider, stream_type, payload) VALUES (?, ?, ?, ?, ?, ?, ?);", batch)
                    conn.commit()
                    batch = []
            if batch:
                cur.executemany("INSERT OR IGNORE INTO cameras (id, title, lat, lon, provider, stream_type, payload) VALUES (?, ?, ?, ?, ?, ?, ?);", batch)
                conn.commit()
            cur.execute("SELECT COUNT(*) FROM cameras;")
            cam_count = cur.fetchone()[0]
            cur.execute("INSERT OR REPLACE INTO system_metadata (key, value) VALUES ('total_cameras', ?);", (str(cam_count),))
            cur.execute("INSERT OR REPLACE INTO system_metadata (key, value) VALUES ('real_cameras', ?);", (str(cam_count),))
            conn.commit()
            print(f"      \033[92m[✓] {cam_count:,} Webcams & Verkehrssensoren erfolgreich indexiert.\033[0m")
        except Exception as e:
            print(f"      \033[91m[!] Hinweis beim Importieren der Kameras: {e}\033[0m")
    else:
        print(f"      \033[92m[✓] Webcam-Index bereit ({cam_count:,} Kameras).\033[0m")
        
    conn.commit()
    conn.close()

def prompt_optional_keys():
    """Interactive guided terminal prompt for optional API keys."""
    print("\n\033[93m[2/3] Konfiguration optionaler Drittanbieter-Keys (Zero-Fake Richtlinie)\033[0m")
    print("      OmniScope OSINT funktioniert vollständig mit freien, quelloffenen Feeds:")
    print("      \033[92m✓\033[0m 105,000+ Öffentliche Webcams & Verkehrskameras (Weltweit)")
    print("      \033[92m✓\033[0m 140+ Wetter-Supercomputer (DWD ICON, NOAA GFS, ECMWF IFS via Open-Meteo)")
    print("      \033[92m✓\033[0m Live RainViewer Doppler-Niederschlagsradar")
    print("      \033[92m✓\033[0m NOAA NEXRAD Dual-Pol Doppler-Radar & Unwetterwarnungen")
    print("      \033[92m✓\033[0m USGS Globale Echtzeit-Erdbeben")
    print("      \033[92m✓\033[0m Digitraffic AIS Schiffs-Tracking")
    print("      \033[92m✓\033[0m Europäischer Bahnverkehr & Hubs")
    print("      \033[92m✓\033[0m ISS Raumstations-Tracker & NASA HD Earth Cam\n")
    print("      \033[94mOptionale Provider können für zusätzliche Feeds aktiviert werden.\033[0m")
    print("      \033[90mHinweis: Wenn du einen Key überspringst, wird der Provider sauber aus der UI entfernt (Keine Fake-Daten!).\033[0m\n")
    
    existing_env = {}
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        existing_env[k.strip()] = v.strip().strip("'\"")
        except Exception:
            pass

    if "--auto" in sys.argv or "--non-interactive" in sys.argv or not sys.stdin.isatty():
        configure = "n"
    else:
        try:
            configure = input("\033[97mMöchtest du jetzt optionale API-Keys eingeben? [j/N]: \033[0m").strip().lower()
        except (EOFError, KeyboardInterrupt):
            configure = "n"
    
    keys = {
        "NVIDIA_NIM_KEY": existing_env.get("NVIDIA_NIM_KEY", ""),
        "OPENSKY_USERNAME": existing_env.get("OPENSKY_USERNAME", ""),
        "OPENSKY_PASSWORD": existing_env.get("OPENSKY_PASSWORD", ""),
        "TOMORROW_API_KEY": existing_env.get("TOMORROW_API_KEY", ""),
        "FIRMS_MAP_KEY": existing_env.get("FIRMS_MAP_KEY", ""),
        "AIRNOW_API_KEY": existing_env.get("AIRNOW_API_KEY", ""),
        "OPENROUTESERVICE_KEY": existing_env.get("OPENROUTESERVICE_KEY", ""),
    }

    if configure in ("j", "ja", "y", "yes"):
        print("\n\033[90m---------------------------------------------------------------------------------\033[0m")
        print("\033[96m1. NVIDIA NIM (KI-Reasoning & Diffusion-Wettermodelle)\033[0m")
        print("   Kostenlos: 1,000 Credits bei https://build.nvidia.com/")
        curr = keys["NVIDIA_NIM_KEY"]
        prompt_txt = f"   Key eingeben [{curr[:8]}...]: " if curr else "   Key eingeben (oder Enter zum Überspringen): "
        val = input(prompt_txt).strip()
        if val: keys["NVIDIA_NIM_KEY"] = val

        print("\n\033[96m2. OpenSky Network (Echtzeit ADS-B Flugzeug-Transponder)\033[0m")
        print("   Kostenloser Community-Account: https://opensky-network.org/")
        curr_u = keys["OPENSKY_USERNAME"]
        prompt_txt = f"   OpenSky Benutzername [{curr_u}]: " if curr_u else "   OpenSky Benutzername (oder Enter zum Überspringen): "
        val = input(prompt_txt).strip()
        if val: keys["OPENSKY_USERNAME"] = val

        if keys["OPENSKY_USERNAME"]:
            val_p = input("   OpenSky Passwort: ").strip()
            if val_p: keys["OPENSKY_PASSWORD"] = val_p

        print("\n\033[96m3. Tomorrow.io (Lokale Mikroklima- & Luftqualitätssensoren)\033[0m")
        print("   Kostenloser Free-Tier Key: https://www.tomorrow.io/")
        curr = keys["TOMORROW_API_KEY"]
        prompt_txt = f"   Key eingeben [{curr[:8]}...]: " if curr else "   Key eingeben (oder Enter zum Überspringen): "
        val = input(prompt_txt).strip()
        if val: keys["TOMORROW_API_KEY"] = val

        print("\n\033[96m4. NASA FIRMS (VIP Aktive Waldbrand-Satelliten-Hotspots)\033[0m")
        print("   Kostenloser Map-Key: https://firms.modaps.eosdis.nasa.gov/api/map_key")
        curr = keys["FIRMS_MAP_KEY"]
        prompt_txt = f"   Key eingeben [{curr[:8]}...]: " if curr else "   Key eingeben (oder Enter zum Überspringen): "
        val = input(prompt_txt).strip()
        if val: keys["FIRMS_MAP_KEY"] = val

        print("\n\033[96m5. AirNow EPA (US Luftqualitäts-Messnetzwerk AQI)\033[0m")
        print("   Kostenlos: https://docs.airnowapi.org/")
        curr = keys["AIRNOW_API_KEY"]
        prompt_txt = f"   Key eingeben [{curr[:8]}...]: " if curr else "   Key eingeben (oder Enter zum Überspringen): "
        val = input(prompt_txt).strip()
        if val: keys["AIRNOW_API_KEY"] = val

        print("\n\033[96m6. OpenRouteService (Geocoding & Matrix-Routing)\033[0m")
        print("   Kostenloser Token: https://openrouteservice.org/")
        curr = keys["OPENROUTESERVICE_KEY"]
        prompt_txt = f"   Key eingeben [{curr[:8]}...]: " if curr else "   Key eingeben (oder Enter zum Überspringen): "
        val = input(prompt_txt).strip()
        if val: keys["OPENROUTESERVICE_KEY"] = val

    return keys

def save_configuration(keys):
    """Writes configured keys to .env and SQLite vault."""
    print("\n\033[93m[3/3] Speichere Konfiguration...\033[0m")
    
    # 1. Write to .env
    lines = [
        "# OmniScope OSINT - Configuration",
        "# Generated automatically via setup_wizard.py",
        "# Strict Zero-Fake Policy: Absent keys omit providers cleanly from UI and backend.",
        "",
    ]
    for k, v in keys.items():
        lines.append(f"{k}={v}")
    
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"      \033[92m[✓] Konfiguration in .env gespeichert.\033[0m")

    # 2. Sync to backend vault.db
    try:
        from backend.config import save_keys as persist_vault
        vault_dict = {
            "nvidia_nim_key": keys.get("NVIDIA_NIM_KEY", ""),
            "opensky_client_id": keys.get("OPENSKY_USERNAME", ""),
            "opensky_client_secret": keys.get("OPENSKY_PASSWORD", ""),
            "tomorrow_api_key": keys.get("TOMORROW_API_KEY", ""),
            "firms_map_key": keys.get("FIRMS_MAP_KEY", ""),
            "airnow_api_key": keys.get("AIRNOW_API_KEY", ""),
            "openrouteservice_key": keys.get("OPENROUTESERVICE_KEY", ""),
        }
        persist_vault(vault_dict)
        print(f"      \033[92m[✓] Lokaler SQLite Vault (vault.db) synchronisiert.\033[0m")
    except Exception as e:
        print(f"      \033[90m(Vault sync notice: {e})\033[0m")

def print_summary(keys):
    print("\n\033[90m=================================================================================\033[0m")
    print("\033[92mOMNISCOPE OSINT - STATUSBERICHT (ZERO FAKES):\033[0m")
    print("\033[90m=================================================================================\033[0m")
    
    print("\033[97mStandard Open-Source Feeds (Aktiv):\033[0m")
    print("  [✓] 105,000+ Kameras & Webcams        [✓] 140+ Wetter-Supercomputer")
    print("  [✓] RainViewer Doppler-Radar          [✓] NOAA NEXRAD Doppler & Alerts")
    print("  [✓] USGS Globale Erdbeben             [✓] Digitraffic AIS Schiffsverkehr")
    print("  [✓] Europäischer Bahnverkehr          [✓] ISS Live Tracker & NASA Earth Cam\n")
    
    print("\033[97mOptionale Feeds:\033[0m")
    for name, k_name in [
        ("NVIDIA NIM KI-Reasoning", "NVIDIA_NIM_KEY"),
        ("OpenSky ADS-B Flugtransponder", "OPENSKY_USERNAME"),
        ("Tomorrow.io Mikroklima/Luft", "TOMORROW_API_KEY"),
        ("NASA FIRMS VIP Waldbrände", "FIRMS_MAP_KEY"),
        ("AirNow EPA Luftqualitäts-AQI", "AIRNOW_API_KEY"),
        ("OpenRouteService Routing", "OPENROUTESERVICE_KEY")
    ]:
        val = keys.get(k_name, "")
        if val:
            print(f"  \033[92m[AKTIV]\033[0m   {name}")
        else:
            print(f"  \033[90m[OMITTED] {name} (Nicht in UI angezeigt, keine Fake-Calls)\033[0m")

    print("\n\033[92m[✓] Setup vollständig abgeschlossen!\033[0m")
    print("Starte den Server mit: \033[96mstart.bat\033[0m oder \033[96mpython run_server.py\033[0m\n")

def main():
    clear_screen()
    print_banner()
    init_sqlite_database()
    keys = prompt_optional_keys()
    save_configuration(keys)
    print_summary(keys)

if __name__ == "__main__":
    main()
