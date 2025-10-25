import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# Blueprints
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.quiz import quiz_bp
from routes.misc import misc_bp

from database import init_db

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
CORS(app)

# register blueprints (semua konsisten pakai /api/...)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
app.register_blueprint(misc_bp, url_prefix="/api/misc")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)


