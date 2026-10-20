# OmniScope OSINT & Web v2.1.0 Roadmap: 170 Neue Keyless Provider, Map-Layers, MON-02 Deep-Dives & Tools

> **Version:** v2.1.0 Taktische Kartenerweiterung & Deep-Dive Architektur  
> **Architektur-Grundsatz:**
> * **MON-01 (Tactical Global Map):** Der zentrale Haupt-Kartenschirm. Alle geografischen Daten, Seekabel, Schiffe, Flugzeuge, Strahlungswerte, Katastrophen, Bojen, WebSDRs, Grenzen und Kraftwerke werden als **performante, ein- und ausschaltbare Layer direkt auf MON-01** dargestellt.
> * **MON-02 (Tactical Node Deep-Dive Inspector):** Der dedizierte forensische Untersuchungs-Monitor. Klick auf eine beliebige Node auf der MON-01-Karte öffnet sofort den vollständigen **MON-02 Deep-Dive** (Live-Stream, Spezifikationen, Sensor-Diagramme, UN-Lageberichte, Frequenz-Audio, Schiffs-/Flugdaten).  
> **Ecosystem:** OmniScope OSINT (Self-Hosted Python/FastAPI Localhost Core), OmniScope Web (Serverless Cloudflare Pages & Workers), Desktop EXE & Android APK  
> **Strikte Qualitäts-Direktive:** 100% Zero-Fake Policy, ausschließlich verifizierte echte Keyless Open Data APIs, KEINE nutzlosen Backend-Algorithmen oder theoretischer Mathe-Füllstoff.  
> **Umfang:** 170 konkrete, nützliche Features (F-001 bis F-170), aufgeteilt in 10 Domänen.

---

## 🧭 Übersicht der 10 Taktischen Domänen

