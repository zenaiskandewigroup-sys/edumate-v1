# routes/chat.py
from flask import Blueprint, request, jsonify
from models import save_chat, get_chats_for_user
from utils.ai_helper import generate_chat_reply

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("", methods=["POST"])
def chat():
    data = request.get_json() or {}
    question = (data.get("message") or data.get("question") or "").strip()
    username = data.get("username") or "anonymous"

    if not question:
        return jsonify({"error": "Pertanyaan kosong"}), 400

    save_chat(username, "user", question)

    try:
        answer = generate_chat_reply(question, username=username)
    except Exception as e:
        answer = f"[Error] Gagal mendapat jawaban: {e}"

    save_chat(username, "bot", answer)

    history = get_chats_for_user(username)
    return jsonify({"reply": answer, "history": history}), 200

@chat_bp.route("/history/<username>", methods=["GET"])
def history(username):
    history = get_chats_for_user(username)
    return jsonify({"history": history})


