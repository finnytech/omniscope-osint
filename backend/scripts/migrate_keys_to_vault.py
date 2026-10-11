import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(BASE_DIR))

from backend.services.vault import set_vault_key, get_all_vault_keys, VAULT_DB_PATH

# 1. Existing keys from api_keys.json
api_keys_file = os.path.join(BASE_DIR, "data", "api_keys.json")
migrated = 0

if os.path.exists(api_keys_file):
    try:
        with open(api_keys_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in data.items():
                if v:
                    set_vault_key(k, v, f"Migrated from api_keys.json")
                    migrated += 1
        print(f"Migrated {migrated} keys from api_keys.json to {VAULT_DB_PATH}")
    except Exception as e:
        print(f"Error reading api_keys.json: {e}")

# 2. Check defaults
default_keys = {
    "mapbox_token": "",
    "firms_map_key": "",
    "openweather_api_key": "",
    "opensky_client_id": "",
    "opensky_client_secret": "",
    "windy_api_key": "",
    "tomorrow_api_key": "",
    "codiv_api_key": "",
    "nvidia_nim_key": ""
}

all_in_vault = get_all_vault_keys()
for k, v in default_keys.items():
    if k not in all_in_vault and v:
        set_vault_key(k, v, "Default seeded key")
        print(f"Seeded key {k}")

# 3. Verify
final_keys = get_all_vault_keys()
print(f"Vault successfully loaded with {len(final_keys)} keys:")
for k, v in final_keys.items():
    masked = v[:5] + "..." + v[-4:] if len(v) > 9 else "***"
    print(f"  {k}: {masked}")

# 4. Scrub api_keys.json so no plaintext keys remain
scrubbed = {k: "" for k in final_keys.keys()}
with open(api_keys_file, "w", encoding="utf-8") as f:
    json.dump(scrubbed, f, indent=2)
print("api_keys.json scrubbed of plaintext keys.")
