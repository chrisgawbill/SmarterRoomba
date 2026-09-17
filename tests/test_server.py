import json
import threading
import unittest
import urllib.error
import urllib.request

from smarter_roomba.app import create_server
from smarter_roomba.config import ServerConfig


class ConfigTests(unittest.TestCase):
    def test_defaults_and_env_overrides(self) -> None:
        self.assertEqual(ServerConfig.from_env({}), ServerConfig())
        self.assertEqual(
            ServerConfig.from_env(
                {"SMARTER_ROOMBA_HOST": "0.0.0.0", "SMARTER_ROOMBA_PORT": "9000"}
            ),
            ServerConfig("0.0.0.0", 9000),
        )

    def test_invalid_ports_are_rejected(self) -> None:
        for value in ("abc", "0", "65536"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ServerConfig.from_env({"SMARTER_ROOMBA_PORT": value})


class HealthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server(ServerConfig(port=0))
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.server.server_port}{path}"

    def test_health(self) -> None:
        with urllib.request.urlopen(self.url("/health")) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers["Content-Type"], "application/json")
            self.assertEqual(json.load(response), {"status": "ok"})

    def test_unknown_path_is_not_found(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(self.url("/unknown"))
        self.assertEqual(error.exception.code, 404)
        error.exception.close()