```
┌────────────────────────────────────────────────────────────────────────┐
│      OMNISCOPE v2.1.0 DUAL-COMMAND: MON-01 MAP & MON-02 DEEP-DIVE     │
│                                                                        │
│  [D1]  Seekabel, Cyber & Internet-Outage Layers + MON-02 Deep-Dive     │
│  [D2]  GDACS Katastrophen, Multi-Hazard & Tsunami + MON-02 Deep-Dive   │
│  [D3]  Weltraum, Satelliten & Solar-Hazards + MON-02 Deep-Dive         │
│  [D4]  Strahlungs-Sensorik, Umwelt & Bio-Hazards + MON-02 Deep-Dive    │
│  [D5]  Luftfahrt, Flughäfen & NOTAM Hazards + MON-02 Deep-Dive         │
│  [D6]  Maritim-AIS, Schiffsverkehr & Bojen + MON-02 Deep-Dive          │
│  [D7]  WebSDR-Funk, HF-Spektrum & Blitzortung + MON-02 Deep-Dive       │
│  [D8]  Grenzposten, Energie & Kritische Infra + MON-02 Deep-Dive       │
│  [D9]  MON-01 / MON-02 Synchronisations- & Taktik-Steuerung            │
│  [D10] OSINT Feld-Werkzeuge, Rechner & Geo-Exporte                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Domain 1: Seekabel, Cyber & Internet-Outage Layers + MON-02 Deep-Dive (F-001 - F-017)

*Vektor-Seekabel auf MON-01, IODA-Netzausfälle, Tor-Exit-Nodes und vollständige MON-02 Seekabel- & Outage-Forensik.*

- **F-001** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Submarine Cable Vektor-Layer auf MON-01** - Interaktives Vektor-Netzwerk von 550+ globalen Untersee-Glasfaserkabeln direkt auf der Weltkarte.
- **F-002** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 Seekabel Deep-Dive Dossier** - Klick auf ein Seekabel auf MON-01 lädt in MON-02 sofort die technischen Daten: Kabellänge in km, Faserpaare, Kapazität (Tbps), Inbetriebnahmedatum, Eigentümerkonsortium und Landestationen.
- **F-003** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Seekabel-Landestationen (Landing Points) Marker auf MON-01** - Klickbare Küstenpunkte aller globalen Anlandestationen.
- **F-004** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Strategische Seekabel-Nadelöhre (Chokepoints) Risiko-Layer** - Farbliche Hervorhebung von Risikozonen (Rotes Meer, Malakka, Gibraltar, Ärmelkanal) mit Single-Point-of-Failure-Stufen.
- **F-005** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **IODA Globale Internet-Ausfall-Polygone auf MON-01** (`api.ioda.inetintel.cc.gatech.edu/v2/outages/summary`) - Färbt Länder und Regionen mit aktiven Netzausfällen rot/orange auf der Karte ein.
- **F-006** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 IODA Outage Deep-Dive Inspektor** - Klick auf ein Land auf MON-01 visualisiert in MON-02 den 3-Signal-Laufzeitgraphen: BGP-Routing-Rückzüge, Active-Probing-Latenz und Darknet-Teleskop-Aktivität.
- **F-007** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Tor-Relay Weltnetzwerk-Layer auf MON-01** (`onionoo.torproject.org/details`) - 7.500+ aktive Tor-Relays als zuschaltbare Kartenpunkte (Grün = Guard, Rot = Exit).
- **F-008** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 Tor Node Deep-Dive Dossier** - Klick auf ein Tor-Relay auf MON-01 zeigt in MON-02 Nickname, Fingerprint, ASN, Bandbreiten-Verlauf, Uptime und Kontakt-Info.
- **F-009** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Tor Exit-Node Schnellprüfung** - Schnelleingabe im MON-01-Header prüft eine IP und öffnet sofort den Deep-Dive in MON-02.
- **F-010** `[OSINT]` `[WEB-EDITION]`: **RIPE Stat BGP-Prefix Routing-Layer** (`stat.ripe.net/data/routing-status/data.json`) - Zeigt BGP-Sichtbarkeit und unautorisierte Prefix-Hijacks auf der Karte.
- **F-011** `[OSINT]` `[WEB-EDITION]`: **Internet-Knotenpunkte (IXP) Layer** (`api.bgpview.io`) - Markiert weltweite IXPs (DE-CIX, AMS-IX) mit Klick-Deep-Dive in MON-02 für verbundene Carrier.
- **F-012** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **DNS Root Server Cluster Layer auf MON-01** (`stat.ripe.net/data/dns-root-telemetry/data.json`) - Standorte und Live-Latenzen der 13 DNS-Wurzelserver-Netze (A bis M).
- **F-013** `[WEB-EDITION]` `[OSINT]`: **Interaktiver Seekabel-Bruch Simulator** - Klick auf ein Seekabel simuliert dessen Ausfall und zeigt umgeleitete Datenwege im MON-02-Bericht.
- **F-014** `[WEB-EDITION]` `[OSINT]`: **Satelliten-Bodenstationen (Ground Gateways) Layer** - Geokodierte Gateway-Stationen für Starlink und OneWeb auf MON-01.
- **F-015** `[OSINT]` `[EXE/APK]`: **Lokaler Egress-Netzwerk Tracer** - Zeichnet die Hops der eigenen Internetverbindung auf MON-01 ein mit Latenzgraphen in MON-02.
- **F-016** `[WEB-EDITION]` `[OSINT]`: **Cyber-Outage Alarm-Banner im Karten-Header** - Informiert über akute nationale Internetsperren mit Direktsprung und MON-02-Öffnung.
- **F-017** `[WEB-EDITION]` `[OSINT]`: **Cloudflare Radar Netzausfall-Feed** - Automatischer Live-Marker bei behördlich verhängten Internetsperren oder großen Providerausfällen.

---

## Domain 2: GDACS Katastrophen, Multi-Hazard & Tsunami + MON-02 Deep-Dive (F-018 - F-034)

*Katastrophen-Polygone auf MON-01 mit UN-Lageberichten, Flusspegeln und Tsunami-Wellen in MON-02.*

- **F-018** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **GDACS Multi-Hazard Layer auf MON-01** (`gdacs.org/gdacsapi/api/events/geteventlist/SEARCH`) - Direkte Anzeige aller aktiven UN/EU-Katastrophenmeldungen (Erdbeben, Zyklone, Überschwemmungen, Vulkane, Dürren).
- **F-019** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 GDACS Katastrophen Deep-Dive Briefing** - Klick auf ein Katastrophen-Icon auf MON-01 lädt in MON-02 das vollständige UN-Lagebild: Opferzahlen, zerstörte Krankenhäuser/Schulen, betroffene Bevölkerung und amtliche Bulletins.
- **F-020** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **GDACS Farb-Triage Marker** - Farbcodierte Icons auf MON-01: Rot (internationale Katastrophe), Orange (schwere regionale Lage), Grün (Beobachtung).
- **F-021** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Tropensturm-Zugbahn & Gefahrenkegel auf MON-01** - Zeichnet Live-Zugbahnprognosen, Windradien (34kt, 50kt, 64kt Hurrikan-Stärke) und Sturmflutrisiken.
- **F-022** `[WEB-EDITION]` `[OSINT]`: **MON-02 Tropensturm Deep-Dive Telemetrie** - Zeigt in MON-02 Kerndruck-Verlauf (hPa), maximale Windspitzen, Satelliten-Loop des Auges und Evakuierungsbefehle.
- **F-023** `[WEB-EDITION]` `[OSINT]`: **UN OCHA ReliefWeb Krisen-Marker auf MON-01** (`api.reliefweb.int/v2/disasters`) - Klickbare Lage-Pins für humanitäre Notlagen.
- **F-024** `[WEB-EDITION]` `[OSINT]`: **MON-02 ReliefWeb Lagebericht-Viewer** - Klick auf einen ReliefWeb-Pin öffnet in MON-02 den kompletten UN-Feldbericht mit Spendenaufrufen und Flüchtlingszahlen.
- **F-025** `[WEB-EDITION]` `[OSINT]`: **USGS Live-Flusspegel Layer auf MON-01** (`waterservices.usgs.gov/nwis/iv/?format=json`) - 10.000+ Flusspegel-Pins mit aktuellem Wasserstand und Hochwassermarkierung.
- **F-026** `[WEB-EDITION]` `[OSINT]`: **MON-02 Flusspegel-Ganglinie Deep-Dive** - Klick auf einen Pegel zeigt in MON-02 den 7-Tage-Wasserstandsverlauf, Durchflussmenge (cfs) und Hochwasser-Vorhersage.
- **F-027** `[WEB-EDITION]` `[OSINT]`: **Sturzflut- & Hochwasser-Warnlayer auf MON-01** - Hebt Flussabschnitte optisch hervor, deren Pegel über die Hochwasser-Warnmarke steigen.
- **F-028** `[WEB-EDITION]` `[OSINT]`: **Aktive Vulkane & Aschewolken-Layer auf MON-01** (Smithsonian / GDACS) - Eruptionsstatus, Farbcodes (Rot/Orange/Gelb) und Aschewolken-Polygone.
- **F-029** `[WEB-EDITION]` `[OSINT]`: **MON-02 Vulkan-Inspektor** - Zeigt in MON-02 Vulkanprofil, Eruptionsgeschichte, Webcams vor Ort und Seismizität des Kraters.
- **F-030** `[WEB-EDITION]` `[OSINT]`: **Tsunami-Laufzeit-Isochronen Layer auf MON-01** (NOAA PTWC) - Zeichnet Ausbreitungskonturen der Tsunami-Wellenfront in 1-Stunden-Schritten ein.
- **F-031** `[WEB-EDITION]` `[OSINT]`: **Copernicus EMS Satelliten-Schadenskarten Layer auf MON-01** - Überlagert die Karte mit offiziellen Satellitenkarten von Flutgrenzen und Zerstörungsgraden.
- **F-032** `[WEB-EDITION]` `[OSINT]`: **Bevölkerungs-Expositions-Kalkulator auf MON-01** - Klick auf ein Epizentrum zeichnet 25km/50km/100km-Ringe und schätzt betroffene Einwohner.
- **F-033** `[WEB-EDITION]` `[OSINT]`: **Dürre- & Erntestress Vektor-Layer auf MON-01** - Satellitengestützte Bodenfeuchte-Anomalien zur Früherkennung von Dürrezonen.
- **F-034** `[WEB-EDITION]` `[OSINT]`: **Katastrophen-Kamera Direktsprung in MON-02** - Klick auf einen GDACS-Event lädt in MON-02 sofort die nächstgelegene aktive Webcam zur optischen Sichtung.

---

## Domain 3: Weltraum, Satelliten & Solar-Hazards + MON-02 Deep-Dive (F-035 - F-051)

*Bodenspuren auf MON-01, Weltraumwetter und vollständiger MON-02 Satelliten- & Asteroiden-Inspektor.*

- **F-035** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **ISS & Tiangong Raumstationen Live-Bodenspur auf MON-01** (`celestrak.org/...GROUP=stations&FORMAT=json-pretty`) - Echtzeit-Position, Flughöhe (420 km), Bahngeschwindigkeit (27.600 km/h) und 90-Minuten-Umlaufbahn.
- **F-036** `[WEB-EDITION]` `[OSINT]`: **MON-02 Raumstationen Deep-Dive Cockpit** - Klick auf die ISS oder Tiangong auf MON-01 lädt in MON-02 den Live-HD-Erd-Videostream, Besatzungsliste, wissenschaftliche Nutzlasten und das Bordfunk-Audio.
- **F-037** `[WEB-EDITION]` `[OSINT]`: **Satelliten-Sichtbarkeits-Kegel (Footprint) Layer auf MON-01** - Zeichnet den aktuellen Ausleuchtungsbereich der Raumstationen auf die Erdoberfläche.
- **F-038** `[WEB-EDITION]` `[OSINT]`: **CelesTrak Aktive Satellitenflotte Layer** (`celestrak.org/...GROUP=active&FORMAT=json-pretty`) - Wählbare Satellitengruppen (Weather, Navigation, Earth Resources) als bewegliche Icons auf MON-01.
- **F-039** `[WEB-EDITION]` `[OSINT]`: **MON-02 Satelliten-Telemetry Dossier** - Klick auf einen Satelliten auf MON-01 zeigt in MON-02 NORAD-ID, Apogäum/Perigäum, Inklination, Betreiber und geplante Lebensdauer.
- **F-040** `[WEB-EDITION]` `[OSINT]`: **Starlink-Megakonstellation Dichte-Heatmap auf MON-01** - Visualisiert die Dichte aktiver Starlink-Orbitalebenen über dem gewählten Kartengebiet.
- **F-041** `[WEB-EDITION]` `[OSINT]`: **Weltraumschrott-Trümmerwolken Layer auf MON-01** (`GROUP=cosmos-1408-debris`) - Trümmerfelder historischer Satellitenkollisionen und ASAT-Tests.
- **F-042** `[WEB-EDITION]` `[OSINT]`: **Aurora Borealis / Australis OVATION 30-Minuten Polarlicht-Layer** - Farbfläche auf MON-01 mit Polarlichter-Sichtbarkeitswahrscheinlichkeiten (0-100%).
- **F-043** `[WEB-EDITION]` `[OSINT]`: **Tag-Nacht-Grenze (Terminator) mit Dämmerungszonen auf MON-01** - Exakter Sonnenstand mit bürgerlicher, nautischer und astronomischer Dämmerung.
- **F-044** `[WEB-EDITION]` `[OSINT]`: **NASA JPL Asteroiden-Annäherungs Radar auf MON-01** (`ssd-api.jpl.nasa.gov/cad.api`) - Einblendbares Radarfenster für erdnahe Asteroiden der nächsten 30 Tage mit Distanz in Monddistanzen (LD).
- **F-045** `[WEB-EDITION]` `[OSINT]`: **MON-02 Asteroiden-Gefahren Deep-Dive** - Klick auf einen Asteroiden zeigt in MON-02 Relativgeschwindigkeit (km/s), geschätzten Durchmesser in Metern, Torino-Skala und Orbit-3D-Simulation.
- **F-046** `[WEB-EDITION]` `[OSINT]`: **NOAA SWPC Solar Flare Röntgenfluss Status-Badge** (`services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json`) - Live-Badge im Karten-Header für C-, M- und X-Klasse Sonneneruptionen.
- **F-047** `[WEB-EDITION]` `[OSINT]`: **MON-02 Weltraumwetter Deep-Dive Terminal** - Zeigt in MON-02 GOES-Röntgengraphen, Sonnenwind-Geschwindigkeit (ACE/DSCOVR) und geomagnetischen Kp-Index-Verlauf.
- **F-048** `[WEB-EDITION]` `[OSINT]`: **SDO Live-Sonnenbild Popover in MON-02** - Klick auf das Sonnen-Icon lädt in MON-02 die neueste AIA-193-Extrem-UV-Aufnahme der Sonne zur Analyse koronaler Löcher.
- **F-049** `[WEB-EDITION]` `[OSINT]`: **Koronaler Massenauswurf (CME) Stoßwellen-Uhr** - Countdown-Rechner bis zum Eintreffen von Plasma-Schockwellen am Erdmagnetfeld.
- **F-050** `[WEB-EDITION]` `[OSINT]`: **Satelliten-Überflug-Prädiktor für Kartenstandort** - Klick auf einen Kartenpunkt berechnet nächste sichtbare Überflüge und Blickrichtung.
- **F-051** `[WEB-EDITION]` `[OSINT]`: **Wiedereintritts-Alarm für abstürzende Raketenstufen** - Markiert die geschätzte Bodenspur abstürzender Raumfahrt-Objekte auf MON-01.

---

## Domain 4: Strahlungs-Sensorik, Umwelt & Bio-Hazards + MON-02 Deep-Dive (F-052 - F-068)

*Radioaktivitäts-Pins auf MON-01, Feinstaub und vollständiger MON-02 Strahlungs- & Schadstoff-Inspektor.*

- **F-052** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Safecast Radioaktivitäts-Messnetz Layer auf MON-01** (`api.safecast.org`) - Weltweites Bürgernetzwerk von Geigerzähler-Stationen mit Messwerten in µSv/h und CPM direkt auf der Karte.
- **F-053** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 Strahlungs-Sensor Deep-Dive Dossier** - Klick auf einen Safecast-Punkt auf MON-01 lädt in MON-02 die Dosisleistungshistorie, Sensor-Typ (bGeigie Nano), Standortfoto und akustische Geigerzähler-Klicks.
- **F-054** `[WEB-EDITION]` `[OSINT]`: **Kernkraftwerke Schutzzonen Layer auf MON-01** - 440+ Atomkraftwerke weltweit mit 10km-, 25km- und 50km-Sicherheitsringen.
- **F-055** `[WEB-EDITION]` `[OSINT]`: **MON-02 Kernkraftwerks-Inspektor** - Klick auf ein AKW auf MON-01 zeigt in MON-02 Reaktortypen, MW-Leistung, Status, Kühlquelle und aktuelle Strahlungswerte der Umgebungs-Sensoren.
- **F-056** `[WEB-EDITION]` `[OSINT]`: **Staatliche Frühwarnnetze (EURDEP & EPA RadNet) Layer auf MON-01** - Amtliche Gamma-Dosisleistungs-Messstationen europäischer und amerikanischer Behörden.
- **F-057** `[WEB-EDITION]` `[OSINT]`: **Radioaktivitäts-Grenzwert Warnmarker auf MON-01** - Messpunkte auf der Karte färben sich rot und pulsieren, sobald > 0,30 µSv/h gemessen werden.
- **F-058** `[WEB-EDITION]` `[OSINT]`: **OpenAQ Weltweite Luftqualitäts-Messstationen Layer auf MON-01** (v3 API) - 30.000+ amtliche Messstellen weltweit.
- **F-059** `[WEB-EDITION]` `[OSINT]`: **MON-02 Luftqualitäts-Deep-Dive** - Klick auf eine OpenAQ-Station zeigt in MON-02 Feinstaub (PM2.5, PM10), Ozon (O3), Stickstoffdioxid (NO2) und 24-Stunden-Trenddiagramme.
- **F-060** `[WEB-EDITION]` `[OSINT]`: **Feinstaub-Heatmap (PM2.5 & PM10) auf MON-01** - Transparente Farbüberlagerung der Karte nach dem EPA/WHO-Luftqualitätsindex (AQI).
- **F-061** `[WEB-EDITION]` `[OSINT]`: **Copernicus CAMS Waldbrand-Rauchfahnen Layer auf MON-01** - Vorhersage der Rauch- und Feinstaubausbreitung bei Großbränden.
- **F-062** `[WEB-EDITION]` `[OSINT]`: **EFFIS Aktive Brandherde & Brandleistungs Layer auf MON-01** - Satellitenerfasste Brandherde mit Megawatt-Brandintensität (FRP).
- **F-063** `[WEB-EDITION]` `[OSINT]`: **Waldbrand-Gefahrenindex (FWI) Flächen-Layer auf MON-01** - Kartiert Waldbrand-Gefahrenstufen von Gering bis Extrem.
- **F-064** `[WEB-EDITION]` `[OSINT]`: **Sahara-Staub & Sandsturm Ausbreitungs-Vektor auf MON-01** - Verfolgt transkontinentale Staubwolken über Ozeanen.
- **F-065** `[WEB-EDITION]` `[OSINT]`: **Gefahrgut- & Chemieanlagen Evakuierungsradien Tool auf MON-01** - Klick auf Industrieanlagen zeichnet 5km/10km/25km-Sicherheitskreise ein.
- **F-066** `[WEB-EDITION]` `[OSINT]`: **Gaußsches Rauchfahnen-Modell auf MON-01** - Berechnet und zeichnet die windabhängige Ausbreitungswolke basierend auf dem lokalen Windvektor.
- **F-067** `[WEB-EDITION]` `[OSINT]`: **Akustischer Geigerzähler-Klicker in MON-02** - Erzeugt Klickgeräusche proportional zur Strahlendosis der im Deep-Dive geöffneten Station.
- **F-068** `[WEB-EDITION]` `[OSINT]`: **Umweltlage-Filterleiste auf MON-01** - Schnelles Umschalten zwischen Strahlung, Feinstaub und Waldbrand-Ansicht.

---

## Domain 5: Luftfahrt, Flughäfen & NOTAM Hazards + MON-02 Deep-Dive (F-069 - F-085)

*Flughafen-Marker auf MON-01, Flugwetter-Kategorien und vollständiger MON-02 Flugbetriebs- & METAR-Inspektor.*

- **F-069** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **FAA NAS Flughafen-Status Layer auf MON-01** (`nasstatus.faa.gov/api/airport-status-information`) - Live-Erfassung von Ground Stops, Ground Delays und Startbahn-Verzögerungen an Großflughäfen.
- **F-070** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 Flughafen Deep-Dive Cockpit** - Klick auf einen Flughafen auf MON-01 lädt in MON-02 den Dekodierten METAR/TAF, aktive Pisten, Verspätungsgründe, Webcams am Rollfeld und ATC-Tower-Audio.
- **F-071** `[WEB-EDITION]` `[OSINT]`: **Flughafen-Marker mit Betriebs-Status auf MON-01** - Markiert Airports auf der Karte: Grün (Normalbetrieb), Gelb (Verzögerungen), Rot (Ground Stop / Piste gesperrt).
- **F-072** `[WEB-EDITION]` `[OSINT]`: **Flugwetter-Kategorien Farb-Layer auf MON-01** - Färbt Flugplätze nach VFR (Grün), MVFR (Blau), IFR (Rot) und LIFR (Magenta) ein.
- **F-073** `[WEB-EDITION]` `[OSINT]`: **Pisten-Seitenwind-Rechner Tool in MON-02** - Berechnet für jede Piste des im Deep-Dive geöffneten Airports die exakte Gegen- und Seitenwindkomponente.
- **F-074** `[WEB-EDITION]` `[OSINT]`: **SIGMET & AIRMET Gefahrenzonen-Polygone auf MON-01** - Live-Polygone auf der Karte für schwere Gewitterzonen, Vereisungsgebiete und Turbulenzen.
- **F-075** `[WEB-EDITION]` `[OSINT]`: **Vulkanasche-Sperrkorridore Layer (VAAC) auf MON-01** - Kartiert gesperrte Flugflächen bei Vulkanausbrüchen.
- **F-076** `[WEB-EDITION]` `[OSINT]`: **Militärflugzeug-Filter Layer auf MON-01** (`api.airplanes.live/v2/mil`) - Hebt Tanker, AWACS-Aufklärer und Transportmaschinen mit speziellem Militär-Icon hervor.
- **F-077** `[WEB-EDITION]` `[OSINT]`: **MON-02 Flugzeug Deep-Dive Dossier** - Klick auf ein Flugzeug auf MON-01 zeigt in MON-02 Flugnummer, Rufzeichen, ICAO, Flugzeugtyp, barometrische Höhe, Steig-/Sinkrate, Abflughafen, Zielflughafen und Foto.
- **F-078** `[WEB-EDITION]` `[OSINT]`: **Notfall-Transpondercode Sofortalarm auf MON-01 & MON-02** - Pulsierender roter Marker bei Squawk 7700 (Luftnotfall), 7600 (Funkausfall) oder 7500 mit sofortigem Auto-Fokus in MON-02.
- **F-079** `[WEB-EDITION]` `[OSINT]`: **Live ATC-Tower Funkstream Popover in MON-02** - Klick auf einen Flughafen öffnet den verlinkten Live-Funkstream direkt im Audio-Bereich von MON-02.
- **F-080** `[WEB-EDITION]` `[OSINT]`: **Durchstart- & Fehlanflug-Erkennung auf MON-01** - Markiert Flugzeuge, die unter 1.000 Fuß den Landeanflug abbrechen und steil steigen.
- **F-081** `[WEB-EDITION]` `[OSINT]`: **Flugbeschränkungsgebiete (TFR / VIP Airspace) Layer auf MON-01** - Luftraumsperrzonen bei Staatsbesuchen und Großveranstaltungen.
- **F-082** `[WEB-EDITION]` `[OSINT]`: **Großkreis-Flugrouten-Messwerkzeug** - Zieht eine Großkreis-Linie zwischen zwei Flughäfen auf MON-01 und berechnet Distanz und Kurs.
- **F-083** `[WEB-EDITION]` `[OSINT]`: **Drohnen-Schutzzonen (UAS Geofencing) Layer auf MON-01** - Zeichnet die 5-Meilen-Sicherheitszone um Flughäfen für zivile Drohnen.
- **F-084** `[WEB-EDITION]` `[OSINT]`: **Aviation METAR/TAF Rohcode Sofort-Dekoder** - Eingabefeld im Tool-Bereich übersetzt Flugwettercodes sofort in Klartext.
- **F-085** `[WEB-EDITION]` `[OSINT]`: **Luftfahrt-Filterleiste auf MON-01** - Schnelles Umschalten zwischen Zivil-, Militär- und Notfallflügen.

---

## Domain 6: Maritim-AIS, Schiffsverkehr & Bojen + MON-02 Deep-Dive (F-086 - F-102)

*Live-Schiffe auf MON-01, Bojen-Telemetrie und vollständiger MON-02 Schiffs- & Hafen-Inspektor.*

- **F-086** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Ostsee-AIS Schiffs-Layer auf MON-01** (`meri.digitraffic.fi/api/ais/v1/locations`) - 100% keyless Echtzeit-Schiffspositionen in der Ostsee und im Finnischen Meerbusen.
- **F-087** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 Schiffs-Deep-Dive Dossier** - Klick auf ein Schiff auf MON-01 lädt in MON-02 Schiffsname, IMO, MMSI, Flagge, Schiffstyp, Tiefgang, Fahrt durchs Wasser (SOG), Kurs (COG), Bestimmungshafen, ETA und Schiffsfoto.
- **F-088** `[WEB-EDITION]` `[OSINT]`: **Schiffstyp-Farbkodierung auf MON-01** - Frachter (Orange), Tanker (Rot), Fähren/Passagiere (Blau), Militär/Patrouille (Gelb), Fischerei (Grün).
- **F-089** `[WEB-EDITION]` `[OSINT]`: **30-Minuten Kurs- & Geschwindigkeits-Vektoren auf MON-01** - Zeigt Bewegungsrichtung und vorausberechnete Position der Schiffe an.
- **F-090** `[WEB-EDITION]` `[OSINT]`: **NOAA NDBC Hochsee-Messbojen Layer auf MON-01** (`ndbc.noaa.gov/data/realtime2/`) - 1.000+ ozeanische Bojen als interaktive Sensor-Pins auf der Karte.
- **F-091** `[WEB-EDITION]` `[OSINT]`: **MON-02 Ozean-Boje Deep-Dive Telemetrie** - Klick auf eine Boje auf MON-01 zeigt in MON-02 signifikante Wellenhöhe, dominante Wellenperiode, Wassertemperatur, Luftdruck und Windböen-Verlauf.
- **F-092** `[WEB-EDITION]` `[OSINT]`: **Monsterwellen-Warnmarker auf MON-01** - Bojen pulsieren rot, sobald signifikante Wellenhöhen > 6,0 Meter (Grober Seegang) gemessen werden.
- **F-093** `[WEB-EDITION]` `[OSINT]`: **Meerengen-Transit-Zähler auf MON-01** - Zeigt Schiffsanzahl auf Transitkurs in Suezkanal, Panamakanal, Straße von Hormus und Bosporus an.
- **F-094** `[WEB-EDITION]` `[OSINT]`: **"Dark Ship" AIS-Ausfall-Indikator auf MON-01** - Hebt Schiffe hervor, deren AIS-Transponder in Küstennähe plötzlich erlischt.
- **F-095** `[WEB-EDITION]` `[OSINT]`: **Handelshäfen & Liegeplatz-Status Layer auf MON-01** - Klickbare Häfen mit Deep-Dive in MON-02 für gemeldete Schiffsankünfte.
- **F-096** `[WEB-EDITION]` `[OSINT]`: **Seenotrettungs-Suchmuster Generator (SAR)** - Zeichnet quadratische und sektorielle Suchmuster direkt auf die MON-01-Karte.
- **F-097** `[WEB-EDITION]` `[OSINT]`: **GEBCO Ozean-Tiefenlinien & Fahrrinnen Layer auf MON-01** - Unterwassertopografie zur Erkennung von Flachwasser, Riffen und Tiefseegräben.
- **F-098** `[WEB-EDITION]` `[OSINT]`: **12-Meilen-Hoheitsgewässer & 200-Meilen-AWZ Grenzen auf MON-01** - Vektorlinien der territorialen Seegrenzen aller Küstenstaaten.
- **F-099** `[WEB-EDITION]` `[OSINT]`: **Arktische Meereis-Ausdehnung Layer auf MON-01** (NSIDC) - Eiskonzentration in Nordwestpassage und Nördlicher Seeroute.
- **F-100** `[WEB-EDITION]` `[OSINT]`: **Nautisches Distanz- & Peilungs-Werkzeug** - Misst exakte Seemeilen und rechtweisende Peilung zwischen zwei Punkten auf See.
- **F-101** `[WEB-EDITION]` `[OSINT]`: **Schiffs-Abfangkurs Rechner** - Berechnet Kurs und Zeitaufwand zum Erreichen eines Zielschiffs auf See.
- **F-102** `[WEB-EDITION]` `[OSINT]`: **Leuchtturm- & Seezeichen-Datenbank (AtoN) auf MON-01** - Markiert Leuchtfeuer und Fahrwassertonnen mit Blitzkennung und Klick-Deep-Dive.

---

## Domain 7: WebSDR-Funk, HF-Spektrum & Blitzortung + MON-02 Deep-Dive (F-103 - F-119)

*SDR-Antennen auf MON-01 mit Live-Audio-Player, Frequenz-Wasserfall und Spektrum in MON-02.*

- **F-103** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **KiwiSDR Globales WebSDR-Empfängernetz Layer auf MON-01** (`rx.linkfanel.net/kiwisdr_com.js`) - 1.200+ frei zugängliche SDR-Funkempfänger als interaktive Antennen-Icons auf der Weltkarte.
- **F-104** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 WebSDR Live-Audio & Frequenz-Tuner** - Klick auf einen KiwiSDR-Marker auf MON-01 lädt in MON-02 sofort den echten WebSDR-Audio-Stream, Frequenzabstimmung (0-30 MHz), AM/USB/LSB/CW-Demodulation und SNR-Anzeige.
- **F-105** `[WEB-EDITION]` `[OSINT]`: **Internationale Notfunk-Frequenz Schnellauswahl in MON-02**:
  - 2182 kHz (See-Notruf Grenzwelle)
  - 121,5 MHz (Luftfahrt Notfrequenz VHF)
  - 243,0 MHz (Militär Notruf UHF)
  - 14.300 MHz (Maritime Mobile Net)
  - 7.110 MHz / 14.195 MHz (Katastrophen-Notfunk der Funkamateure).
- **F-106** `[WEB-EDITION]` `[OSINT]`: **Zeitzeichen- & Normalfrequenzsender Layer auf MON-01** (WWV, CHU) - Standorte und Reichweiten strategischer Zeitzeichensender.
- **F-107** `[WEB-EDITION]` `[OSINT]`: **Zahlensender & Militärbaken Marker auf MON-01** - Standorte und Frequenzen bekannter Kurzwellenbaken (UVB-76 'The Buzzer' 4625 kHz, The Pip, Squeaky Wheel) mit 1-Klick-Abstimmung in MON-02.
- **F-108** `[WEB-EDITION]` `[OSINT]`: **Blitzortung / LightningMaps Live-Stream Layer auf MON-01** - Direkte Darstellung elektromagnetischer Blitzeinschläge in Echtzeit auf der Karte.
- **F-109** `[WEB-EDITION]` `[OSINT]`: **Echtzeit-Donnerschall Ausbreitungswelle auf MON-01** - Zeichnet einen sich mit 343 m/s ausbreitenden Kreis um Blitzeinschläge.
- **F-110** `[WEB-EDITION]` `[OSINT]`: **Amateurfunk Maidenhead-Gitter (QTH Locator) Overlay auf MON-01** - Blendet das weltweite Großfeld- und Kleinfeld-Raster (z. B. `JO31kk`) ein.
- **F-111** `[WEB-EDITION]` `[OSINT]`: **Ionosphärische Grenzfrequenz (MUF) Layer auf MON-01** - Farbkarte der maximal nutzbaren Reflexionsfrequenz für weltweite Kurzwellenverbindungen.
- **F-112** `[WEB-EDITION]` `[OSINT]`: **Funkhorizont & Antennenreichweiten-Rechner Tool** - Klick auf einen Kartenpunkt zeichnet die optische und VHF/UHF-Reichweite basierend auf der Antennenhöhe: $d \approx 4,12 \times \sqrt{h}$.
- **F-113** `[WEB-EDITION]` `[OSINT]`: **BOS- & Feuerwehr-Funkstream Marker auf MON-01** - Markiert Standorte frei zugänglicher Rettungsdienst- und Polizeifunk-Streams mit Audio-Wiedergabe in MON-02.
- **F-114** `[WEB-EDITION]` `[OSINT]`: **KiwiSDR Signal-Rausch-Filter auf MON-01** - Filtert SDR-Marker auf der Karte nach Signalqualität (SNR) und freien Nutzerplätzen.
- **F-115** `[WEB-EDITION]` `[OSINT]`: **Morsecode (CW) Audio- & Flashtool** - Integriertes Tool zum Kodieren/Dekodieren von Text in akustische Morsetöne und Blinksignale.
- **F-116** `[WEB-EDITION]` `[OSINT]`: **Rufzeichen-Präfix Identifikator** - Schnelleingabe im Funkmenü identifiziert das Ursprungsland jedes Funkrufzeichens.
- **F-117** `[WEB-EDITION]` `[OSINT]`: **Aurora-Funkreflexion Warnanzeige auf MON-01** - Markiert bei Sonnenstürmen Gebiete mit möglicher UKW-Funküberreichweite über Polarlichter.
- **F-118** `[WEB-EDITION]` `[OSINT]`: **MON-02 KiwiSDR Wasserfall-Spektrum Anzeige** - Zeigt in MON-02 ein hochauflösendes Live-Wasserfalldiagramm des empfangenen Frequenzbereichs.
- **F-119** `[WEB-EDITION]` `[OSINT]`: **Funk- & Frequenz-Filterleiste auf MON-01** - Schnelles Ein- und Ausschalten von SDRs, Notruffrequenzen und Blitzen.

---

## Domain 8: Grenzposten, Energie & Kritische Infra + MON-02 Deep-Dive (F-120 - F-136)

*Grenzkontrollen und Energie-Knoten auf MON-01 mit Wartezeiten, Reaktor- und Damm-Dossiers in MON-02.*

- **F-120** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **CBP Grenzwartezeiten Layer auf MON-01** (`bwt.cbp.gov/api/bwtpublicmod`) - Live-Wartezeiten an allen Grenzübergängen der USA zu Kanada und Mexiko direkt als klickbare Marker.
- **F-121** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **MON-02 Grenzposten Deep-Dive Dossier** - Klick auf einen Grenzübergang auf MON-01 lädt in MON-02 Wartezeiten für Standardspuren, Frachtverkehr, SENTRI/NEXUS-Spuren, offene Schalter und Verzögerungshistorie.
- **F-122** `[WEB-EDITION]` `[OSINT]`: **Grenzposten-Warnhinweise auf MON-01** - Hebt Grenzstellen hervor, die wegen Blockaden, Kontrollen oder Bauarbeiten geschlossen oder stark verzögert sind.
- **F-123** `[WEB-EDITION]` `[OSINT]`: **OpenStreetMap Overpass Infrastruktur-Layer auf MON-01** (`overpass-api.de/api/interpreter`):
  - Kernkraftwerke (`power=plant + plant:source=nuclear`)
  - Große Umspannwerke (`power=substation`)
  - Öltanklager & LNG-Terminals (`man_made=storage_tank + content=oil`)
  - Richtfunk- & Fernsehtürme (`man_made=tower`)
  - Zivilschutz-Bunker (`amenity=bunker`).
- **F-124** `[WEB-EDITION]` `[OSINT]`: **IAEA PRIS Nuklear-Reaktor Layer auf MON-01** - Standorte aller 440+ Atomreaktoren mit Megawatt-Leistung und Kühlwasserquelle.
- **F-125** `[WEB-EDITION]` `[OSINT]`: **MON-02 Atomreaktor- & Damm-Dossier** - Klick auf eine Energieanlage auf MON-01 zeigt in MON-02 Baujahr, thermische Leistung, Reaktorflotte, Stauhöhe und Speichervolumen.
- **F-126** `[WEB-EDITION]` `[OSINT]`: **Global Dam Watch & GRanD Staudämme Layer auf MON-01** - Standorte, Stauhöhe und Speichervolumen in Mio. m³ von 7.000+ Großtalsperren weltweit.
- **F-127** `[WEB-EDITION]` `[OSINT]`: **Stromnetz-Netzfrequenz Anzeige (ENTSO-E)** - Live-Status im Header für 50,00 Hz (Europa) und 60,00 Hz (USA) zur Früherkennung von Netzabwürfen.
- **F-128** `[WEB-EDITION]` `[OSINT]`: **Stromerzeugungs-Mix Popover in MON-02** - Klick auf ein Land zeigt den aktuellen Anteil von Atom-, Kohle-, Gas-, Wasser- und Sonnenenergie.
- **F-129** `[WEB-EDITION]` `[OSINT]`: **Öl- & Gaspipelines Vektor-Layer auf MON-01** - Wichtigste Pipeline-Trassen (Nord Stream, D門zhba, Keystone, Colonial).
- **F-130** `[WEB-EDITION]` `[OSINT]`: **Strategische Eisenbahn-Frachtkorridore & Alpentunnel auf MON-01** - Gotthard-Basistunnel, Brennerpass, Kanaltunnel und Güterverkehrs-Achsen.
- **F-131** `[WEB-EDITION]` `[OSINT]`: **Weltraumbahnhöfe & Raketen-Startrampen Layer auf MON-01** (Cape Canaveral, Baikonur, Kourou, Tanegashima) mit Startbereich-Sicherheitszonen.
- **F-132** `[WEB-EDITION]` `[OSINT]`: **Strategische Erdölreserve-Kavernen (SPR) Marker auf MON-01** - Standorte und Füllmengen strategischer Treibstofflager.
- **F-133** `[WEB-EDITION]` `[OSINT]`: **Meerwasserentsalzungsanlagen Layer auf MON-01** - Kritische Trinkwasserproduktionswerke im Nahen Osten und Trockengebieten.
- **F-134** `[WEB-EDITION]` `[OSINT]`: **Globale Halbleiter-Fabriken (Fabs) Layer auf MON-01** - Standorte der weltweiten Chiphersteller (TSMC, Intel, Samsung, ASML).
- **F-135** `[WEB-EDITION]` `[OSINT]`: **Kritische Infrastruktur Näherungsalarm** - Schlägt Alarm, wenn Waldbrände oder Unwetter näher als 15 km an AKWs, Staudämme oder Raffinerien heranrücken.
- **F-136** `[WEB-EDITION]` `[OSINT]`: **Infrastruktur-Filterleiste auf MON-01** - Schnelles Umschalten zwischen Grenzen, Kraftwerken, Dämmen und Pipelines.

---

## Domain 9: MON-01 / MON-02 Synchronisations- & Taktik-Steuerung (F-137 - F-153)

*Die nahtlose Kommando-Brücke zwischen Kartenauswahl auf MON-01 und Tiefenanalyse auf MON-02.*

- **F-137** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Bidirektionale MON-01 / MON-02 Node-Kopplung** - Klick auf eine beliebige Node auf der MON-01-Karte schaltet MON-02 sofort und ohne Verzögerung auf den entsprechenden Node-Deep-Dive um.
- **F-138** `[WEB-EDITION]` `[OSINT]`: **Hierarchischer Layer-Manager auf MON-01** - Ausklappbares Baum-Menü auf der Karte mit Gruppen: *Cyber/Seekabel*, *Katastrophen*, *Weltraum*, *Umwelt/Strahlung*, *Luftfahrt*, *Maritim*, *Funk/SDR*, *Infrastruktur*.
- **F-139** `[WEB-EDITION]` `[OSINT]`: **Stufenloser Layer-Transparenz-Schieberegler** - Erlaubt die Feinjustierung der Deckkraft jedes einzelnen Overlays über der Basiskarte auf MON-01.
- **F-140** `[WEB-EDITION]` `[OSINT]`: **Aktive Layer-Zähler & Master-Toggle auf MON-01** - Zeigt im Header die Anzahl aktiver Ebenen an (z. B. `[6 LAYER AKTIV]`) mit Ein-Klick-Ausschalter.
- **F-141** `[WEB-EDITION]` `[OSINT]`: **Hochleistungs-Vektor-Cluster-Rendering** - Fasst dichte Marker (z. B. 2.400 Webcams oder 7.500 Tor-Knoten) beim Herauszoomen zu flüssigen Clustern zusammen.
- **F-142** `[WEB-EDITION]` `[OSINT]`: **Floating Picture-in-Picture (PiP) Kamera-Player** - Löst den MON-02-Feed als frei verschiebbares Miniaturfenster über der MON-01-Karte ab.
- **F-143** `[WEB-EDITION]` `[OSINT]`: **Dual-Viewport Split-Screen Modus auf MON-01** - Vertikaler Schieber zum direkten Vorher-Nachher-Vergleich (z. B. Satellit vs. Doppler-Radar).
- **F-144** `[WEB-EDITION]` `[OSINT]`: **Karten-Basisschichten-Schnellwechsler auf MON-01** - Schaltet nahtlos zwischen Dark Cyberpunk, ESRI World Satellite, Topografie und OpenStreetMap um.
- **F-145** `[WEB-EDITION]` `[OSINT]`: **Vollbild-Kartenmodus (F11)** - Schaltet MON-01 auf volle Bildschirmgröße ohne störende Rahmen für Lagezentren und Beamer.
- **F-146** `[WEB-EDITION]` `[OSINT]`: **Taktischer Fadenkreuz- & Koordinaten-Retikel** - Zeigt im Fadenkreuz permanent Breiten-/Längengrad und Geländehöhe des Kartenzentrums an.
- **F-147** `[WEB-EDITION]` `[OSINT]`: **Kompass-Rose & Richtungs-Anzeige auf MON-01** - Zeigt Karten-Drehung und Ausrichtung zum geografischen Nordpol.
- **F-148** `[WEB-EDITION]` `[OSINT]`: **Globaler Audio-Mute Schalter** - Ein Klick schaltet alle akustischen Signale (Sirenen, Geigerzähler, WebSDR-Audio, Radar-Beeps) stumm.
- **F-149** `[WEB-EDITION]` `[OSINT]`: **High-Contrast Night Recon OLED Theme** - Reines Schwarz (`#000000`) für blendfreie Arbeit bei Nachteinsätzen.
- **F-150** `[WEB-EDITION]` `[OSINT]`: **MGRS / UTM Gitter-Overlay auf MON-01** - Zeichnet wahlweise das 100km- oder 10km-Militär-Gitter direkt über das Gelände.
- **F-151** `[WEB-EDITION]` `[OSINT]`: **Karten-Lesezeichen & Schnell-Sprungmarken** - Speichert Lieblingskoordinaten (z. B. Hormus, Taiwan-Straße, Berlin, New York) für 1-Klick-Fokus.
- **F-152** `[WEB-EDITION]` `[OSINT]`: **Panik-Schutz-Taste (Boss Key)** - `Ctrl+Shift+X` schaltet den Bildschirm blitzschnell auf ein neutrales Dokument um.
- **F-153** `[WEB-EDITION]` `[OSINT]`: **Layer-Konfiguration Speichern & Laden** - Sichert die aktuelle Auswahl aktiver Ebenen im Browser-Speicher für spätere Sitzungen.

