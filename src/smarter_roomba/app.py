import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .config import ServerConfig


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/health":
            self.send_error(404)
            return

        body = json.dumps({"status": "ok"}, separators=(",", ":")).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        logging.info(format, *args)


def create_server(config: ServerConfig) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((config.host, config.port), RequestHandler)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        config = ServerConfig.from_env()
    except ValueError as error:
        logging.error("configuration error: %s", error)
        return 2

    with create_server(config) as server:
        host, port = server.server_address[:2]
        logging.info("health=ok listening=http://%s:%s", host, port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("server stopped")
    return 0
