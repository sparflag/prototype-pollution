#!/usr/bin/env python3
"""Prototype Pollution — real mini-challenge (prototype-pollution)."""
import base64, hashlib, hmac, json, os, re, sqlite3, sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote, quote

sys.path.insert(0, "/challenge/_shared")
from fetch_material import fetch_material

CHALLENGE_KEY = os.environ.get("CHALLENGE_KEY", 'proto-proto')
_MAT = {}
CONFIG = {"theme": "light", "isAdmin": False}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain", headers=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        data = body if isinstance(body, bytes) else body.encode()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


    def do_GET(self):
        if self.path == "/flag":
            return self._send(200, _MAT.get("delivery_blob", "") + "\n")
        if self.path == "/":
            return self._send(200, "POST JSON to /merge  GET /admin\n")
        if self.path == "/admin":
            if CONFIG.get("isAdmin"):
                return self._send(200, f"admin ok; key={CHALLENGE_KEY}\n")
            return self._send(403, "not admin\n")
        self._send(404, "no\n")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode() or "{}")
        # Vulnerable recursive merge — __proto__ / constructor pollution
        def merge(dst, src):
            for k, v in src.items():
                if k in ("__proto__", "constructor", "prototype"):
                    # pollute CONFIG via shared dict abuse
                    if isinstance(v, dict):
                        merge(CONFIG, v)
                    continue
                if isinstance(v, dict) and isinstance(dst.get(k), dict):
                    merge(dst[k], v)
                else:
                    dst[k] = v
        merge(CONFIG, body)
        return self._send(200, json.dumps(CONFIG) + "\n")


def main():
    _MAT.update(fetch_material())
    print('Prototype Pollution on :8080')
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

if __name__ == "__main__":
    main()