---

## Domain 10: OSINT Feld-Werkzeuge, Rechner & Geo-Exporte (F-154 - F-170)

*Foto-Geolokalisierung, Sonnenstand, Schattenlängen, Koordinaten-Konverter und GIS-Exporte.*

- **F-154** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Sonnen- & Schattenwinkel Foto-Geolokalisierungs-Rechner** - Berechnet für jedes Datum und jeden Ort den exakten Sonnenstand (Azimut und Elevation) und die Schattenlänge bekannter Objekte: $L = \frac{h}{\tan(\theta)}$.
- **F-155** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Dämmerungs- & Dunkelheits-Rechner** - Berechnet Sonnenaufgang, Sonnenuntergang, Goldene Stunde und absolute Dunkelheitsphasen für Aufklärungseinsätze.
- **F-156** `[WEB-EDITION]` `[OSINT]` `[EXE/APK]`: **Militär- & Taktik-Koordinaten-Konverter Tool**:
  - Dezimalgrad (DD: `52.5200, 13.4050`)
  - Grad Minuten Sekunden (DMS: `52°31'12"N, 13°24'18"E`)
  - UTM (Universal Transverse Mercator: `33U 391820 5820120`)
  - MGRS (Military Grid Reference System: `33UUU9182020120`)
  - Maidenhead QTH Locator (`JO62qn`).
