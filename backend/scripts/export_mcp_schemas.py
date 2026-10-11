import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from backend.services.osint_mcp_server import TOOL_DEFINITIONS

from pathlib import Path

MCP_DIR = os.environ.get("OMNISCOPE_MCP_DIR") or str(Path.home() / ".gemini" / "antigravity" / "mcp" / "osint-board")
CACHE_PATH = os.path.join(BASE_DIR, "backend", "services", "tools_cache.json")

os.makedirs(MCP_DIR, exist_ok=True)

clean_tools_list = []

for tool in TOOL_DEFINITIONS:
    name = tool["name"]
    desc = tool.get("description", "")
    params = tool.get("parameters") or {"type": "object", "properties": {}}
    
    # Ensure params is a valid object schema
    if not isinstance(params, dict):
        params = {"type": "object", "properties": {}}
    if "type" not in params:
        params["type"] = "object"
    if "properties" not in params:
        params["properties"] = {}
        
    tool_spec = {
        "name": name,
        "description": desc,
        "inputSchema": params,
        "parameters": params
    }
    clean_tools_list.append(tool_spec)
    
    # Write Antigravity lazy tool JSON
    lazy_json_path = os.path.join(MCP_DIR, f"{name}.json")
    with open(lazy_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": name,
            "description": desc,
            "parameters": params
        }, f, indent=2, ensure_ascii=False)

# Write fast-boot tools_cache.json
with open(CACHE_PATH, "w", encoding="utf-8") as f:
    json.dump(clean_tools_list, f, indent=2, ensure_ascii=False)

print(f"Successfully exported {len(clean_tools_list)} clean MCP tools to {MCP_DIR} and {CACHE_PATH}!")
