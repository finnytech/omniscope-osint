import os
import sys
import json
import ssl
import gzip
import urllib.request
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AuxStationsDownloader")

DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

ctx = ssl._create_unverified_context()

def download_file(url: str, filename: str, headers: dict = None):
    filepath = os.path.join(DOWNLOADS_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        logger.info(f"File already exists: {filename} ({os.path.getsize(filepath)} bytes)")
        return filepath
    
    logger.info(f"Downloading {url} -> {filename}...")
    req_headers = {"User-Agent": "CyberSpectreNexus/1.0"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = resp.read()
            with open(filepath, "wb") as f:
                f.write(data)
        logger.info(f"Successfully downloaded {filename} ({len(data)} bytes)")
        return filepath
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return None

def fetch_canada_stations():
    filepath = os.path.join(DOWNLOADS_DIR, "canada_stations.json")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100000:
        logger.info(f"Canada stations already downloaded ({os.path.getsize(filepath)} bytes)")
        return
    
    all_features = []
    limit = 1000
    offset = 0
    logger.info("Fetching Canada ECCC stations in batches...")
    while True:
        url = f"https://api.weather.gc.ca/collections/climate-stations/items?f=json&limit={limit}&offset={offset}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CyberSpectreNexus/1.0"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            features = data.get("features", [])
            if not features:
                break
            all_features.extend(features)
            logger.info(f"Canada ECCC fetched {len(all_features)} stations (offset {offset})...")
            if len(features) < limit:
                break
            offset += limit
        except Exception as e:
            logger.error(f"Error fetching Canada batch at offset {offset}: {e}")
            break
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(all_features, f)
    logger.info(f"Saved {len(all_features)} Canada stations to {filepath}")

def main():
    logger.info("Starting auxiliary station downloads...")
    # 1. Meteostat
    download_file("https://bulk.meteostat.net/v2/stations/full.json.gz", "meteostat_full.json.gz")
    
    # 2. Australia BOM
    download_file("http://www.bom.gov.au/climate/data/lists_by_element/stations.txt", "bom_stations.txt")
    
    # 3. NOAA NDBC Marine Buoys
    download_file("https://www.ndbc.noaa.gov/activestations.xml", "ndbc_stations.xml")
    
    # 4. NOAA CO-OPS Coastal Stations
    download_file("https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?type=met", "coops_stations.json")
    
    # 5. DWD CDC Germany
    download_file("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt", "dwd_kl_stations.txt")
    download_file("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/TU_Stundenwerte_Beschreibung_Stationen.txt", "dwd_tu_stations.txt")
    
    # 6. Canada ECCC
    fetch_canada_stations()

    logger.info("All auxiliary station downloads finished.")

if __name__ == "__main__":
    main()