- **F-157** `[WEB-EDITION]` `[OSINT]`: **Großkreis-Distanz- & Peilungs-Werkzeug** - Misst exakte Luftlinien-Entfernung in km, Meilen und Seemeilen inklusive Kompasskurs.
- **F-158** `[WEB-EDITION]` `[OSINT]`: **Funkhorizont & Sichtlinien-Rechner** - Berechnet maximale Sichtweite zweier Punkte über Erdkrümmung: $d \approx 4,12 \times (\sqrt{h_1} + \sqrt{h_2})$.
- **F-159** `[WEB-EDITION]` `[OSINT]`: **Aviation METAR/TAF Rohcode Dekoder** - Schnelleingabe beliebiger METAR-Zeichenketten mit sofortiger Klartextübersetzung.
- **F-160** `[WEB-EDITION]` `[OSINT]`: **Seismischer P- und S-Wellen Ankunftszeit-Rechner** - Berechnet Vorwarnzeit und Eintreffen der zerstörerischen Scherwellen am Standort des Nutzers.
- **F-161** `[WEB-EDITION]` `[OSINT]`: **Doppler-Windvektor Zerlegungswerkzeug** - Rechnet Radialgeschwindigkeiten in wahren Windvektor um: $V_{\text{true}} = \frac{V_r}{\cos(\theta - \phi)}$.
- **F-162** `[WEB-EDITION]` `[OSINT]`: **Fahrtzeit- & Distanz-Rechner** - Ermittelt benötigte Reisezeiten bei vorgegebener Geschwindigkeit in Knoten, km/h oder mph.
- **F-163** `[WEB-EDITION]` `[OSINT]`: **Taktischer Radien-Generator auf MON-01** - Klick auf einen Kartenpunkt zeichnet konzentrische Sperr- und Sicherheitsringe (1km, 5km, 10km, 25km, 50km).
- **F-164** `[WEB-EDITION]` `[OSINT]`: **Polygon-Flächen- & Umfangs-Messwerkzeug** - Ermöglicht das Zeichnen von Suchgebieten mit automatischer Flächenberechnung in $\text{km}^2$ und Hektar.
- **F-165** `[WEB-EDITION]` `[OSINT]`: **Ein-Klick GeoJSON Karten-Export** - Exportiert alle aktuell sichtbaren Kartenebenen, Seekabel und Sensoren als GeoJSON für QGIS und ArcGIS.
- **F-166** `[WEB-EDITION]` `[OSINT]`: **KML / KMZ Export für Google Earth** - Exportiert Flugbahnen, Satellitenspuren und Gefahrenzonen als 3D-KML.
- **F-167** `[WEB-EDITION]` `[OSINT]`: **CSV Sensor-Daten Export** - Exportiert sichtbare Sensortabellen (Erdbeben, Pegel, Wetter) als saubere Tabellen-Datei.
- **F-168** `[WEB-EDITION]` `[OSINT]`: **Hochauflösender Taktischer Screenshot-Generator** - Erzeugt einen hochauflösenden PNG-Kartenausschnitt mit Zeitstempel, Koordinaten und Klassifizierungsbanner.
- **F-169** `[WEB-EDITION]` `[OSINT]`: **Offline-Lagebild Snapshot-Paketierer** - Bündelt den aktuellen Kartenausschnitt samt Daten in eine autarke HTML-Datei für den Feldeinsatz ohne Internet.
- **F-170** `[WEB-EDITION]` `[OSINT]`: **Missions-Fallakten Manager (Case Files)** - Speichert vollständige Ermittlungssitzungen (aktive Layer, Markierungen, Notizen und Kamera-Favoriten).

