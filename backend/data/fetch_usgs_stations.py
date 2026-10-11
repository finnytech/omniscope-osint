import urllib.request
import json
import os
import concurrent.futures

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads", "usgs_stations.json")
if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 500000:
    print(f"USGS stations already fetched ({os.path.getsize(OUTPUT_FILE)} bytes).")
    exit(0)

# 50 US states
states = [
    'al','ak','az','ar','ca','co','ct','de','fl','ga',
    'hi','id','il','in','ia','ks','ky','la','me','md',
    'ma','mi','mn','ms','mo','mt','ne','nv','nh','nj',
    'nm','ny','nc','nd','oh','ok','or','pa','ri','sc',
    'sd','tn','tx','ut','vt','va','wa','wv','wi','wy'
]

def fetch_state(st):
    url = f"https://waterservices.usgs.gov/nwis/site/?format=rdb&siteType=ST,LK,SP,AT&siteStatus=active&stateCd={st}"
    results = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CyberSpectreNexus/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            lines = r.read().decode('utf-8', errors='ignore').splitlines()
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split('\t')
            # Format: agency_cd, site_no, station_nm, site_tp_cd, dec_lat_va, dec_long_va, coord_meth_cd, coord_acy_cd, coord_datum_cd, dec_coord_datum_cd, district_cd, state_cd, county_cd, country_cd, land_net_ds, map_nm, map_scale_fc, alt_va, alt_meth_cd, alt_acy_va, alt_datum_cd, huc_cd
            if len(parts) >= 6 and parts[0] == 'USGS':
                try:
                    site_id = parts[1].strip()
                    name = parts[2].strip()
                    lat = float(parts[4])
                    lon = float(parts[5])
                    alt = float(parts[17]) if len(parts) > 17 and parts[17].strip() else 0.0
                    alt_m = round(alt * 0.3048, 1)
                    if lat != 0.0 and lon != 0.0:
                        results.append({
                            "id": f"usgs_{site_id}",
                            "name": name,
                            "lat": round(lat, 4),
                            "lon": round(lon, 4),
                            "elevation": alt_m,
                            "state": st.upper()
                        })
                except Exception:
                    continue
        print(f"USGS {st.upper()}: {len(results)} stations")
        return results
    except Exception as e:
        print(f"USGS {st.upper()} error: {e}")
        return []

all_usgs = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_state, st) for st in states]
    for f in concurrent.futures.as_completed(futures):
        all_usgs.extend(f.result())

print(f"Total USGS stations collected: {len(all_usgs)}")
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(all_usgs, out)
print(f"Saved to {OUTPUT_FILE}")
