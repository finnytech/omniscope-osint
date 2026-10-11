"""
CYBER-SPECTRE-NEXUS: OSINT Board Fast-Boot MCP Stdio Runner
===========================================================
Ultra-fast (< 5ms) JSON-RPC Stdio-Runner for Google Antigravity 2.
Features:
- Instant startup: responds to 'initialize' and 'tools/list' in < 2ms using pre-cached tools_cache.json
- Background engine warmup: loads JevEngine, CameraEngine, and SQLite in a daemon thread without blocking handshake
- Full MCP 2024-11-05 protocol compliance with inputSchema & parameters dual-export
"""

import sys
import os
import json
import threading
import asyncio

# Configure UTF-8 text I/O on Windows
if sys.platform == "win32":
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        import io
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_cache.json")

# Fast load cached tool definitions
_tools_list = []
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            _tools_list = json.load(f)
    except Exception as e:
        sys.stderr.write(f"[osint-mcp] Failed to read tools_cache.json: {e}\n")

# Background warmup synchronization
_warmup_event = threading.Event()
_dispatch_func = None
_loop = None

def _warmup_backend():
    global _dispatch_func, _loop
    try:
        sys.stderr.write("[osint-mcp] Background engine warmup started...\n")
        sys.stderr.flush()
        
        # Import heavy server modules in background
        from backend.services.osint_mcp_server import execute_tool
        _dispatch_func = execute_tool
        
        # Initialize an event loop for async tool executions
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
        
        _warmup_event.set()
        sys.stderr.write("[osint-mcp] Background engine warmup completed successfully.\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[osint-mcp] Background warmup error: {e}\n")
        sys.stderr.flush()
        _warmup_event.set()

def run_server():
    # Start background warmup immediately
    threading.Thread(target=_warmup_backend, daemon=True).start()
    
    sys.stderr.write(f"[osint-mcp] Fast-boot Stdio server active ({len(_tools_list)} tools ready in < 5ms).\n")
    sys.stderr.flush()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                os._exit(0)
            line_str = line.strip()
            if not line_str:
                continue

            req = json.loads(line_str)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "ping":
                sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {}}) + "\n")
                sys.stdout.flush()
                continue

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {"listChanged": False}
                        },
                        "serverInfo": {
                            "name": "osint-board",
                            "version": "2.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue

            if method in ("notifications/initialized", "initialized"):
                continue

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": _tools_list
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue

            if method == "tools/call":
                tname = params.get("name")
                targs = params.get("arguments", {})

                # Ensure backend engines are warmed up
                if not _warmup_event.wait(timeout=35.0):
                    err_resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32000, "message": "Backend engine initialization timed out"}
                    }
                    sys.stdout.write(json.dumps(err_resp) + "\n")
                    sys.stdout.flush()
                    continue

                if _dispatch_func and _loop:
                    try:
                        t_res = _loop.run_until_complete(_dispatch_func(tname, targs))
                        raw_data = t_res.get("result", t_res) if isinstance(t_res, dict) else t_res
                        text_out = json.dumps(raw_data, ensure_ascii=False, indent=2) if isinstance(raw_data, (dict, list)) else str(raw_data)
                        is_err = isinstance(t_res, dict) and "error" in t_res
                        resp = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": text_out}],
                                "isError": is_err
                            }
                        }
                    except Exception as ex:
                        resp = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": f"Tool execution exception: {ex}"}],
                                "isError": True
                            }
                        }
                else:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32603, "message": "Engine dispatcher unavailable"}
                    }

                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue

            if req_id is not None:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method {method} not found"}
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"[osint-mcp] Error in loop: {e}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    try:
        run_server()
    except (KeyboardInterrupt, SystemExit):
        os._exit(0)
    except BaseException:
        os._exit(0)
