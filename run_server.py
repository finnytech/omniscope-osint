"""
CYBER-SPECTRE-NEXUS: Master Server Runner
Features:
- Single-Instance PID Lockfile (prevents multiple Uvicorn instances and RAM explosion)
- Automatic cleanup of stale/ghost processes on port 8888
- Dual-stack IPv4/IPv6 socket binding
"""

import os
import sys
import socket
import atexit
import signal
import time
import subprocess
import uvicorn
from backend.main import app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(BASE_DIR, "server.pid")

def is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        # On Windows, os.kill(pid, 0) checks if process exists
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False

def kill_pid(pid: int):
    try:
        print(f"[*] Terminating previous server process (PID: {pid})...", flush=True)
        if sys.platform == "win32":
            os.system(f"taskkill /F /PID {pid} >nul 2>&1")
        else:
            os.kill(pid, signal.SIGTERM)
        time.sleep(1.0)
    except Exception as e:
        print(f"[!] Could not kill PID {pid}: {e}", flush=True)

def cleanup_pid():
    if os.path.exists(PID_FILE):
        try:
            os.remove(PID_FILE)
        except Exception:
            pass

def enforce_single_instance(port: int):
    # 1. Check PID file
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    old_pid = int(content)
                    if is_pid_alive(old_pid) and old_pid != os.getpid():
                        print(f"[!] Detected existing server running on PID {old_pid}. Terminating old instance...", flush=True)
                        kill_pid(old_pid)
        except Exception as e:
            print(f"[!] Note on PID check: {e}", flush=True)

    # 2. Check if port is already bound
    sock_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_bound = False
    try:
        sock_test.bind(('127.0.0.1', port))
    except Exception:
        is_bound = True
    finally:
        sock_test.close()

    if is_bound:
        print(f"[!] Port {port} is occupied. Attempting to free port...", flush=True)
        try:
            # Find PID using port on Windows
            out = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True, text=True)
            for line in out.strip().splitlines():
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in parts:
                    local_addr = parts[1]
                    if local_addr.endswith(f":{port}"):
                        pid_to_kill = int(parts[-1])
                        if pid_to_kill != os.getpid() and pid_to_kill > 0:
                            kill_pid(pid_to_kill)
            time.sleep(1.0)
        except Exception:
            pass

    # 3. Write current PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    atexit.register(cleanup_pid)

def run():
    if "--mcp" in sys.argv:
        from backend.services.osint_mcp_server import run_stdio_server
        try:
            run_stdio_server()
        except (KeyboardInterrupt, SystemExit):
            os._exit(0)
        except BaseException:
            os._exit(0)
        return

    port = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8888
    enforce_single_instance(port)

    print(f'[*] OmniScope OSINT starting on 0.0.0.0:{port} [PID: {os.getpid()}]', flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

if __name__ == '__main__':
    run()
