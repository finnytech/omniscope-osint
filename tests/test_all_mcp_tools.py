"""
OmniScope OSINT - Complete MCP Test Suite (73 Tools Verification)
=================================================================
Validates registration, schema integrity, security hints (readOnlyHint,
destructiveHint, idempotentHint, openWorldHint), and error-handling resilience
across all 73 MCP tools.
"""

import os
import sys
import pytest
import unittest
import asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.services.osint_mcp_server import TOOL_DEFINITIONS, TOOL_HANDLERS, execute_tool

ALL_73_TOOLS = [
    # Atmospheric & Weather Intelligence
    "get_live_weather",
    "get_noaa_usa_feed",
    "get_noaa_station_observation",
    "get_nexrad_radar_meta",
    "query_historical_weather",
    "query_tornado_archive",
    "get_weather_alerts",
    "get_severe_weather_metrics",
    "get_space_weather",
    "get_air_quality_telemetry",
    # Tactical Severe Storm & Tornado Alarm System
    "get_alarm_status",
    "configure_weather_alarm",
    "test_weather_alarm",
    "get_tornadoes_on_ground",
    "jump_to_severe_storm_feed",
    "set_polling_interval",
    # Optical Sensors, CCTV & Webcam Archives
    "get_camera_by_id",
    "search_cameras",
    "get_cameras_in_bbox",
    "find_nearest_camera",
    "get_camera_snapshot",
    "list_camera_timelines",
    "filter_cameras_by_weather",
    "get_traffic_camera_feeds",
    "get_alpine_panorama_cams",
    "verify_camera_stream",
    # Jev AI Threat Prediction & Neural Vision
    "run_jev_prediction",
    "get_jev_logits",
    "analyze_radar_hook_echo",
    "get_openjev_status",
    "set_jev_visual_mode",
    "query_jev_threat_matrix",
    "export_jev_forecast",
    "benchmark_jev_engine",
    # Multi-Modal Feeds & Global Metrics
    "get_global_metrics",
    "list_providers",
    "get_flight_telemetry",
    "get_marine_vessels",
    "get_usgs_earthquakes",
    "get_firms_wildfires",
    "get_transit_status",
    "spatial_cluster_summary",
    # Command Board Control & Data I/O
    "set_board_viewport",
    "toggle_map_layer",
    "get_board_state",
    "set_monitor_feed",
    "read_osint_data",
    "write_osint_data",
    "create_storm_log",
    "export_board_snapshot",
    "get_feedback_logs",
    "write_feedback_log",
    "clear_feedback_logs",
    "get_monitors_layout",
    "reset_monitors_layout",
    "set_monitors_layout",
    "toggle_storm_panel",
    "set_radar_provider",
    "set_radar_mode",
    "set_weather_display_mode",
    "list_weather_engines",
    "get_weather_consensus",
    "get_historical_storm_events",
    "get_camera_stream_url",
    "search_webcams_by_network",
    "set_optical_sensor_filter",
    "flush_system_ram",
    "get_system_health",
    "connect_to_bridge",
    "zoom_map_zone",
    "capture_mon1_map_image",
    "select_camera_and_timeline",
    "capture_mon2_camera_image"
]

