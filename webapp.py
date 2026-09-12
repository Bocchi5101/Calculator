"""WSGI entry point for production hosting: gunicorn webapp:application."""

import json

from calculator import calculate
from server import ASSETS, ROOT


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    status = "200 OK"
    content_type = "application/json"

    if method in {"GET", "HEAD"} and path == "/health":
        body = b'{"status":"ok"}'
    elif method in {"GET", "HEAD"} and path in ASSETS:
        filename, content_type = ASSETS[path]
        try:
            body = (ROOT / filename).read_bytes()
        except FileNotFoundError:
            status, content_type, body = "404 Not Found", "text/plain", b"Not found"
    elif method == "POST" and path == "/api/calculate":
        try:
            length = int(environ.get("CONTENT_LENGTH") or "0")
            if not 0 < length <= 4096:
                raise ValueError("Invalid request size.")
            data = json.loads(environ["wsgi.input"].read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a calculation.")
            result = calculate(float(data["first"]), data["operator"], float(data["second"]))
            payload = {"result": result}
        except (ValueError, TypeError, KeyError, OverflowError) as error:
            status = "400 Bad Request"
            message = str(error) if isinstance(error, ValueError) else "Please enter valid numbers and an operation."
            payload = {"error": message}
        body = json.dumps(payload, allow_nan=False).encode()
    else:
        status, content_type, body = "404 Not Found", "text/plain", b"Not found"

    start_response(status, [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
        ("X-Content-Type-Options", "nosniff"),
    ])
    return [b"" if method == "HEAD" else body]
