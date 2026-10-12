# OmniScope Releases: Android APK & Windows Desktop EXE

Offizielle Release-Pakete für **OmniScope OSINT & Weather Grid**.

---

## 📱 1. Android APK (`OmniScope-v1.0.apk`)

* **Dateipfad:** `releases/android/OmniScope-v1.0.apk`
* **Größe:** ca. 338 KB
* **Plattformen:** Android Smartphones & Tablets (Android 7.0 bis Android 15+)
* **Features & Standalone Mobile-Architektur:**
  * **100% Standalone (Kein Backend/Localhost erforderlich):** Direkte Client-seitige Datenverarbeitung und Stream-Wiedergabe ohne lokalen Python-Server.
  * **Offline Kamera-Katalog:** 1.500 kuratierte weltweite OSINT-Webcams direkt im APK-Asset-Bundle integriert.
  * **Touch-optimierte Cyberpunk-UI:** Mindest-Touchzielgröße 44x44px für Smartphone & Tablet.
  * **Mobile Bottom Navigation Dock:** Einhand-Steuerung für `[🗺️ RADAR]`, `[🌪️ STÜRME]`, `[📹 KAMERA]`, `[⚡ SCAN]`, `[🚨 ALARM]`.
  * **Slide-Up Bottom Sheet:** Live-Unwetter- & Tornado-Bedrohungspanel lässt sich per Daumenklick von unten einschieben.
  * **Safe Area Insets:** Optimiert für Display-Notches, Kameraschnittstellen und Android-Gestenleiste.
  * **Kryptographisch signiert:** APK Signature Scheme v2 & v3 validiert.
* **Installation:**
  1. APK auf das Android-Gerät übertragen.
  2. Im Dateimanager antippen und "Installieren" wählen (ggf. "Unbekannte Apps installieren" einmalig erlauben).
  3. App direkt starten.

---

## 💻 2. Windows Native Desktop EXE (`OmniScope.exe`)

* **Dateipfad:** `releases/windows/OmniScope/OmniScope.exe`
* **Größe:** Vollständiges Standalone-Paket in `releases/windows/OmniScope/`
* **Plattformen:** Windows 10 & Windows 11 (64-Bit)
* **Features & Native Desktop-Architektur:**
  * **100% Echtes Natives Desktop-Fenster:** Startet in einem eigenen nativen Windows-Container (pywebview / Edge Chromium WebView2 Win32-Container). **Kein externer Browser** (`msedge.exe` / `chrome.exe` / `webbrowser`) wird geöffnet!
  * **Eigenständiger Task-Manager-Eintrag:** Erscheint als native App `OmniScope.exe` mit eigenem Fenstertitel ("OMNISCOPE // GLOBAL OSINT TACTICAL GRID") und individuellem Prozess-Lebenszyklus.
  * **Autonomer Shutdown:** Beim Schließen des Fensters beendet sich die Applikation inklusive des integrierten Backend-Threads sofort und sauber (`os._exit(0)`).
  * **Tastatur-Shortcuts:**
    * `F11`: Vollbildmodus (Kommandozentrale).
    * `Esc`: Schließt alle offenen Dialoge und Lageberichte.
    * `Ctrl+R` / `F5`: Sofortiger Sensor- und Doppler-Scan.
  * **Single-Instance Lock:** Verhindert doppelte Prozesse und schützt den Arbeitsspeicher.
  * **Vollständige Spatial-Datenbank:** 508.474 Webcams und 505.000 Wetterstationen direkt offline angebunden.
* **Start:**
  * Einfach Doppelklick auf `OmniScope.exe`.

---

## 🛡️ Zero-Fake Richtlinie
Beide Versionen unterliegen der strikten Zero-Fake-Richtlinie:
* Echte Unterscheidung zwischen Doppler-Rotation in der Wolke (`📡 RADAR ROTATION (UNBESTÄTIGT)`) und Bodenkontakt (`🚨 AM BODEN (BESTÄTIGT)`).
* Keine erfundenen EF-Ratings oder künstlichen Wind- und Hagelgeschwindigkeiten.