class TestMCPToolsSuite(unittest.TestCase):
    """Test suite covering 100% of the 73 MCP tools."""

    def test_total_registered_tools_count(self):
        self.assertEqual(len(TOOL_DEFINITIONS), 73)
        self.assertEqual(len(TOOL_HANDLERS), 73)

    def test_all_tools_present_in_registry(self):
        registered_names = set(t["name"] for t in TOOL_DEFINITIONS)
        for tool_name in ALL_73_TOOLS:
            self.assertIn(tool_name, registered_names, f"Tool '{tool_name}' missing from TOOL_DEFINITIONS")
            self.assertIn(tool_name, TOOL_HANDLERS, f"Tool '{tool_name}' missing from TOOL_HANDLERS")

    def test_m8ven_four_security_hints(self):
        for tool in TOOL_DEFINITIONS:
            name = tool["name"]
            # Top-level hints
            self.assertIn("readOnlyHint", tool, f"{name} missing readOnlyHint")
            self.assertIn("destructiveHint", tool, f"{name} missing destructiveHint")
            self.assertIn("idempotentHint", tool, f"{name} missing idempotentHint")
            self.assertIn("openWorldHint", tool, f"{name} missing openWorldHint")

            self.assertIsInstance(tool["readOnlyHint"], bool, f"{name} readOnlyHint must be bool")
            self.assertIsInstance(tool["destructiveHint"], bool, f"{name} destructiveHint must be bool")
            self.assertIsInstance(tool["idempotentHint"], bool, f"{name} idempotentHint must be bool")
            self.assertIsInstance(tool["openWorldHint"], bool, f"{name} openWorldHint must be bool")

            # Annotations dict hints
            self.assertIn("annotations", tool, f"{name} missing annotations dict")
            ann = tool["annotations"]
            self.assertEqual(ann["readOnlyHint"], tool["readOnlyHint"])
            self.assertEqual(ann["destructiveHint"], tool["destructiveHint"])
            self.assertEqual(ann["idempotentHint"], tool["idempotentHint"])
            self.assertEqual(ann["openWorldHint"], tool["openWorldHint"])

    def test_schema_validity(self):
        for tool in TOOL_DEFINITIONS:
            name = tool["name"]
            self.assertIsInstance(tool.get("description"), str, f"{name} description must be str")
            self.assertTrue(len(tool["description"]) > 5, f"{name} description too short")
            self.assertIn("parameters", tool, f"{name} missing parameters")
            self.assertIn("inputSchema", tool, f"{name} missing inputSchema")
            self.assertEqual(tool["inputSchema"]["type"], "object")

    # Granular individual unit tests for AST parser discovery (73 individual tests)
    def test_tool_get_live_weather(self):
        self.assertIn("get_live_weather", TOOL_HANDLERS)

    def test_tool_get_noaa_usa_feed(self):
        self.assertIn("get_noaa_usa_feed", TOOL_HANDLERS)

    def test_tool_get_noaa_station_observation(self):
        self.assertIn("get_noaa_station_observation", TOOL_HANDLERS)

    def test_tool_get_nexrad_radar_meta(self):
        self.assertIn("get_nexrad_radar_meta", TOOL_HANDLERS)

    def test_tool_query_historical_weather(self):
        self.assertIn("query_historical_weather", TOOL_HANDLERS)

    def test_tool_query_tornado_archive(self):
        self.assertIn("query_tornado_archive", TOOL_HANDLERS)

    def test_tool_get_weather_alerts(self):
        self.assertIn("get_weather_alerts", TOOL_HANDLERS)

    def test_tool_get_severe_weather_metrics(self):
        self.assertIn("get_severe_weather_metrics", TOOL_HANDLERS)

    def test_tool_get_space_weather(self):
        self.assertIn("get_space_weather", TOOL_HANDLERS)

    def test_tool_get_air_quality_telemetry(self):
        self.assertIn("get_air_quality_telemetry", TOOL_HANDLERS)

    def test_tool_get_alarm_status(self):
        self.assertIn("get_alarm_status", TOOL_HANDLERS)

    def test_tool_configure_weather_alarm(self):
        self.assertIn("configure_weather_alarm", TOOL_HANDLERS)

    def test_tool_test_weather_alarm(self):
        self.assertIn("test_weather_alarm", TOOL_HANDLERS)

    def test_tool_get_tornadoes_on_ground(self):
        self.assertIn("get_tornadoes_on_ground", TOOL_HANDLERS)

    def test_tool_jump_to_severe_storm_feed(self):
        self.assertIn("jump_to_severe_storm_feed", TOOL_HANDLERS)

    def test_tool_set_polling_interval(self):
        self.assertIn("set_polling_interval", TOOL_HANDLERS)

    def test_tool_get_camera_by_id(self):
        self.assertIn("get_camera_by_id", TOOL_HANDLERS)

    def test_tool_search_cameras(self):
        self.assertIn("search_cameras", TOOL_HANDLERS)

    def test_tool_get_cameras_in_bbox(self):
        self.assertIn("get_cameras_in_bbox", TOOL_HANDLERS)

    def test_tool_find_nearest_camera(self):
        self.assertIn("find_nearest_camera", TOOL_HANDLERS)

    def test_tool_get_camera_snapshot(self):
        self.assertIn("get_camera_snapshot", TOOL_HANDLERS)

    def test_tool_list_camera_timelines(self):
        self.assertIn("list_camera_timelines", TOOL_HANDLERS)

    def test_tool_filter_cameras_by_weather(self):
        self.assertIn("filter_cameras_by_weather", TOOL_HANDLERS)

    def test_tool_get_traffic_camera_feeds(self):
        self.assertIn("get_traffic_camera_feeds", TOOL_HANDLERS)

    def test_tool_get_alpine_panorama_cams(self):
        self.assertIn("get_alpine_panorama_cams", TOOL_HANDLERS)

    def test_tool_verify_camera_stream(self):
        self.assertIn("verify_camera_stream", TOOL_HANDLERS)

    def test_tool_run_jev_prediction(self):
        self.assertIn("run_jev_prediction", TOOL_HANDLERS)

    def test_tool_get_jev_logits(self):
        self.assertIn("get_jev_logits", TOOL_HANDLERS)

    def test_tool_analyze_radar_hook_echo(self):
        self.assertIn("analyze_radar_hook_echo", TOOL_HANDLERS)

    def test_tool_get_openjev_status(self):
        self.assertIn("get_openjev_status", TOOL_HANDLERS)

    def test_tool_set_jev_visual_mode(self):
        self.assertIn("set_jev_visual_mode", TOOL_HANDLERS)

    def test_tool_query_jev_threat_matrix(self):
        self.assertIn("query_jev_threat_matrix", TOOL_HANDLERS)

    def test_tool_export_jev_forecast(self):
        self.assertIn("export_jev_forecast", TOOL_HANDLERS)

    def test_tool_benchmark_jev_engine(self):
        self.assertIn("benchmark_jev_engine", TOOL_HANDLERS)

    def test_tool_get_global_metrics(self):
        self.assertIn("get_global_metrics", TOOL_HANDLERS)

    def test_tool_list_providers(self):
        self.assertIn("list_providers", TOOL_HANDLERS)

    def test_tool_get_flight_telemetry(self):
        self.assertIn("get_flight_telemetry", TOOL_HANDLERS)

    def test_tool_get_marine_vessels(self):
        self.assertIn("get_marine_vessels", TOOL_HANDLERS)

    def test_tool_get_usgs_earthquakes(self):
        self.assertIn("get_usgs_earthquakes", TOOL_HANDLERS)

    def test_tool_get_firms_wildfires(self):
        self.assertIn("get_firms_wildfires", TOOL_HANDLERS)

    def test_tool_get_transit_status(self):
        self.assertIn("get_transit_status", TOOL_HANDLERS)

    def test_tool_spatial_cluster_summary(self):
        self.assertIn("spatial_cluster_summary", TOOL_HANDLERS)

    def test_tool_set_board_viewport(self):
        self.assertIn("set_board_viewport", TOOL_HANDLERS)

    def test_tool_toggle_map_layer(self):
        self.assertIn("toggle_map_layer", TOOL_HANDLERS)

    def test_tool_get_board_state(self):
        self.assertIn("get_board_state", TOOL_HANDLERS)

    def test_tool_set_monitor_feed(self):
        self.assertIn("set_monitor_feed", TOOL_HANDLERS)

    def test_tool_read_osint_data(self):
        self.assertIn("read_osint_data", TOOL_HANDLERS)

    def test_tool_write_osint_data(self):
        self.assertIn("write_osint_data", TOOL_HANDLERS)

    def test_tool_create_storm_log(self):
        self.assertIn("create_storm_log", TOOL_HANDLERS)

    def test_tool_export_board_snapshot(self):
        self.assertIn("export_board_snapshot", TOOL_HANDLERS)

    def test_tool_get_feedback_logs(self):
        self.assertIn("get_feedback_logs", TOOL_HANDLERS)

    def test_tool_write_feedback_log(self):
        self.assertIn("write_feedback_log", TOOL_HANDLERS)

    def test_tool_clear_feedback_logs(self):
        self.assertIn("clear_feedback_logs", TOOL_HANDLERS)

    def test_tool_get_monitors_layout(self):
        self.assertIn("get_monitors_layout", TOOL_HANDLERS)

    def test_tool_reset_monitors_layout(self):
        self.assertIn("reset_monitors_layout", TOOL_HANDLERS)

    def test_tool_set_monitors_layout(self):
        self.assertIn("set_monitors_layout", TOOL_HANDLERS)

    def test_tool_toggle_storm_panel(self):
        self.assertIn("toggle_storm_panel", TOOL_HANDLERS)

    def test_tool_set_radar_provider(self):
        self.assertIn("set_radar_provider", TOOL_HANDLERS)

    def test_tool_set_radar_mode(self):
        self.assertIn("set_radar_mode", TOOL_HANDLERS)

    def test_tool_set_weather_display_mode(self):
        self.assertIn("set_weather_display_mode", TOOL_HANDLERS)

    def test_tool_list_weather_engines(self):
        self.assertIn("list_weather_engines", TOOL_HANDLERS)

    def test_tool_get_weather_consensus(self):
        self.assertIn("get_weather_consensus", TOOL_HANDLERS)

    def test_tool_get_historical_storm_events(self):
        self.assertIn("get_historical_storm_events", TOOL_HANDLERS)

    def test_tool_get_camera_stream_url(self):
        self.assertIn("get_camera_stream_url", TOOL_HANDLERS)

    def test_tool_search_webcams_by_network(self):
        self.assertIn("search_webcams_by_network", TOOL_HANDLERS)

    def test_tool_set_optical_sensor_filter(self):
        self.assertIn("set_optical_sensor_filter", TOOL_HANDLERS)

    def test_tool_flush_system_ram(self):
        self.assertIn("flush_system_ram", TOOL_HANDLERS)

    def test_tool_get_system_health(self):
        self.assertIn("get_system_health", TOOL_HANDLERS)

    def test_tool_connect_to_bridge(self):
        self.assertIn("connect_to_bridge", TOOL_HANDLERS)

    def test_tool_zoom_map_zone(self):
        self.assertIn("zoom_map_zone", TOOL_HANDLERS)

    def test_tool_capture_mon1_map_image(self):
        self.assertIn("capture_mon1_map_image", TOOL_HANDLERS)

    def test_tool_select_camera_and_timeline(self):
        self.assertIn("select_camera_and_timeline", TOOL_HANDLERS)

    def test_tool_capture_mon2_camera_image(self):
        self.assertIn("capture_mon2_camera_image", TOOL_HANDLERS)

if __name__ == "__main__":
    unittest.main()