---

## 📊 Zusammenfassung der v2.1.0 Architektur
* **Gesamtanzahl neuer Features:** **170 Features** (F-001 bis F-170)
* **Karten- & Inspektions-Architektur:**
  * **MON-01 = Tactical Global Map:** Trägt alle zuschaltbaren Vektor- und Raster-Layers (Seekabel, AIS Schiffe, Flugzeuge, Katastrophen, Strahlung, WebSDRs, Grenzen).
  * **MON-02 = Deep-Dive Inspector:** Empfängt Klicks von MON-01 und liefert die detaillierte forensische Untersuchung der ausgewählten Node (Live-Kamera/Stream, Spezifikationen, Sensor-Diagramme, UN-Lageberichte, Frequenz-Audio).
* **Keine unnötigen neuen Monitore:** Keine Dummy-Cards; das bestehende Monitor-Layout bleibt schlank und aufgeräumt.
* **Web-Edition Kompatibilität:** **Über 130 Features speziell mit `[WEB-EDITION]` gekennzeichnet**
* **Self-Hosted Core & Desktop/APK:** **Alle 170 Features uneingeschränkt nutzbar**
* **Zero-Fake Richtlinie:** 100% echte, verifizierte offene Daten — keinerlei Fake-Simulationen oder Dummy-Platzhalter!
