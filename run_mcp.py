#!/usr/bin/env python3
"""
OmniScope OSINT - Local MCP Server Launcher
Direct stdio runner for Claude Desktop, Cursor, and autonomous AI agents.
Connects directly to local SQLite spatial database (nodes.db / omniscope_spatial.db).
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.services.osint_mcp_server import run_stdio_server

if __name__ == "__main__":
    try:
        run_stdio_server()
    except (KeyboardInterrupt, SystemExit):
        os._exit(0)
    except BaseException:
        os._exit(0)
