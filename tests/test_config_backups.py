import hashlib
import json
import sys
import tempfile
import threading
import time
import types
import unittest
from pathlib import Path
from unittest import mock


if "paho" not in sys.modules:
    paho_module = types.ModuleType("paho")
    mqtt_package = types.ModuleType("paho.mqtt")
    client_module = types.ModuleType("paho.mqtt.client")
    client_module.Client = type("Client", (), {})
    client_module.MQTTMessage = type("MQTTMessage", (), {})
    client_module.CallbackAPIVersion = type("CallbackAPIVersion", (), {"VERSION2": object()})
    client_module.MQTT_ERR_SUCCESS = 0
    mqtt_package.client = client_module
    paho_module.mqtt = mqtt_package
    sys.modules["paho"] = paho_module
    sys.modules["paho.mqtt"] = mqtt_package
    sys.modules["paho.mqtt.client"] = client_module

from app.history_store import HistoryStore
from app.main import Camera, Hub


class ConfigSnapshotStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self._tmpdir.name) / "history.sqlite3")
        self.store = HistoryStore(
            self.db_path,
            max_config_snapshots_per_camera=2,
            config_snapshot_max_age_days=0,
        )

    def tearDown(self) -> None:
        self.store.close()
        self._tmpdir.cleanup()

    def test_dedup_skips_identical_consecutive_hash(self) -> None:
        first = self.store.record_config_snapshot(
            recorded_at=100,
            camera_id="cam1",
            source="manual",
            config={"image": {"hflip": True}},
            capabilities={"image": {}},
            content_hash="abc",
        )
        second = self.store.record_config_snapshot(
            recorded_at=101,
            camera_id="cam1",
            source="hub_write",
            config={"image": {"hflip": True}},
            capabilities={"image": {}},
            content_hash="abc",
        )
        self.assertTrue(first["stored"])
        self.assertFalse(second["stored"])
        self.assertTrue(second["skipped_duplicate"])
        self.assertEqual(len(self.store.list_config_snapshots("cam1")), 1)

    def test_retention_prunes_by_count(self) -> None:
        for index in range(4):
            self.store.record_config_snapshot(
                recorded_at=100 + index,
                camera_id="cam1",
                source="manual",
                config={"n": index},
                content_hash=f"hash-{index}",
            )
        rows = self.store.list_config_snapshots("cam1")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["content_hash"], "hash-3")
        self.assertEqual(rows[1]["content_hash"], "hash-2")


