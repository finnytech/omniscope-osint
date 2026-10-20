# OmniScope Privat [Origin Edition]
**Private High-Performance OSINT & Tactical Command Center**
Developed by FinnyTech • Architecture: Native Python FastAPI + SQLite Spatial DB + Model Context Protocol (MCP)

---

## Architecture & Capabilities
OmniScope Privat is the local, sovereign Origin Edition of OmniScope with zero external dependency and full offline/local power:
- **Spatial Engine**: 560 MB SQLite Index (`backend/data/omniscope_spatial.db`) with 508,474 cameras and 505,000 physical weather stations.
- **FastAPI Core**: High-throughput asynchronous backend (`backend/main.py`) with stream proxy, JEV visual convective predictor, and local MCP server.
- **10 Tactical Multi-Domain Layers**:
  1. Subsea Fiber Cables & Landing Stations (TeleGeography live)
  2. Disaster Alerts (GDACS)
  3. Radiation Geiger Grid (Radmon & Safecast)
  4. Baltic Sea Marine AIS (Digitraffic Finland Live Vectors)
  5. Aviation Weather Center (AWC) METAR/TAF & FAA Airport Delays
  6. KiwiSDR 0-32 MHz HF Receivers (with in-app Native Audio Deck)
  7. US Customs & Border Protection (CBP) Border Crossing Delays
  8. Tor Network Relays (Onionoo)
  9. NEXRAD Doppler Composite & 147 WMO Numerical Weather Models
  10. Asteroids & Near-Earth Objects (NASA JPL CAD)
- **Zero-Fake Guarantee**: 100% genuine real-world scientific telemetry.

---

## Local Startup
```powershell
cd D:\projects\omniscope-privat
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Open in browser: `http://localhost:8000`
