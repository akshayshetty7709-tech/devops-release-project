import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")


def build_response(path):
    if path == "/health":
        return 200, {"status": "ok"}
    if path == "/":
        return 200, {"app": "devops-demo", "version": VERSION}
    return 404, {"error": "not found"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = build_response(self.path)
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7070"))
    print(f"devops-demo {VERSION} listening on {port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
