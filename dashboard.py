#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"

sys.path.insert(0, str(BASE_DIR))
import api.index as vercel_api

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        vercel_api._cors_headers(self)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            return vercel_api.handler.do_GET(self)
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            return vercel_api.handler.do_POST(self)
        self.send_response(404)
        self.end_headers()

def run(port=3000):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"⚡ Sovereign Agent Dashboard & Co-Pilot running at http://127.0.0.1:{port}/")
    print(f"📊 Telemetry API served at http://127.0.0.1:{port}/api/telemetry")
    print(f"🤖 Conversational Co-Pilot at http://127.0.0.1:{port}/api/copilot")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Sovereign Agent Server.")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign Agent Dashboard")
    parser.add_argument("--port", type=int, default=3000, help="Port to listen on (default: 3000)")
    args = parser.parse_args()
    run(port=args.port)
