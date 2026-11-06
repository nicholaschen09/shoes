"""Small local server for the Shoes showcase.

Edit SHOES below to add your own pairs. No uploads or database are needed.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"

SHOES = [
    {
        "id": "weekend-walks-01",
        "brand": "Nike",
        "model": "Air Max 1",
        "colorway": "Red / White / Neutral Grey",
        "category": "Weekend",
        "price": 150,
        "currency": "USD",
        "purchaseYear": 2024,
        "wornSince": 2024,
        "rating": 4.5,
        "comments": "A little bit of color makes every Saturday better.",
        "details": ["Visible Air", "Retro runner"],
        "imageUrl": "/images/nike.png",
    },
    {
        "id": "trail-days-01",
        "brand": "Salomon",
        "model": "XT-6",
        "colorway": "Vanilla Ice / Olive",
        "category": "Trail",
        "price": 200,
        "currency": "USD",
        "purchaseYear": 2022,
        "wornSince": 2022,
        "rating": 4.9,
        "comments": "The one that makes a steep trail feel like a good idea.",
        "details": ["Quicklace", "Trail grip"],
        "imageUrl": "/images/salomon-xt-6.png",
    },
    {
        "id": "road-days-01",
        "brand": "Hoka",
        "model": "Mach X",
        "colorway": "White / Blue",
        "category": "Running",
        "price": 180,
        "currency": "USD",
        "purchaseYear": 2024,
        "wornSince": 2024,
        "rating": 4.7,
        "comments": "Light, springy, and ready for a long road day.",
        "details": ["Road running", "Cushioned ride"],
        "imageUrl": "/images/hoka.png",
    },
    {
        "id": "classic-days-01",
        "brand": "Converse",
        "model": "Chuck Taylor All Star",
        "colorway": "Black / White",
        "category": "Classic",
        "price": 65,
        "currency": "USD",
        "purchaseYear": 2021,
        "wornSince": 2021,
        "rating": 4.6,
        "comments": "A classic that works with almost everything.",
        "details": ["Canvas upper", "High top"],
        "imageUrl": "/images/converse.png",
    },
    {
        "id": "everyday-days-01",
        "brand": "New Balance",
        "model": "530",
        "colorway": "White / Silver",
        "category": "Daily",
        "price": 100,
        "currency": "USD",
        "purchaseYear": 2023,
        "wornSince": 2023,
        "rating": 4.7,
        "comments": "A comfortable everyday pair with a little retro character.",
        "details": ["Mesh upper", "Retro runner"],
        "imageUrl": "/images/new-balance.png",
    },
    {
        "id": "casual-days-01",
        "brand": "Vans",
        "model": "Old Skool",
        "colorway": "Black / White",
        "category": "Casual",
        "price": 70,
        "currency": "USD",
        "purchaseYear": 2022,
        "wornSince": 2022,
        "rating": 4.7,
        "comments": "A dependable everyday classic with an easy profile.",
        "details": ["Canvas upper", "Waffle outsole"],
        "imageUrl": "/images/vans.png?v=2",
    },
]


class ShowcaseHandler(BaseHTTPRequestHandler):
    """Serve the compiled frontend and the in-code shoe collection."""

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        request_path = urlsplit(self.path).path
        if request_path == "/api/shoes":
            self._send_json(SHOES)
            return

        assets = {
            "/": (PUBLIC / "index.html", "text/html; charset=utf-8"),
            "/styles.css": (ROOT / "src" / "styles.css", "text/css; charset=utf-8"),
            "/frontend.js": (DIST / "frontend.js", "text/javascript; charset=utf-8"),
            "/images/salomon-xt-6.png": (PUBLIC / "images" / "salomon-xt-6.png", "image/png"),
            "/images/hoka.png": (PUBLIC / "images" / "hoka.png", "image/png"),
            "/images/nike.png": (PUBLIC / "images" / "nike.png", "image/png"),
            "/images/converse.png": (PUBLIC / "images" / "converse.png", "image/png"),
            "/images/new-balance.png": (PUBLIC / "images" / "new-balance.png", "image/png"),
            "/images/vans.png": (PUBLIC / "images" / "vans.png", "image/png"),
        }
        asset = assets.get(request_path)
        if asset is None or not asset[0].is_file():
            self.send_error(404, "Not found")
            return
        self._send_file(*asset)

    def _send_json(self, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[server] {format % args}")


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print(f"Shoes running at http://{address[0]}:{address[1]}")
    ThreadingHTTPServer(address, ShowcaseHandler).serve_forever()
