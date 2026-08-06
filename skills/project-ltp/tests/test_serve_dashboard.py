from __future__ import annotations

import errno
import http.client
import importlib.util
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import call, patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "serve_dashboard.py"
SPEC = importlib.util.spec_from_file_location("serve_dashboard", SCRIPT)
assert SPEC and SPEC.loader
serve_dashboard = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = serve_dashboard
SPEC.loader.exec_module(serve_dashboard)


class DashboardServerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.project = root / "project"
        (self.project / "ltp").mkdir(parents=True)
        (self.project / "ltp" / "ltp-model.yaml").write_text(
            "project:\n  name: Test\nentities: []\nlinks: []\nviews: {}\n",
            encoding="utf-8",
        )
        self.static = root / "dist"
        (self.static / "assets").mkdir(parents=True)
        (self.static / "index.html").write_text("<h1>Dashboard</h1>", encoding="utf-8")
        (self.static / "assets" / "app.js").write_text("console.log('ok')", encoding="utf-8")
        self.server = serve_dashboard.create_server(
            self.project,
            port=0,
            static=self.static,
            quiet=True,
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.host, self.port = self.server.server_address[:2]

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method: str, path: str):
        connection = http.client.HTTPConnection(self.host, self.port, timeout=2)
        connection.request(method, path)
        response = connection.getresponse()
        body = response.read()
        headers = dict(response.getheaders())
        connection.close()
        return response.status, headers, body

    def test_serves_only_dashboard_and_known_model(self) -> None:
        status, headers, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Dashboard", body)
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])

        status, _, body = self.request("GET", "/api/model")
        self.assertEqual(status, 200)
        self.assertIn(b"name: Test", body)

        status, _, _ = self.request("GET", "/api/throughput")
        self.assertEqual(status, 204)

        status, _, _ = self.request("GET", "/api/github-sync")
        self.assertEqual(status, 204)

    def test_serves_the_github_sync_ledger_when_present(self) -> None:
        (self.project / "ltp" / "github-sync.yaml").write_text(
            "repo: o/r\nactions:\n  ACT-1:\n    issue: 4\n", encoding="utf-8"
        )
        status, _, body = self.request("GET", "/api/github-sync")
        self.assertEqual(status, 200)
        self.assertIn(b"issue: 4", body)
        _, _, meta = self.request("GET", "/api/meta")
        self.assertIn(b'"tracking"', meta)

    def test_rejects_traversal_and_unknown_paths(self) -> None:
        for path in ("/assets/%2e%2e/index.html", "/assets/../index.html", "/project/ltp/ltp-model.yaml"):
            status, _, _ = self.request("GET", path)
            self.assertEqual(status, 404, path)

    def test_is_read_only(self) -> None:
        status, _, body = self.request("POST", "/api/model")
        self.assertEqual(status, 405)
        self.assertIn(b"read only", body)

    def test_meta_changes_when_throughput_appears(self) -> None:
        status, _, body = self.request("GET", "/api/meta")
        self.assertEqual(status, 200)
        self.assertIn(b'"exists":false', body)
        (self.project / "ltp" / "throughput.yaml").write_text(
            "definition:\n  name: X\n  unit: x\n  period: week\nperiods: []\n",
            encoding="utf-8",
        )
        status, _, body = self.request("GET", "/api/meta")
        self.assertEqual(status, 200)
        self.assertIn(b'"exists":true', body)


class DashboardBoundaryTest(unittest.TestCase):
    def test_non_loopback_requires_explicit_override(self) -> None:
        with self.assertRaises(ValueError):
            serve_dashboard.validate_bind_host("0.0.0.0", allow_network=False)
        serve_dashboard.validate_bind_host("0.0.0.0", allow_network=True)

    def test_missing_model_fails_before_server_start(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            static = root / "dist"
            static.mkdir()
            (static / "index.html").write_text("ok", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                serve_dashboard.resolve_paths(root, static)

    def test_automatic_port_selection_tries_the_next_port(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "project"
            (project / "ltp").mkdir(parents=True)
            (project / "ltp" / "ltp-model.yaml").write_text(
                "project:\n  name: Test\nentities: []\nlinks: []\nviews: {}\n",
                encoding="utf-8",
            )
            static = root / "dist"
            static.mkdir()
            (static / "index.html").write_text("ok", encoding="utf-8")
            fake_server = unittest.mock.Mock()
            with patch.object(
                serve_dashboard,
                "ThreadingHTTPServer",
                side_effect=[
                    OSError(errno.EADDRINUSE, "Address already in use"),
                    fake_server,
                ],
            ) as server_class:
                result = serve_dashboard.create_server(
                    project,
                    port=8765,
                    auto_port=True,
                    static=static,
                )
            self.assertIs(result, fake_server)
            self.assertTrue(fake_server.daemon_threads)
            self.assertEqual(
                server_class.call_args_list,
                [
                    call(("127.0.0.1", 8765), unittest.mock.ANY),
                    call(("127.0.0.1", 8766), unittest.mock.ANY),
                ],
            )

    def test_explicit_port_does_not_fall_back(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "project"
            (project / "ltp").mkdir(parents=True)
            (project / "ltp" / "ltp-model.yaml").write_text(
                "project:\n  name: Test\nentities: []\nlinks: []\nviews: {}\n",
                encoding="utf-8",
            )
            static = root / "dist"
            static.mkdir()
            (static / "index.html").write_text("ok", encoding="utf-8")
            with patch.object(
                serve_dashboard,
                "ThreadingHTTPServer",
                side_effect=OSError(errno.EADDRINUSE, "Address already in use"),
            ) as server_class:
                with self.assertRaises(OSError):
                    serve_dashboard.create_server(
                        project,
                        port=9000,
                        auto_port=False,
                        static=static,
                    )
            server_class.assert_called_once_with(
                ("127.0.0.1", 9000),
                unittest.mock.ANY,
            )


if __name__ == "__main__":
    unittest.main()
