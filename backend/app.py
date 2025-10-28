import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# Blueprints (optional import safe)
try:
    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.quiz import quiz_bp
    from routes.misc import misc_bp
    from database import init_db
except Exception as e:
    print(f"[WARN] Skipping module import: {e}")
    auth_bp = chat_bp = quiz_bp = misc_bp = None
    init_db = lambda: None

# --- Flask setup ---
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app = Flask(__name__, static_folder=frontend_dir, template_folder=frontend_dir)
CORS(app)

# --- Register Blueprints (only if available) ---
if auth_bp: app.register_blueprint(auth_bp, url_prefix="/api/auth")
if chat_bp: app.register_blueprint(chat_bp, url_prefix="/api/chat")
if quiz_bp: app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
if misc_bp: app.register_blueprint(misc_bp, url_prefix="/api/misc")

# --- Routes ---
@app.route("/")
def index():
    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, "index.html")
    return jsonify({"status": "ok", "message": "Edumate backend running (no frontend)"})

@app.route("/<path:path>")
def serve_page(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return jsonify({"error": "File not found"}), 404

# --- Main entry ---
def vercel_handler(request=None):
    """Vercel-compatible entrypoint"""
    return app

if __name__ == "__main__":
    print("[INIT] Starting local Flask server...")
    init_db()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
