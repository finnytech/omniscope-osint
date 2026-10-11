import urllib.request
import json

query = """[out:json][timeout:15];
node["amenity"="webcam"](47.0, 5.5, 55.0, 15.5);
out body 15;
"""

try:
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=query.encode("utf-8"),
        headers={"User-Agent": "CyberSpectreNexus/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("OSM Webcams count:", len(data.get("elements", [])))
    for el in data.get("elements", [])[:5]:
        print(el.get("id"), el.get("lat"), el.get("lon"), el.get("tags", {}).get("name"), el.get("tags", {}).get("url"))
except Exception as e:
    print("Error:", e)
