# 🌍 OmniScope OSINT [Native Edition]
**High-Performance Geospatial Intelligence & Tactical Command Center**  
Developed by [FinnyTech](https://github.com/finnytech) • Architecture: Native Python FastAPI + SQLite Spatial DB + Model Context Protocol (MCP)

[![Cloudflare Pages Live](https://img.shields.io/badge/Live-omniscope--web.pages.dev-blue?style=for-the-badge)](https://omniscope-web.pages.dev)
[![Vercel Live](https://img.shields.io/badge/Live-omniscope--web.vercel.app-black?style=for-the-badge&logo=vercel)](https://omniscope-web.vercel.app/)
[![Worker Live](https://img.shields.io/badge/Live-Cloudflare%20Worker-F38020?style=for-the-badge&logo=cloudflare)](https://omniscope-web.fuchsdany1984.workers.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=for-the-badge)](CODE_OF_CONDUCT.md)

---

## 🌐 Live Web Deployments & Mirror Endpoints
- **Cloudflare Pages Production**: [https://omniscope-web.pages.dev](https://omniscope-web.pages.dev)
- **Vercel Global Deployment**: [https://omniscope-web.vercel.app/](https://omniscope-web.vercel.app/)
- **Cloudflare Anycast Edge Worker API**: [https://omniscope-web.fuchsdany1984.workers.dev/](https://omniscope-web.fuchsdany1984.workers.dev/)

---

## ⚡ Architecture & Capabilities
**OmniScope OSINT** is the native desktop and server edition of the OmniScope ecosystem, engineered for high-throughput spatial analysis, sovereign offline operation, and real-time open intelligence:

- **Spatial Engine**: Native SQLite spatial indexing with over 500,000 indexed physical sensor nodes and global feeds.
- **FastAPI Core**: Asynchronous backend core (`backend/main.py`) with low-latency telemetry streaming, reverse-proxying, and Model Context Protocol (MCP) tool integration.
- **10 Tactical Multi-Domain Layers**:
  1. **Subsea Fiber Cables**: TeleGeography global undersea cables and landing stations.
  2. **Disaster Alerts**: Real-time Global Disaster Alert and Coordination System (GDACS).
  3. **Radiation Geiger Grid**: Radmon and Safecast environmental sensor networks.
  4. **Maritime AIS**: High-resolution vessel telemetry and marine vectors.
  5. **Aviation METAR/TAF**: Aviation Weather Center (AWC) and FAA airport delay monitors.
  6. **KiwiSDR Radio Receivers**: 0–32 MHz HF radio receiver grid with in-app native audio deck and FFT spectrum waterfall.
  7. **Border Wait Times**: US Customs & Border Protection (CBP) commercial and passenger crossing telemetry.
  8. **Tor Network Relays**: Onionoo consensus routing and relay nodes.
  9. **Radar & Meteorology**: NEXRAD Doppler composite loops and 147 WMO numerical weather models.
  10. **Space & Orbital**: NASA JPL Close-Approach Asteroids & ISS orbital tracking.
- **Zero-Fake Guarantee**: 100% authentic, keyless scientific data feeds.

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/finnytech/omniscope-osint.git
cd omniscope-osint
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Tactical Command Center
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
```
http://localhost:8000
```

---

## 📦 Standalone Releases
Pre-packaged standalone builds for Windows and Android are available on the [Releases Page](https://github.com/finnytech/omniscope-osint/releases):
- **Windows Desktop:** `OmniScope-v2.4-Windows-x64.zip` (Native lightweight WebView2 runtime)
- **Android APK:** `OmniScope-v2.4.apk` (Standalone signed APK)

---

## 📜 License & Community
- **License:** [MIT License](LICENSE)
- **Code of Conduct:** [Contributor Covenant v2.1](CODE_OF_CONDUCT.md)
- **Maintainer Contact:** `contact@finny.eu.org`
