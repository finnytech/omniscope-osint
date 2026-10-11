"""
OmniScope OSINT: Feedback & Diagnostic Telemetry Logger
Records detailed node scan metrics, spatial query boundaries, coordinate anomalies,
and client-side UI feedback into logs/feedback_logs.json.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime, timezone
from collections import deque
from typing import Dict, Any, List, Optional

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
FEEDBACK_LOG_FILE = os.path.join(LOGS_DIR, "feedback_logs.json")

class FeedbackLogger:
    def __init__(self, max_memory_entries: int = 2000, max_file_entries: int = 5000):
        self.log_file = FEEDBACK_LOG_FILE
        self.max_memory_entries = max_memory_entries
        self.max_file_entries = max_file_entries
        self._lock = threading.Lock()
        self._entries: deque = deque(maxlen=max_memory_entries)
        
        # Ensure directory exists on D:\
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Load existing log entries if available
        self._load_existing()

    def _load_existing(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data[-self.max_memory_entries:]:
                            self._entries.append(item)
            except Exception as e:
                sys.stderr.write(f"[FeedbackLogger] Notice: starting fresh log ({e})\n")

    def _persist(self):
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(list(self._entries), f, indent=2, ensure_ascii=False)
        except Exception as e:
            sys.stderr.write(f"[FeedbackLogger] Error saving log file: {e}\n")

    def log_scan(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        zoom: int,
        provider: str,
        node_type: str,
        total_returned: int,
        duration_ms: float,
        breakdown: Optional[Dict[str, int]] = None,
        anomalies: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Logs a spatial bounding box scan with performance and anomaly metrics."""
        entry = {
            "id": f"scan_{int(time.time() * 1000)}_{len(self._entries)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "NODE_SCAN",
            "bbox": {
                "min_lat": round(min_lat, 5),
                "max_lat": round(max_lat, 5),
                "min_lon": round(min_lon, 5),
                "max_lon": round(max_lon, 5),
                "zoom": zoom
            },
            "filters": {
                "provider": provider,
                "node_type": node_type
            },
            "metrics": {
                "total_returned": total_returned,
                "duration_ms": round(duration_ms, 2),
                "breakdown": breakdown or {}
            },
            "anomalies_detected": anomalies or []
        }

        with self._lock:
            self._entries.append(entry)
            self._persist()

        return entry

    def log_anomaly(
        self,
        node_id: str,
        title: str,
        lat: float,
        lon: float,
        reason: str,
        action_taken: str,
        provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """Logs an intercepted coordinate anomaly (e.g. Null Island 0,0, ocean mismatch, or out-of-bounds)."""
        entry = {
            "id": f"anom_{int(time.time() * 1000)}_{len(self._entries)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "COORDINATE_ANOMALY",
            "node": {
                "id": node_id,
                "title": title,
                "provider": provider or "Unknown",
                "lat": lat,
                "lon": lon
            },
            "reason": reason,
            "action_taken": action_taken
        }

        with self._lock:
            self._entries.append(entry)
            self._persist()

        return entry

    def log_client_event(self, event_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Logs interactive events from the UI (e.g. layout reset, camera clicks, alarms)."""
        entry = {
            "id": f"client_{int(time.time() * 1000)}_{len(self._entries)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": f"CLIENT_{event_name.upper()}",
            "payload": payload
        }

        with self._lock:
            self._entries.append(entry)
            self._persist()

        return entry

    def get_logs(self, limit: int = 100, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            entries = list(self._entries)
            if event_type and event_type != "all":
                entries = [e for e in entries if e.get("event_type", "").lower() == event_type.lower()]
            return entries[-limit:]

    def clear_logs(self):
        with self._lock:
            self._entries.clear()
            self._persist()

# Global Singleton
feedback_logger = FeedbackLogger()
