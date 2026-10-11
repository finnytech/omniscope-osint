import urllib.request
import json
import time

KEY = ""
countries = ['US', 'DE', 'AT', 'CH', 'FR', 'IT', 'JP', 'AU', 'CA', 'NO', 'SE', 'IS', 'ES', 'NZ', 'GB']
total = 0

for c in countries:
    url = f"https://api.windy.com/webcams/api/v3/webcams?countries={c}&limit=50&include=player,images,location"
    req = urllib.request.Request(url, headers={"x-windy-api-key": KEY, "User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            count = len(data.get("webcams", []))
            total += count
            print(f"{c}: {count} cams (country total: {data.get('total')})")
    except Exception as e:
        print(f"{c} error: {e}")
    time.sleep(0.1)

print(f"Total fetched from test countries: {total}")
