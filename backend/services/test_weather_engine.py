"""
Test suite for WeatherEngine service.
Verifies station indexing, pagination, live Open-Meteo queries, caching,
RainViewer radar frames, and NOAA severe storm alert processing.
"""

import os
import sys
import time

# Ensure backend directory is in python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.weather_engine import WeatherEngine

def run_tests():
    print("==================================================")
    print("CYBER-SPECTRE-NEXUS: WEATHER ENGINE TEST HARNESS")
    print("==================================================")

    engine = WeatherEngine()

    # TEST 1: Station count verification
    total_stations = len(engine.stations)
    print(f"\n[TEST 1] Weather Stations Database Count:")
    print(f"  Total stations loaded: {total_stations}")
    assert total_stations >= 4300, f"Expected at least 4300 stations, got {total_stations}"
    print("  --> PASS: 4,300+ stations requirement satisfied!")

    # TEST 2: Station types and coverage
    type_counts = {}
    continent_counts = {}
    for s in engine.stations:
        type_counts[s["type"]] = type_counts.get(s["type"], 0) + 1
        continent_counts[s["continent"]] = continent_counts.get(s["continent"], 0) + 1

    print(f"\n[TEST 2] Station Breakdown by Type:")
    for t, cnt in type_counts.items():
        print(f"  - {t}: {cnt}")
    assert "airport_metar" in type_counts and type_counts["airport_metar"] > 1000
    assert "wmo" in type_counts and type_counts["wmo"] > 1000
    assert "storm_chaser_post" in type_counts and type_counts["storm_chaser_post"] >= 50
    assert "coastal_station" in type_counts and type_counts["coastal_station"] >= 30
    print("  --> PASS: All 4 required types represented with rich global coverage!")

    print(f"\n[TEST 2b] Continent Distribution:")
    for c, cnt in continent_counts.items():
        print(f"  - {c}: {cnt}")

    # TEST 3: Station querying & pagination
    print(f"\n[TEST 3] Pagination & Search Filtering:")
    # Paging
    page1 = engine.get_weather_stations(limit=5, offset=0)
    assert len(page1["stations"]) == 5
    assert page1["total"] == total_stations
    print(f"  Page 1 limit=5 returned {len(page1['stations'])} stations.")

    # Country filter
    de_stations = engine.get_weather_stations(country="Germany", limit=10)
    print(f"  Germany stations found: {de_stations['total']} (Sample: {de_stations['stations'][0]['name']})")
    assert de_stations["total"] > 50

    # Query search
    query_res = engine.get_weather_stations(query="Tornado", limit=5)
    print(f"  Query 'Tornado' matching stations: {query_res['total']}")

    # Lookup by ID
    station_norman = engine.get_station_by_id("storm_nssl_spc_ok")
    assert station_norman is not None
    print(f"  Direct ID lookup 'storm_nssl_spc_ok': {station_norman['name']} ({station_norman['country']})")
    print("  --> PASS: Pagination and filtering functional!")

    # TEST 4: Spatial nearest station lookup
    print(f"\n[TEST 4] Spatial Proximity Search:")
    okc_lat, okc_lon = 35.4676, -97.5164 # Oklahoma City
    nearest_okc = engine.find_nearest_stations(okc_lat, okc_lon, limit=3)
    print(f"  Nearest stations to Oklahoma City ({okc_lat}, {okc_lon}):")
    for st in nearest_okc:
        print(f"    - {st['name']} ({st['type']}): {st['distance_km']} km, bearing {st['bearing_compass']} ({st['bearing_deg']}°)")
    assert len(nearest_okc) == 3
    print("  --> PASS: Spatial indexing functional!")

    # TEST 5: Live Open-Meteo Weather with 5-min TTL Cache
    print(f"\n[TEST 5] Live Weather Telemetry (Open-Meteo):")
    t0 = time.time()
    live1 = engine.get_live_weather(52.52, 13.41) # Berlin
    t1 = time.time()
    print(f"  Network fetch took: {round((t1 - t0) * 1000, 1)} ms")
    print(f"  Cached flag: {live1.get('cached')}")
    print(f"  Temperature: {live1.get('temperature_c')}°C ({live1.get('temperature_f')}°F)")
    print(f"  Relative Humidity: {live1.get('relative_humidity')}%")
    print(f"  Wind: {live1.get('wind_speed_kmh')} km/h ({live1.get('wind_speed_knots')} kts) from {live1.get('wind_direction_compass')}")
    print(f"  Wind Gusts: {live1.get('wind_gusts_kmh')} km/h")
    print(f"  Surface Pressure: {live1.get('surface_pressure_hpa')} hPa")
    print(f"  Precipitation: {live1.get('precipitation_mm')} mm")
    print(f"  Weather Condition: {live1.get('weather_condition')} - '{live1.get('weather_description')}' (code: {live1.get('weather_code')})")

    assert live1.get("temperature_c") is not None
    assert live1.get("wind_speed_kmh") is not None
    assert live1.get("surface_pressure_hpa") is not None
    assert live1.get("weather_code") is not None

    # Test cache hit (TTL 5 mins)
    t2 = time.time()
    live_cached = engine.get_live_weather(52.52, 13.41)
    t3 = time.time()
    cache_duration_ms = round((t3 - t2) * 1000, 3)
    print(f"  Second fetch (Cache Hit) took: {cache_duration_ms} ms")
    print(f"  Cached flag: {live_cached.get('cached')}, Cache age: {live_cached.get('cache_age_seconds')}s")
    assert live_cached.get("cached") is True
    assert cache_duration_ms < 10.0 # Under 10ms
    print("  --> PASS: Live weather and in-memory TTL caching functional!")

    # TEST 6: RainViewer Doppler Radar Tiles
    print(f"\n[TEST 6] RainViewer Doppler Radar API:")
    radar = engine.get_radar_tiles()
    print(f"  Host: {radar.get('host')}")
    print(f"  Radar past frames count: {len(radar.get('radar_past', []))}")
    print(f"  Radar nowcast frames count: {len(radar.get('radar_nowcast', []))}")
    print(f"  Satellite infrared frames count: {len(radar.get('satellite_infrared', []))}")
    print(f"  Latest radar timestamp: {radar.get('latest_radar_time')}")
    print(f"  Latest tile URL template: {radar.get('latest_radar_tile_url')}")
    assert len(radar.get("radar_past", [])) > 0
    assert radar.get("host") is not None
    print("  --> PASS: RainViewer radar integration functional!")

    # TEST 7: NOAA Active Severe Alerts
    print(f"\n[TEST 7] NOAA Active Severe Alerts API:")
    alerts = engine.get_severe_alerts()
    print(f"  Total active alerts in USA: {alerts.get('total_alerts')}")
    print(f"  Counts by severity: {alerts.get('counts_by_severity')}")
    print(f"  Counts by category: {alerts.get('counts_by_category')}")
    if alerts.get("alerts"):
        sample_alert = alerts["alerts"][0]
        print(f"  Sample alert: [{sample_alert.get('severity')}] {sample_alert.get('event')} - {sample_alert.get('headline')}")
    assert "total_alerts" in alerts
    print("  --> PASS: NOAA active alerts integration functional!")

    print("\n==================================================")
    print("ALL 7 WEATHER ENGINE UNIT TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
