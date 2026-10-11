import urllib.request
import json

KEY = ""

# 1. Countries
try:
    url = "https://api.windy.com/webcams/api/v3/countries"
    req = urllib.request.Request(url, headers={"x-windy-api-key": KEY, "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    print("Total countries in Windy:", len(data))
    sorted_countries = sorted(data, key=lambda x: x.get("count", 0), reverse=True)
    for c in sorted_countries[:15]:
        print(f"  {c.get('name')} ({c.get('code')}): {c.get('count')} webcams")
except Exception as e:
    print("Countries Error:", e)

# 2. Categories
try:
    url = "https://api.windy.com/webcams/api/v3/categories"
    req = urllib.request.Request(url, headers={"x-windy-api-key": KEY, "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        cats = json.loads(resp.read().decode())
    print("\nCategories in Windy:")
    for cat in cats:
        print(f"  {cat.get('name')} (id: {cat.get('id')}): {cat.get('count')} webcams")
except Exception as e:
    print("Categories Error:", e)
