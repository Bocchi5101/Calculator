"""Serve the space calculator locally using only Python's standard library."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from calculator import calculate

ROOT = Path(__file__).resolve().parent / "static"
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/music.mp3": ("music.mp3", "audio/mpeg"),
}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        asset = ASSETS.get(self.path)
        if asset is None:
            self.send_error(404)
            return
        filename, content_type = asset
        self.respond(200, (ROOT / filename).read_bytes(), content_type)

    def do_POST(self):
        if self.path != "/api/calculate":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("Invalid request size.")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a calculation.")
            result = calculate(float(data["first"]), data["operator"], float(data["second"]))
            payload, status = {"result": result}, 200
        except (ValueError, TypeError, KeyError, OverflowError) as error:
            message = str(error) if isinstance(error, ValueError) else "Please enter valid numbers and an operation."
            payload, status = {"error": message}, 400
        self.respond(status, json.dumps(payload, allow_nan=False).encode(), "application/json")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Space calculator: http://127.0.0.1:8000 (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
