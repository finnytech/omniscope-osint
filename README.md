# 🌐 OmniScope OSINT [OFFICIAL ORIGINAL]

[![Official Original Project](https://img.shields.io/badge/OmniScope-OFFICIAL%20ORIGINAL-00ffcc?style=for-the-badge&logo=shield)](https://github.com/finnytech/omniscope-osint)
[![FinnyTech Original](https://img.shields.io/badge/Author-FinnyTech-ff0055?style=for-the-badge)](https://github.com/finnytech)
[![Web Edition](https://img.shields.io/badge/Web%20Edition-omniscope--web.pages.dev-blue?style=for-the-badge)](https://omniscope-web.pages.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> [!IMPORTANT]
> ### 🚨 OFFICIAL REPOSITORY & INTELLECTUAL PROPERTY NOTICE
> **OmniScope™ is the original, authentic open-source tactical OSINT operations center developed exclusively by [FinnyTech](https://github.com/finnytech).**
>
> ⚠️ **BEWARE OF UNAUTHORIZED CLONES & COPYCATS**:
> Following viral social media coverage, third parties (such as *"Sam Good Group / OmniScope Lite"*) have begun attempting to copy the interface, branding, and concept of OmniScope.
>
> - **Official Native / Desktop OSINT Repository**: [`https://github.com/finnytech/omniscope-osint`](https://github.com/finnytech/omniscope-osint)
> - **Official Web Edition Repository**: [`https://github.com/finnytech/omniscope-web`](https://github.com/finnytech/omniscope-web)
> - **Official Standalone MCP Suite Repository**: [`https://github.com/finnytech/omniscope-mcp`](https://github.com/finnytech/omniscope-mcp)
> - **Canonical Live Web App**: [`https://omniscope-web.pages.dev`](https://omniscope-web.pages.dev)
>
> Always verify that you are cloning and contributing to the official **FinnyTech** repositories.

> **Open-Source Dual-Monitor Geospatial Intelligence, Weather Radar & Public Sensor Grid**  
> *100% Legal & Open Data • Zero-Fake Policy • Dynamic Provider Omission • Fast SQLite Spatial Indexing*

---

## ⚡ Overview

**OmniScope OSINT** is a tactical, browser-based command center for real-time geospatial intelligence, global weather radar observation, and public sensor telemetry. 

Built with a cyberpunk tactical interface, OmniScope features a dual-monitor multi-viewport layout:
- **MON-01 (Tactical Operations Map)**: Interactive multi-layer cartography featuring high-resolution satellite imagery, real-time RainViewer Doppler precipitation radar loops, NOAA NEXRAD storm cells, earthquake epicenters, wildfire telemetry, and orbital space tracking.
- **MON-02 (Omni View Monitor)**: Dedicated multi-inspector panel for high-definition public streaming webcams, municipal highway cameras, and environmental telemetry.

---

## 🛡️ Strict Zero-Fake Policy

Unlike traditional mock dashboards that generate synthetic coordinates or dummy airplanes when credentials fail, **OmniScope OSINT operates under a strict Zero-Fake Policy**:

- **No Synthetic Fallbacks**: If an optional provider's API key is not configured, the application **never** generates fake airplanes, mock weather readings, or simulated telemetry.
- **Dynamic Feature Omission**: If an API key is absent, that provider is **completely omitted from the UI and backend routines**. Layer checkboxes, filter buttons, and polling timers for that provider simply do not appear in the dashboard.
- **Pure Open Ground Truth**: Every node, camera, weather reading, and radar return displayed in OmniScope corresponds to a genuine physical sensor or authenticated open data feed.

---

## 🌍 Open Sensor Grid (100% Free & Keyless)

OmniScope OSINT works straight out of the box with zero third-party accounts or API keys required:

| Sensor / Telemetry Feed | Source Network | Access Model |
| :--- | :--- | :--- |
| **105,000+ Real Webcams & Cams** | Panomax, Roundshot, TfL London, WSDOT, Foto-Webcam, Alpine Net | Free / Open Public |
| **140+ Weather Supercomputers** | DWD ICON, NOAA GFS, ECMWF IFS, GEM, UKMO via Open-Meteo | Free / Open Public |
| **Real-time Rain Doppler Radar** | RainViewer API Composite | Free / Open Public |
| **NOAA NEXRAD USA Radar** | NOAA National Weather Service Radar Network | Free / Open Public |
| **Global Earthquakes** | USGS Real-time GeoJSON Feeds | Free / Open Public |
| **Marine AIS Vessel Tracking** | Digitraffic Marine Maritime Network | Free / Open Public |
| **European Rail Transit** | High-speed European Transit & Departure Hubs | Free / Open Public |
| **ISS Orbital Trajectory** | Open-Notify Space Telemetry + NASA HD Earth Stream | Free / Open Public |
| **Space Weather & Kp-Index** | NOAA Space Weather Prediction Center (SWPC) | Free / Open Public |

---

## 🔑 Optional Keyed Networks

For advanced enterprise capabilities, you can optionally connect third-party keys during the first-run wizard. If skipped, these providers are cleanly omitted without affecting other features:

- **NVIDIA NIM** (`NVIDIA_NIM_KEY`): Generative AI reasoning & diffusion forecast models. Free 1,000 credits at [build.nvidia.com](https://build.nvidia.com/).
- **OpenSky Network** (`OPENSKY_USERNAME`, `OPENSKY_PASSWORD`): Live commercial flight transponders via ADS-B. Free community accounts at [opensky-network.org](https://opensky-network.org/).
- **Tomorrow.io** (`TOMORROW_API_KEY`): Hyper-local microclimate and air quality index. Free API tier at [tomorrow.io](https://www.tomorrow.io/).
- **NASA FIRMS** (`FIRMS_MAP_KEY`): Active satellite wildfire detections. Free map key at [firms.modaps.eosdis.nasa.gov](https://firms.modaps.eosdis.nasa.gov/api/map_key).
- **AirNow EPA** (`AIRNOW_API_KEY`): US Environmental Protection Agency AQI feeds at [docs.airnowapi.org](https://docs.airnowapi.org/).
- **OpenRouteService** (`OPENROUTESERVICE_KEY`): Matrix routing and geocoding at [openrouteservice.org](https://openrouteservice.org/).

## 📦 Standalone Releases (Windows Native EXE & Android APK)

Fertig kompilierte Standalone-Releases ohne Notwendigkeit einer manuellen Python-Umgebung:

| Edition | Datei | Plattform | Besonderheiten |
| :--- | :--- | :--- | :--- |
| **Android APK** | [`OmniScope-v1.0.apk`](releases/android/OmniScope-v1.0.apk) | Android 7.0 bis 15+ | 100% Offline/Standalone, Touch-UI, 1.500 eingebettete Webcams, kryptographisch v2/v3 signiert (~338 KB) |
| **Windows Native EXE** | [`OmniScope-v1.0-Windows-x64.zip`](releases/windows/OmniScope-v1.0-Windows-x64.zip) | Windows 10 & 11 (64-Bit) | Echtes natives WebView2-Fenster, kein externer Browser-Popup, Single-Instance, F11-Kommandomodus (~45 MB) |

Ausführliche Installations- und Systemhinweise findest du in der [Releases Dokumentation](releases/README.md).

---

## 🚀 Quick Start Guide (Entwickler / Source Code)

### Windows (1-Click Launcher)
Simply double-click `start.bat` or run:
```cmd
start.bat
```
*The launcher automatically detects Python, sets up a local `.venv` virtual environment, installs dependencies, runs the interactive setup wizard on first launch, and opens `http://127.0.0.1:8888`.*

### PowerShell
```powershell
.\start.ps1
```

### Linux / macOS
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Run interactive setup wizard
python3 setup_wizard.py

# 4. Launch server
python3 run_server.py
```

---

## 🛠️ Interactive Setup Wizard

Running `setup_wizard.py` launches a terminal setup assistant:
1. **Initializes SQLite Spatial Index**: Creates `backend/data/omniscope_spatial.db` with spatial B-Tree indices (`idx_weather_spatial`, `idx_camera_spatial`) for sub-millisecond bounding box queries.
2. **Key Configuration Prompt**: Prompts for optional keys with direct registration links.
3. **Generates `.env`**: Safely writes settings to a gitignored `.env` file and syncs with the local SQLite credentials vault.
4. **Outputs Active vs. Omitted Status**: Confirms which features are enabled and which are cleanly omitted under the Zero-Fake policy.

---

## ⚖️ Legal & Compliance Disclaimer
 
- **100% Legal Public Data**: All streaming webcams, traffic cameras, and sensor feeds aggregated by OmniScope OSINT originate from publicly accessible, open-government, municipal, or research feeds (including DOT highway cameras, tourism webcams, NOAA, and USGS).
- **No Unauthorized Interception**: OmniScope does not breach firewalls, access private CCTV cameras, or intercept restricted communications.
- **Biometric & Privacy Protections**: OmniScope OSINT is designed exclusively for meteorological observation, environmental research, and open-source intelligence. It must not be deployed for biometric facial recognition, individual tracking, or unauthorized personal surveillance under the EU AI Act (2024/1689) or applicable privacy regulations.
- **Trademark Notice**: OmniScope OSINT is an independent open-source project and is not affiliated with, endorsed by, or associated with Visokio Omniscope or any other commercial entities.
- **Compliance**: Users are responsible for complying with local open-source intelligence and data aggregation laws.

---

## 📚 Attributions & Third-Party Credits

- **Weather Consensus**: Meteorological models provided by [Open-Meteo.com](https://open-meteo.com/) under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Precipitation Radar**: Live composite Doppler tiles provided by [RainViewer.com](https://www.rainviewer.com/).
- **Earthquake Feeds**: Global seismic telemetry provided by the [United States Geological Survey (USGS)](https://earthquake.usgs.gov/).
- **Severe Storm Warnings**: National Weather Service feeds provided by the [National Oceanic and Atmospheric Administration (NOAA)](https://www.noaa.gov/).
- **Orbital Space Tracking**: Satellite trajectories via Open-Notify and NASA.

---

## 🤖 Model Context Protocol (MCP) Suite

OmniScope features a dedicated, standalone repository for its complete Model Context Protocol ecosystem:  
👉 **Official Standalone MCP Repository**: [`https://github.com/finnytech/omniscope-mcp`](https://github.com/finnytech/omniscope-mcp)

It provides **two official editions**:
1. **🌐 Web Edge MCP (`omniscope-web-mcp`)**: Zero-dependency cloud client querying live Cloudflare Anycast APIs ([omniscope-web.pages.dev](https://omniscope-web.pages.dev)).
2. **🖥️ Local Spatial Grid MCP (`omniscope-local-mcp`)**: Sub-millisecond direct SQLite IPC querying local `nodes.db` / `omniscope_spatial.db` (1,013,474 indexed ground nodes).

### Running Local MCP from Source:
```bash
python run_mcp.py
```
Or via `run_server.py`:
```bash
python run_server.py --mcp
```

### Running from Standalone Windows `.exe`:
```cmd
OmniScope.exe --mcp
```

### 3. Configure in Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "omniscope-local": {
      "command": "python",
      "args": ["D:/projects/omniscope-osint/run_mcp.py"]
    }
  }
}
```

### 4. Configure in Cursor (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "omniscope-local": {
      "command": "python",
      "args": ["D:/projects/omniscope-osint/run_mcp.py"]
    }
  }
}
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

## 🏷️ Tags & Keywords

`osint` • `open-source-intelligence` • `geoint` • `sigint` • `weather` • `earth-observation` • `doppler-radar` • `weather-radar` • `meteorology` • `geospatial` • `gis` • `leaflet` • `fastapi` • `python` • `surveillance` • `cctv` • `traffic-cameras` • `webcams` • `earthquake` • `usgs` • `noaa` • `nexrad` • `radar` • `satellite` • `remote-sensing` • `situational-awareness` • `mcp` • `model-context-protocol` • `tactical` • `cyberpunk` • `dashboard` • `realtime` • `sqlite` • `spatial-database` • `open-meteo` • `rainviewer` • `maritime` • `ais` • `aviation` • `space-weather` • `solar-flare` • `disaster-response` • `emergency-management` • `storm-tracking` • `hurricane-tracker` • `tornado-tracking` • `wildfire-tracking` • `firms` • `environmental-monitoring` • `command-center` • `threat-intelligence` • `defense-tech` • `panomax` • `flight-tracking`
