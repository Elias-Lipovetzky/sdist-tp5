# proxy.py - reverse proxy minimo (stdlib, sin dependencias)
# Sirve el frontend y reenvia /api a la API: TODO queda bajo el MISMO origen (localhost:8080).
# Asi el navegador no ve cross-origin -> no hace falta CORS.
#
#   python3 proxy.py         # levanta en http://localhost:8080
#   (la API Flask debe estar corriendo en :5000)
import http.server, urllib.request, urllib.error, os

API = "http://localhost:5000"
FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=FRONTEND, **k)   # sirve index.html desde ../frontend

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self._proxy("GET")
        return super().do_GET()                          # archivos estaticos

    def do_POST(self):
        if self.path.startswith("/api/"):
            return self._proxy("POST")
        self.send_error(404)

    def _proxy(self, metodo):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n) if n else None
        req = urllib.request.Request(API + self.path, data=body, method=metodo)
        ct = self.headers.get("Content-Type")
        if ct:
            req.add_header("Content-Type", ct)
        try:
            with urllib.request.urlopen(req) as r:
                data = r.read()
                self.send_response(r.status)
                self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.URLError as e:
            self.send_error(502, f"no se pudo contactar la API en {API}: {e}")

if __name__ == "__main__":
    print("Proxy en http://localhost:8080  (frontend + /api -> :5000)")
    http.server.HTTPServer(("", 8080), Handler).serve_forever()
