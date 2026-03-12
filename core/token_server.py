from flask import Flask, request, jsonify
import threading
import logging

# Hide access log
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class TokenServer:
    def __init__(self, auth_callback=None):
        self.app = Flask(__name__)
        self.auth_callback = auth_callback
        self.server_thread = None
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/token", methods=["POST"])
        def receive_token():
            data = request.json
            if not data or "oauth_token" not in data:
                return jsonify({"status": "error", "message": "Missing oauth_token"}), 400

            oauth_token = data.get("oauth_token")
            email = data.get("email", None) # Optional for some V3 manifest flows

            # Pass token back to the main GUI thread
            if self.auth_callback:
                self.auth_callback(oauth_token, email)

            return jsonify({"status": "success", "message": "Token received"}), 200

    def run(self, port=12345):
        def _run_server():
            print(f"[TokenServer] Listening on http://localhost:{port}")
            self.app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
            
        self.server_thread = threading.Thread(target=_run_server, daemon=True)
        self.server_thread.start()

# For standalone testing
if __name__ == "__main__":
    def dummy_callback(token, email):
        print(f"Received Token: {token[:10]}... | Email: {email}")
        
    server = TokenServer(auth_callback=dummy_callback)
    server.run()
    # Hang process to test manually
    import time
    while True: time.sleep(1)
