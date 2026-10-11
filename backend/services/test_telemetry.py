"""
Comprehensive verification test for TelemetryEngine.
Tests all 5 telemetry feeds, caching, fallbacks, and unified snapshot.
"""
import asyncio
import json
import sys
import time

from telemetry_engine import TelemetryEngine, get_telemetry_engine


async def test_all():
    print("=" * 70)
    print("CYBER-SPECTRE-NEXUS: TELEMETRY ENGINE VERIFICATION")
    print("=" * 70)

    engine = TelemetryEngine()
    try:
        # Test 1: ISS Telemetry
        print("\n[TEST 1] Orbital Surveillance (ISS)...")
        t0 = time.time()
        iss = await engine.get_iss_telemetry()
        t1 = time.time()
        print(f"  -> Source: {iss.get('source')}, Time: {(t1 - t0)*1000:.1f}ms")
        print(f"  -> Lat: {iss['latitude']}, Lon: {iss['longitude']}, Alt: {iss['altitude_km']} km, Vel: {iss['velocity_kmh']} km/h")
        print(f"  -> Visibility: {iss['visibility']}, Solar Lat/Lon: {iss['solar_latitude']} / {iss['solar_longitude']}")
        print(f"  -> Video Stream: YouTube ID: {iss['video_stream']['youtube_id']}, Status: {iss['video_stream']['status']}")
        assert "latitude" in iss and "longitude" in iss and "video_stream" in iss
        print("  [PASS] ISS Telemetry verified.")

        # Test 2: Caching of ISS
        print("\n[TEST 2] ISS Caching Mechanism...")
        t0 = time.time()
        iss_cached = await engine.get_iss_telemetry()
        t1 = time.time()
        print(f"  -> Source: {iss_cached.get('source')}, Cache Time: {(t1 - t0)*1000:.2f}ms")
        assert iss_cached.get("source") == "cache"
        print("  [PASS] Cache hit confirmed.")

        # Test 3: ADS-B Flight Tracking
        print("\n[TEST 3] Live ADS-B Flight Tracking (OpenSky)...")
        t0 = time.time()
        flights = await engine.get_flight_tracking(limit=15)
        t1 = time.time()
        print(f"  -> Source: {flights.get('source')}, Provider: {flights.get('provider')}, Time: {(t1 - t0)*1000:.1f}ms")
        print(f"  -> Active Aircraft Count: {flights['count']}")
        if flights["flights"]:
            sample = flights["flights"][0]
            print(f"  -> Sample Flight: ICAO24: {sample['icao24']}, Callsign: '{sample['callsign']}', "
                  f"Country: {sample['origin_country']}, Pos: ({sample['latitude']}, {sample['longitude']}), "
                  f"Alt: {sample['baro_altitude_m']}m ({sample['baro_altitude_ft']}ft), Vel: {sample['velocity_kts']}kts")
            assert "icao24" in sample and "callsign" in sample and "baro_altitude_m" in sample
        print("  [PASS] Flight Tracking verified.")

        # Test 4: Seismic Earthquakes
        print("\n[TEST 4] Global Seismic Feed (USGS)...")
        t0 = time.time()
        quakes = await engine.get_earthquake_feed(feed="all_hour")
        t1 = time.time()
        print(f"  -> Source: {quakes.get('source')}, Feed: {quakes.get('feed_type')}, Time: {(t1 - t0)*1000:.1f}ms")
        print(f"  -> Quake Count: {quakes['count']}, Tsunami Warnings: {quakes['tsunami_warnings']}")
        if quakes["features"]:
            q0 = quakes["features"][0]
            print(f"  -> Sample Quake: M{q0['magnitude']} - {q0['place']} @ {q0['depth_km']}km depth (Tsunami: {q0['tsunami_alert']})")
            assert "magnitude" in q0 and "place" in q0 and "depth_km" in q0
        print("  [PASS] Earthquake feed verified.")

        # Test 5: Wildfire & Thermal Hotspots
        print("\n[TEST 5] NASA FIRMS / EONET Wildfires...")
        t0 = time.time()
        wildfires = await engine.get_wildfire_hotspots(limit=10)
        t1 = time.time()
        print(f"  -> Source: {wildfires.get('source')}, Provider: {wildfires.get('provider')}, Time: {(t1 - t0)*1000:.1f}ms")
        print(f"  -> Hotspots Count: {wildfires['count']}")
        if wildfires["hotspots"]:
            w0 = wildfires["hotspots"][0]
            print(f"  -> Sample Hotspot: {w0['title']} @ ({w0['latitude']}, {w0['longitude']}) - Conf: {w0['confidence']}")
            assert "latitude" in w0 and "longitude" in w0 and "title" in w0
        print("  [PASS] Wildfire hotspots verified.")

        # Test 6: Cyber Threat Intelligence Radar
        print("\n[TEST 6] Cyber Threat Intelligence Radar (Honeypot Attack Stream)...")
        t0 = time.time()
        cyber = engine.get_cyber_threat_radar(count=20)
        t1 = time.time()
        print(f"  -> Source: {cyber.get('source')}, Time: {(t1 - t0)*1000:.2f}ms")
        print(f"  -> Generated Attacks: {len(cyber['events'])}, Defcon: {cyber['summary_stats']['global_defcon_level']}")
        print(f"  -> Critical Count: {cyber['summary_stats']['critical_count']}, Top Attack: {cyber['summary_stats']['top_attack_type']}")
        sample_atk = cyber["events"][0]
        print(f"  -> Sample Attack: [{sample_atk['severity']}] {sample_atk['attack_type']} ({sample_atk['mitre_id']})")
        print(f"     From: {sample_atk['source']['country']} ({sample_atk['source']['ip']}, {sample_atk['source']['actor_attribution']})")
        print(f"     To:   {sample_atk['target']['organization']} in {sample_atk['target']['city']}, {sample_atk['target']['country']} ({sample_atk['target']['sector']})")
        print(f"     Port: {sample_atk['target_port']} / {sample_atk['protocol']} | Rate: {sample_atk['bandwidth_volume']} | Status: {sample_atk['status']}")
        assert "source" in sample_atk and "target" in sample_atk and "attack_type" in sample_atk
        print("  [PASS] Cyber Threat Radar verified.")

        # Test 7: Unified Concurrent Telemetry Snapshot
        print("\n[TEST 7] Unified Telemetry Snapshot (All feeds concurrently)...")
        t0 = time.time()
        snapshot = await engine.get_all_telemetry_snapshot()
        t1 = time.time()
        print(f"  -> System Status: {snapshot['status']}")
        print(f"  -> Total Parallel Latency: {snapshot['telemetry_sync_time_ms']}ms (wall-clock: {(t1 - t0)*1000:.1f}ms)")
        print(f"  -> Feed Health: {json.dumps(snapshot['feed_health'])}")
        assert snapshot["status"] == "ALL_SYSTEMS_OPERATIONAL"
        assert len(snapshot["feeds"]) == 5
        print("  [PASS] Unified Telemetry Snapshot verified.")

        # Test 8: Fallback verification
        print("\n[TEST 8] Fallback Systems Verification...")
        fallback_iss = engine._generate_iss_fallback()
        assert fallback_iss["source"] == "fallback_orbital_model"
        print(f"  -> Dead-reckoning ISS: ({fallback_iss['latitude']}, {fallback_iss['longitude']}) - {fallback_iss['visibility']}")

        fallback_flights = engine._generate_flights_fallback(limit=5)
        assert fallback_flights["source"] == "fallback_synthetic"
        print(f"  -> Synthetic Flights Count: {fallback_flights['count']}")

        fallback_quakes = engine._generate_earthquake_fallback()
        assert fallback_quakes["source"] == "fallback_simulation"
        print(f"  -> Synthetic Quakes Count: {fallback_quakes['count']}")

        fallback_fires = engine._generate_wildfire_fallback(limit=5)
        assert fallback_fires["source"] == "fallback_simulation"
        print(f"  -> Synthetic Wildfires Count: {fallback_fires['count']}")
        print("  [PASS] Fallbacks successfully verified.")

        print("\n" + "=" * 70)
        print(">>> ALL TESTS PASSED SUCCESSFULLY! TELEMETRY ENGINE READY <<<")
        print("=" * 70)

    finally:
        await engine.close()

if __name__ == "__main__":
    asyncio.run(test_all())