class ConfigBackupHubTests(unittest.TestCase):
    def _hub_with_store(self, *, max_snapshots: int = 20) -> Hub:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        hub = object.__new__(Hub)
        hub.state_lock = threading.Lock()
        hub.cameras = {
            "aabbccddeeff": Camera(
                camera_id="aabbccddeeff",
                name="birdbox",
                ip="192.168.1.10",
                api_base_url="https://192.168.1.10:1998/api/v1",
                api_token="tok",
                api_status="online",
                api_streamer="raptor",
            )
        }
        hub.history_store = HistoryStore(
            str(Path(tmp.name) / "h.sqlite3"),
            max_config_snapshots_per_camera=max_snapshots,
            config_snapshot_max_age_days=0,
        )
        self.addCleanup(hub.history_store.close)
        hub.history_enabled = True
        hub.history_db_path = str(Path(tmp.name) / "h.sqlite3")
        hub.history_max_config_snapshots_per_camera = max_snapshots
        hub.history_config_snapshot_max_age_days = 0
        hub.optimistic_supported_controls_by_camera = {}
        hub._resolve_camera_id = lambda camera_id: str(camera_id or "").strip().lower()  # type: ignore[method-assign]
        hub._camera_api_base_url = lambda camera: str(camera.api_base_url or "")  # type: ignore[method-assign]
        hub._record_history_action = lambda *args, **kwargs: None  # type: ignore[method-assign]
        hub._record_native_action = lambda *args, **kwargs: None  # type: ignore[method-assign]
        hub._record_history_config_changes = lambda *args, **kwargs: None  # type: ignore[method-assign]
        hub._record_optimistic_supported_controls = lambda *args, **kwargs: None  # type: ignore[method-assign]
        hub._schedule_api_refresh = lambda camera_id: None  # type: ignore[method-assign]
        hub._schedule_supported_controls_refresh = lambda camera_id: None  # type: ignore[method-assign]
        hub.refresh_camera_api_details = lambda camera_id: True  # type: ignore[method-assign]
        hub._format_timestamp = Hub._format_timestamp.__get__(hub, Hub)
        hub._coerce_int = Hub._coerce_int.__get__(hub, Hub)
        hub._config_snapshot_summary_for_ui = Hub._config_snapshot_summary_for_ui.__get__(hub, Hub)
        hub._config_snapshot_detail_for_ui = Hub._config_snapshot_detail_for_ui.__get__(hub, Hub)
        hub._build_config_restore_plan = Hub._build_config_restore_plan.__get__(hub, Hub)
        hub._strip_restore_secrets = Hub._strip_restore_secrets.__get__(hub, Hub)
        hub._restorable_config_groups = Hub._restorable_config_groups.__get__(hub, Hub)
        hub._restore_capability_group_for_key = Hub._restore_capability_group_for_key.__get__(hub, Hub)
        hub._restore_value_conflict = Hub._restore_value_conflict.__get__(hub, Hub)
        hub._restore_value_summary = Hub._restore_value_summary.__get__(hub, Hub)
        hub._split_native_config_patch_for_settings = Hub._split_native_config_patch_for_settings.__get__(hub, Hub)
        hub._stream_setting_path = Hub._stream_setting_path.__get__(hub, Hub)
        hub.backup_camera_config = Hub.backup_camera_config.__get__(hub, Hub)
        hub._maybe_backup_camera_config = Hub._maybe_backup_camera_config.__get__(hub, Hub)
        hub.preview_camera_config_restore = Hub.preview_camera_config_restore.__get__(hub, Hub)
        hub.restore_camera_config_backup = Hub.restore_camera_config_backup.__get__(hub, Hub)
        hub.patch_camera_config = Hub.patch_camera_config.__get__(hub, Hub)
        hub.list_camera_config_backups = Hub.list_camera_config_backups.__get__(hub, Hub)
        hub.get_camera_config_backup = Hub.get_camera_config_backup.__get__(hub, Hub)
        return hub

    def test_backup_after_successful_patch(self) -> None:
        hub = self._hub_with_store()
        patched: list[tuple[str, dict]] = []

        class FakeClient:
            def patch_setting(self, path: str, body: dict) -> dict:
                patched.append((path, body))
                return {"applied": [path]}

            def patch_config(self, payload: dict) -> dict:
                return {"status": "accepted", "applied": list(payload.keys())}

            def get_config(self, timeout: int | None = None) -> dict:
                return {"image": {"hflip": True}, "stream0": {"width": 1920}, "agent": {"token": "secret"}}

            def _control_timeout(self) -> int:
                return 15

            def get_capabilities(self) -> dict:
                return {"image": {}, "streams": {}}

            def get_device(self) -> dict:
                return {"software": {"firmware_version": "fw-1", "streamer": "raptor"}}

        hub._camera_api_client = lambda camera: FakeClient()  # type: ignore[method-assign]

        # Avoid racing the background backup thread in this unit test.
        hub._schedule_camera_config_backup = lambda *args, **kwargs: None  # type: ignore[method-assign]
        Hub.patch_camera_config(hub, "aabbccddeeff", {"image": {"hflip": True}}, refresh_after=False)
        # Simulate the scheduled backup path directly.
        hub.backup_camera_config("aabbccddeeff", source="hub_write", label="After settings save")
        backups = hub.list_camera_config_backups("aabbccddeeff")
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0]["source"], "hub_write")

    def test_failed_patch_does_not_backup(self) -> None:
        hub = self._hub_with_store()
        hub._schedule_camera_config_backup = lambda *args, **kwargs: (_ for _ in ()).throw(  # type: ignore[method-assign]
            AssertionError("backup must not be scheduled after failed patch")
        )

        class FakeClient:
            def patch_setting(self, path: str, body: dict) -> dict:
                raise RuntimeError("write failed")

            def patch_config(self, payload: dict) -> dict:
                raise RuntimeError("write failed")

            def get_config(self) -> dict:
                raise AssertionError("should not backup")

        hub._camera_api_client = lambda camera: FakeClient()  # type: ignore[method-assign]
        with self.assertRaises(RuntimeError):
            Hub.patch_camera_config(hub, "aabbccddeeff", {"image": {"hflip": True}}, refresh_after=False)
        self.assertEqual(hub.list_camera_config_backups("aabbccddeeff"), [])

    def test_restore_preview_classifies_secrets_dropped_and_conflicts(self) -> None:
        hub = self._hub_with_store()
        snapshot_id = hub.history_store.record_config_snapshot(
            recorded_at=int(time.time()),
            camera_id="aabbccddeeff",
            source="manual",
            firmware_id="fw-old",
            streamer="raptor",
            config={
                "agent": {"token": "secret", "listen": "0.0.0.0"},
                "mqtt_sub": {"host": "broker", "password": "pw"},
                "image": {"hflip": True},
                "legacy_thing": {"x": 1},
                "stream0": {"format": "h265"},
            },
            capabilities={"image": {}, "streams": {}},
            content_hash="snap-1",
        )["snapshot_id"]

        class FakeClient:
            def get_capabilities(self) -> dict:
                return {
                    "image": {},
                    "streams": {"fields": {"format": {"enum": ["h264", "h265"]}}},
                }

            def get_config(self) -> dict:
                return {"image": {"hflip": False}, "stream0": {"format": "h264"}}

        hub._camera_api_client = lambda camera: FakeClient()  # type: ignore[method-assign]
        preview = hub.preview_camera_config_restore("aabbccddeeff", snapshot_id)
        secret_paths = {item["path"] for item in preview["skipped_secrets"]}
        self.assertIn("agent", secret_paths)
        self.assertIn("mqtt_sub.password", secret_paths)
        compatible_paths = {item["path"] for item in preview["compatible"]}
        self.assertIn("image", compatible_paths)
        dropped_paths = {item["path"] for item in preview["dropped"]}
        self.assertIn("legacy_thing", dropped_paths)
        self.assertIn("image", preview["compatible_payload"])
        self.assertNotIn("agent", preview["compatible_payload"])

    def test_restore_apply_uses_settings_peel_for_stream_osd(self) -> None:
        hub = self._hub_with_store()
        snapshot_id = hub.history_store.record_config_snapshot(
            recorded_at=int(time.time()),
            camera_id="aabbccddeeff",
            source="manual",
            config={
                "stream0": {
                    "width": 1280,
                    "osd": {"enabled": True, "usertext": {"enabled": True, "format": "%hostname"}},
                }
            },
            capabilities={"streams": {}},
            content_hash="snap-osd",
        )["snapshot_id"]

        setting_calls: list[tuple[str, dict]] = []

        class FakeClient:
            def get_capabilities(self) -> dict:
                return {"streams": {}}

            def get_config(self) -> dict:
                return {"stream0": {"width": 640}}

            def patch_setting(self, path: str, body: dict) -> dict:
                setting_calls.append((path, body))
                return {"applied": [path]}

            def patch_config(self, payload: dict) -> dict:
                raise AssertionError(f"omnibus should not be required for peeled fields: {payload}")

            def get_device(self) -> dict:
                return {"software": {"firmware_version": "fw", "streamer": "raptor"}}

        hub._camera_api_client = lambda camera: FakeClient()  # type: ignore[method-assign]
        hub.refresh_camera_api_details = lambda camera_id: True  # type: ignore[method-assign]
        hub._schedule_api_refresh = lambda camera_id: None  # type: ignore[method-assign]
        hub._schedule_supported_controls_refresh = lambda camera_id: None  # type: ignore[method-assign]
        hub._record_optimistic_supported_controls = lambda *args, **kwargs: None  # type: ignore[method-assign]

        result = hub.restore_camera_config_backup("aabbccddeeff", snapshot_id, mode="compatible")
        self.assertEqual(result["status"], "success")
        paths = [path for path, _body in setting_calls]
        self.assertTrue(any(path.endswith("width") or "width" in path for path in paths), paths)
        self.assertTrue(any("osd" in path for path in paths), paths)


if __name__ == "__main__":
    unittest.main()
