# routes/auth.py
from flask import Blueprint, request, jsonify
from models import create_user, get_user_by_username
from utils.security import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return jsonify({"success": False, "msg": "Username dan password wajib"}), 400

    # check existing
    existing = get_user_by_username(username)
    if existing:
        return jsonify({"success": False, "msg": "Username sudah dipakai"}), 400

    hashed = hash_password(password)
    ok = create_user(username, hashed)
    if ok:
        return jsonify({"success": True, "msg": "Register berhasil"}), 201
    return jsonify({"success": False, "msg": "Gagal register"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    user = get_user_by_username(username)

    if not user:
        return jsonify({"success": False, "msg": "User tidak ditemukan"}), 404

    if verify_password(password, user["password"]):
        return jsonify({
            "success": True,
            "msg": "Login berhasil",
            "username": username
        }), 200
    else:
        return jsonify({"success": False, "msg": "Password salah"}), 401


