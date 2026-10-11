"""
CyberSpectreNexus - Master 300k+ Weather Stations Compiler
Combines 10+ official open-data meteorological agencies:
1. NOAA GHCN-Daily (132k+ global surface & climate stations)
2. OurAirports Global METAR (72k+ worldwide aviation weather stations)
3. NOAA ISD History / WMO (29k+ synoptic weather stations)
4. Meteostat Global Directory (22k+ international climate stations)
5. Australian Bureau of Meteorology - BOM (19k+ automated weather stations)
6. USGS Hydrological & Atmospheric Network (16k+ observation sites)
7. Environment and Climate Change Canada - ECCC (8.4k+ climate stations)
8. Deutscher Wetterdienst - DWD Germany (2.5k+ high-precision climate stations)
9. NOAA NDBC (1.3k+ oceanic data buoys)
10. NOAA CO-OPS (315 coastal meteorological observatories)
11. CyberSpectre Severe Storm Intercept Posts (12k+ storm chasers & radars)
"""

import os
import sys
import json
import csv
import gzip
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WeatherStationsCompiler")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, ".cache")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
OUTPUT_FILE = os.path.join(BASE_DIR, "weather_stations.json")

CONTINENT_MAP = {
    "NA": "North America",
    "EU": "Europe",
    "AS": "Asia",
    "AF": "Africa",
    "SA": "South America",
    "OC": "Oceania",
    "AN": "Antarctica"
}

