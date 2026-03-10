"""
GKeepSync - Token Receiver Server
Localhost HTTP server nhận oauth_token từ Chrome Extension.
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Callable, Optional
from utils.logger import logger  # type: ignore

TOKEN_SERVER_PORT = 28371


class _TokenHandler(BaseHTTPRequestHandler):
    """Handles incoming token POST from Chrome Extension."""

    # Shared callback - set by TokenServer
    on_token_received: Optional[Callable[[str, str], Optional[str]]] = None

    def do_POST(self):
        if self.path == "/token":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                data = json.loads(body)
                oauth_token = data.get("oauth_token", "")
                email = data.get("email", "")

                if oauth_token:
                    logger.info("Received oauth_token from extension (%d chars)", len(oauth_token))
                    
                    # Notify the app, passing both email and token.
                    # App should return the retrieved master_token (if successful).
                    master_token = None
                    if _TokenHandler.on_token_received:
                        master_token = _TokenHandler.on_token_received(email, oauth_token)
                        
                    response_data = {"status": "ok", "message": "Token received!"}
                    if master_token:
                        response_data["master_token"] = master_token

                    # Send CORS-friendly response
                    self._send_json(200, response_data)
                else:
                    self._send_json(400, {"status": "error", "message": "Missing oauth_token"})
            except Exception as e:
                logger.error("Token handler error: %s", e)
                self._send_json(500, {"status": "error", "message": str(e)})
        else:
            self._send_json(404, {"status": "error", "message": "Not found"})

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, code: int, data: dict):
        self.send_response(code)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format: str, *args: Any) -> None:  # type: ignore[override]
        # Suppress default HTTP logs, use our logger instead
        pass


class TokenServer:
    """Localhost server that receives oauth_token from Chrome Extension."""

    def __init__(self, on_token_received: Optional[Callable[[str, str], Optional[str]]] = None):
        self._server = None
        self._thread = None
        _TokenHandler.on_token_received = on_token_received

    def start(self):
        """Start the token server in a background thread."""
        try:
            self._server = HTTPServer(("127.0.0.1", TOKEN_SERVER_PORT), _TokenHandler)
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()
            logger.info("Token server started on port %d", TOKEN_SERVER_PORT)
        except OSError as e:
            logger.warning("Token server failed to start: %s", e)

    def stop(self):
        """Stop the token server."""
        if self._server:
            self._server.shutdown()
            logger.info("Token server stopped.")
