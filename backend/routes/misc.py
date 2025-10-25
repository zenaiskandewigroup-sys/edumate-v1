# routes/misc.py
from flask import Blueprint, jsonify

misc_bp = Blueprint("misc", __name__)

@misc_bp.route("/about", methods=["GET"])
def about():
    return jsonify({
        "name": "EduMate",
        "description": "EduMate - AI Tutor & Quiz platform built for VirtuHack",
        "features": ["chat", "quiz", "leaderboard", "user accounts"]
    })


