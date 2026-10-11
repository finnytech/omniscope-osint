import urllib.request
import json

KEY = ""

# Test map clusters endpoint
url = "https://api.windy.com/webcams/api/v3/map/clusters?zoom=5&bbox=40,-10,60,30"
req = urllib.request.Request(url, headers={"x-windy-api-key": KEY, "User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    print("Clusters response keys:", list(data.keys()) if isinstance(data, dict) else len(data))
    print("Sample cluster data:", json.dumps(data, indent=2)[:500])
except Exception as e:
    print("Cluster endpoint error:", e)

# Test export all webcams json endpoint
export_url = "https://api.windy.com/webcams/export/all-webcams.json"
req2 = urllib.request.Request(export_url, headers={"x-windy-api-key": KEY, "User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req2, timeout=10) as resp:
        print("Export endpoint headers:", dict(resp.headers))
        first_chunk = resp.read(1000).decode('utf-8', errors='ignore')
        print("First chunk of export:", first_chunk[:300])
except Exception as e:
    print("Export error:", e)