def load_country_lookup():
    countries_file = os.path.join(CACHE_DIR, "countries.csv")
    lookup = {}
    if os.path.exists(countries_file):
        with open(countries_file, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                code = row["code"].strip().upper()
                c_name = row["name"].strip()
                cont_code = row["continent"].strip().upper()
                cont_name = CONTINENT_MAP.get(cont_code, "Global")
                lookup[code] = (c_name, cont_name)
    return lookup

def coords_to_continent(lat, lon):
    if lat > 20 and -130 < lon < -50:
        return "North America"
    elif -60 < lat < 15 and -85 < lon < -30:
        return "South America"
    elif lat > 35 and -15 < lon < 45:
        return "Europe"
    elif -35 < lat < 38 and -20 < lon < 55:
        return "Africa"
    elif lat > 0 and 45 < lon < 150:
        return "Asia"
    elif lat < -10 and 110 < lon < 180:
        return "Oceania"
    elif lat < -60:
        return "Antarctica"
    return "Global"

def compile_stations():
    country_lookup = load_country_lookup()
    seen_ids = set()
    stations = []

    def add_station(s_id, name, country, continent, lat, lon, elev, s_type, provider):
        if not s_id or s_id in seen_ids:
            return False
        try:
            lat = round(float(lat), 4)
            lon = round(float(lon), 4)
            elev = round(float(elev), 1) if elev is not None else 0.0
        except (ValueError, TypeError):
            return False
        
        if lat < -90.0 or lat > 90.0 or lon < -180.0 or lon > 180.0:
            return False
        if lat == 0.0 and lon == 0.0:
            return False
        
        seen_ids.add(s_id)
        stations.append({
            "id": s_id,
            "name": name.strip(),
            "country": country.strip() if country else "Global",
            "continent": continent.strip() if continent else coords_to_continent(lat, lon),
            "lat": lat,
            "lon": lon,
            "elevation": elev,
            "type": s_type,
            "provider": provider
        })
        return True

    # 1. Existing stations (Storm chasers, severe hubs)
    orig_file = os.path.join(BASE_DIR, "weather_stations.json")
    if os.path.exists(orig_file):
        try:
            with open(orig_file, "r", encoding="utf-8") as f:
                orig_data = json.load(f)
            count = 0
            for s in orig_data:
                if add_station(s["id"], s["name"], s.get("country", ""), s.get("continent", ""), s["lat"], s["lon"], s.get("elevation", 0), s.get("type", "storm_chaser_post"), s.get("provider", "CyberSpectre Tactical")):
                    count += 1
            logger.info(f"Loaded {count} existing stations / storm chaser posts.")
        except Exception as e:
            logger.error(f"Error loading existing stations: {e}")

    # 2. NOAA GHCN-Daily
    ghcn_file = os.path.join(DOWNLOADS_DIR, "ghcnd-stations.txt")
    if os.path.exists(ghcn_file):
        logger.info("Ingesting NOAA GHCN-Daily stations...")
        count = 0
        with open(ghcn_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if len(line) < 38:
                    continue
                st_id = f"ghcn_{line[0:11].strip()}"
                try:
                    lat = float(line[12:20])
                    lon = float(line[21:30])
                    elev_str = line[31:37].strip()
                    elev = float(elev_str) if elev_str and elev_str != "-999.9" else 0.0
                except ValueError:
                    continue
                
                raw_name = line[41:71].strip()
                name = raw_name.title() if raw_name else f"GHCN {line[0:11].strip()}"
                cc = line[0:2].upper()
                c_info = country_lookup.get(cc)
                country = c_info[0] if c_info else "Global"
                continent = c_info[1] if c_info else coords_to_continent(lat, lon)
                
                if add_station(st_id, name, country, continent, lat, lon, elev, "ghcn", "NOAA NCEI"):
                    count += 1
        logger.info(f"Ingested {count} NOAA GHCN-Daily stations.")

    # 3. OurAirports Global Aviation METAR
    airports_file = os.path.join(CACHE_DIR, "airports.csv")
    if os.path.exists(airports_file):
        logger.info("Ingesting OurAirports aviation METAR weather stations...")
        count = 0
        with open(airports_file, "r", encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f):
                if row.get("type") == "closed":
                    continue
                ident = row.get("ident", "").strip()
                if not ident:
                    continue
                st_id = f"metar_{ident.lower()}"
                try:
                    lat = float(row["latitude_deg"])
                    lon = float(row["longitude_deg"])
                    elev_ft = row.get("elevation_ft", "")
                    elev_m = round(float(elev_ft) * 0.3048, 1) if elev_ft else 0.0
                except (ValueError, KeyError):
                    continue
                
                name = row.get("name", f"Airport {ident}").strip()
                iso_c = row.get("iso_country", "").strip().upper()
                c_info = country_lookup.get(iso_c)
                country = c_info[0] if c_info else iso_c
                cont_code = row.get("continent", "").strip().upper()
                continent = CONTINENT_MAP.get(cont_code, coords_to_continent(lat, lon))

                if add_station(st_id, name, country, continent, lat, lon, elev_m, "airport_metar", "OurAirports METAR"):
                    count += 1
        logger.info(f"Ingested {count} airport METAR weather stations.")

    # 4. NOAA ISD History / WMO
    isd_file = os.path.join(CACHE_DIR, "isd-history.csv")
    if os.path.exists(isd_file):
        logger.info("Ingesting NOAA ISD synoptic weather stations...")
        count = 0
        with open(isd_file, "r", encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f):
                usaf = row.get("USAF", "").strip()
                wban = row.get("WBAN", "").strip()
                icao = row.get("ICAO", "").strip().upper()
                st_id = f"isd_{usaf}_{wban}" if usaf != "999999" else f"isd_{icao}"
                if not usaf or usaf == "000000":
                    continue
                try:
                    lat = float(row["LAT"])
                    lon = float(row["LON"])
                    elev_str = row.get("ELEV(M)", "")
                    elev = float(elev_str) if elev_str else 0.0
                except (ValueError, KeyError):
                    continue
                
                raw_name = row.get("STATION NAME", "").strip()
                name = raw_name.title() if raw_name else f"ISD Station {usaf}"
                ctry = row.get("CTRY", "").strip().upper()
                c_info = country_lookup.get(ctry)
                country = c_info[0] if c_info else ctry
                continent = c_info[1] if c_info else coords_to_continent(lat, lon)

                if add_station(st_id, name, country, continent, lat, lon, elev, "wmo", "NOAA ISD"):
                    count += 1
        logger.info(f"Ingested {count} NOAA ISD synoptic stations.")

    # 5. Meteostat Global Directory
    meteostat_file = os.path.join(DOWNLOADS_DIR, "meteostat_full.json.gz")
    if os.path.exists(meteostat_file):
        logger.info("Ingesting Meteostat global stations...")
        count = 0
        try:
            with gzip.open(meteostat_file, "rt", encoding="utf-8") as f:
                data = json.load(f)
            for s in data:
                st_id = f"meteostat_{s['id'].lower()}"
                loc = s.get("location", {})
                lat = loc.get("latitude")
                lon = loc.get("longitude")
                elev = loc.get("elevation", 0.0)
                if lat is None or lon is None:
                    continue
                name_obj = s.get("name", {})
                name = name_obj.get("en") or name_obj.get("de") or list(name_obj.values())[0] if name_obj else f"Station {s['id']}"
                cc = s.get("country", "").upper()
                c_info = country_lookup.get(cc)
                country = c_info[0] if c_info else cc
                continent = c_info[1] if c_info else coords_to_continent(lat, lon)

                if add_station(st_id, name, country, continent, lat, lon, elev, "meteostat", "Meteostat"):
                    count += 1
            logger.info(f"Ingested {count} Meteostat stations.")
        except Exception as e:
            logger.error(f"Error ingesting Meteostat: {e}")

    # 6. Australian Bureau of Meteorology (BOM)
    bom_file = os.path.join(DOWNLOADS_DIR, "bom_stations.txt")
    if os.path.exists(bom_file):
        logger.info("Ingesting Australian Bureau of Meteorology (BOM) stations...")
        count = 0
        with open(bom_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f.readlines()[4:]:
                parts = line.split()
                if len(parts) >= 8 and parts[0].isdigit():
                    site = parts[0]
                    st_id = f"bom_{site}"
                    name = " ".join(parts[2:-8]).title() if len(parts) > 10 else f"Station {site}"
                    try:
                        lat = float(parts[-7])
                        lon = float(parts[-6])
                        h_str = parts[-3]
                        elev = float(h_str) if h_str != ".." else 0.0
                    except (ValueError, IndexError):
                        continue

                    if add_station(st_id, name, "Australia", "Oceania", lat, lon, elev, "bom_aws", "Australia BOM"):
                        count += 1
        logger.info(f"Ingested {count} Australia BOM stations.")

    # 7. USGS Hydrological & Atmospheric Network
    usgs_file = os.path.join(DOWNLOADS_DIR, "usgs_stations.json")
    if os.path.exists(usgs_file):
        logger.info("Ingesting USGS observation stations...")
        count = 0
        try:
            with open(usgs_file, "r", encoding="utf-8") as f:
                usgs_data = json.load(f)
            for s in usgs_data:
                if add_station(s["id"], s["name"], "United States", "North America", s["lat"], s["lon"], s.get("elevation", 0), "usgs_gauge", "USGS"):
                    count += 1
            logger.info(f"Ingested {count} USGS stations.")
        except Exception as e:
            logger.error(f"Error ingesting USGS: {e}")

    # 8. Environment and Climate Change Canada (ECCC)
    canada_file = os.path.join(DOWNLOADS_DIR, "canada_stations.json")
    if os.path.exists(canada_file):
        logger.info("Ingesting Canada ECCC climate stations...")
        count = 0
        try:
            with open(canada_file, "r", encoding="utf-8") as f:
                canada_data = json.load(f)
            for feat in canada_data:
                props = feat.get("properties", {})
                geom = feat.get("geometry", {})
                coords = geom.get("coordinates", [])
                if len(coords) < 2:
                    continue
                lon, lat = coords[0], coords[1]
                cid = props.get("CLIMATE_IDENTIFIER") or props.get("STATION_ID")
                st_id = f"eccc_{cid}"
                name = props.get("STN_NAME", f"Station {cid}").title()
                elev = props.get("ELEVATION", 0.0)

                if add_station(st_id, name, "Canada", "North America", lat, lon, elev, "eccc_climate", "Environment Canada"):
                    count += 1
            logger.info(f"Ingested {count} Canada ECCC stations.")
        except Exception as e:
            logger.error(f"Error ingesting Canada ECCC: {e}")

    # 9. Deutscher Wetterdienst (DWD)
    for dwd_name in ["dwd_kl_stations.txt", "dwd_tu_stations.txt"]:
        dwd_path = os.path.join(DOWNLOADS_DIR, dwd_name)
        if os.path.exists(dwd_path):
            logger.info(f"Ingesting DWD stations from {dwd_name}...")
            count = 0
            with open(dwd_path, "r", encoding="latin-1", errors="ignore") as f:
                for line in f:
                    if len(line) < 70 or line.startswith("Stat") or line.startswith("-"):
                        continue
                    sid = line[0:5].strip()
                    if not sid.isdigit():
                        continue
                    st_id = f"dwd_{sid}"
                    try:
                        elev = float(line[24:38].strip())
                        lat = float(line[39:50].strip())
                        lon = float(line[51:60].strip())
                    except ValueError:
                        continue
                    name = line[61:101].strip().title()
                    if add_station(st_id, name, "Germany", "Europe", lat, lon, elev, "dwd_climate", "DWD Germany"):
                        count += 1
            logger.info(f"Ingested {count} DWD stations from {dwd_name}.")

    # 10. NOAA NDBC Marine Buoys
    ndbc_file = os.path.join(DOWNLOADS_DIR, "ndbc_stations.xml")
    if os.path.exists(ndbc_file):
        logger.info("Ingesting NOAA NDBC marine buoy stations...")
        count = 0
        try:
            tree = ET.parse(ndbc_file)
            root = tree.getroot()
            for elem in root.findall("station"):
                bid = elem.get("id")
                if not bid:
                    continue
                st_id = f"ndbc_{bid}"
                name = elem.get("name", f"Buoy {bid}").title()
                try:
                    lat = float(elem.get("lat"))
                    lon = float(elem.get("lon"))
                except (ValueError, TypeError):
                    continue
                if add_station(st_id, name, "Oceanic / Offshore", coords_to_continent(lat, lon), lat, lon, 0.0, "marine_buoy", "NOAA NDBC"):
                    count += 1
            logger.info(f"Ingested {count} NOAA NDBC marine buoys.")
        except Exception as e:
            logger.error(f"Error ingesting NDBC: {e}")

    # 11. NOAA CO-OPS Coastal Meteorological Stations
    coops_file = os.path.join(DOWNLOADS_DIR, "coops_stations.json")
    if os.path.exists(coops_file):
        logger.info("Ingesting NOAA CO-OPS coastal stations...")
        count = 0
        try:
            with open(coops_file, "r", encoding="utf-8") as f:
                coops_data = json.load(f)
            for s in coops_data.get("stations", []):
                sid = s.get("id")
                if not sid:
                    continue
                st_id = f"coops_{sid}"
                name = s.get("name", f"CO-OPS {sid}").title()
                try:
                    lat = float(s.get("lat"))
                    lon = float(s.get("lng"))
                except (ValueError, TypeError):
                    continue
                if add_station(st_id, name, "United States", "North America", lat, lon, 0.0, "coastal_station", "NOAA CO-OPS"):
                    count += 1
            logger.info(f"Ingested {count} NOAA CO-OPS stations.")
        except Exception as e:
            logger.error(f"Error ingesting CO-OPS: {e}")

    total_count = len(stations)
    logger.info(f"=== COMPILATION COMPLETE: {total_count} TOTAL UNIQUE WEATHER STATIONS ===")
    
    # Save compact JSON
    logger.info(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(stations, f, separators=(',', ':'))
    
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    logger.info(f"Successfully saved {total_count} stations ({file_size_mb:.2f} MB) to {OUTPUT_FILE}")

    # Breakdown statistics
    types_count = {}
    continents_count = {}
    providers_count = {}
    for s in stations:
        t = s["type"]
        c = s["continent"]
        p = s["provider"]
        types_count[t] = types_count.get(t, 0) + 1
        continents_count[c] = continents_count.get(c, 0) + 1
        providers_count[p] = providers_count.get(p, 0) + 1

    print("\n================== 300K+ WEATHER STATIONS MASTER AUDIT ==================")
    print(f"TOTAL VERIFIED STATIONS: {total_count:,}")
    print(f"\n--- BREAKDOWN BY PROVIDER ---")
    for p, c in sorted(providers_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {p}: {c:,}")
    print(f"\n--- BREAKDOWN BY CONTINENT ---")
    for cont, c in sorted(continents_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cont}: {c:,}")
    print(f"\n--- BREAKDOWN BY TYPE ---")
    for t, c in sorted(types_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {t}: {c:,}")
    print("=========================================================================\n")

if __name__ == "__main__":
    compile_stations()
