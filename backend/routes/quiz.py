# routes/quiz.py
from flask import Blueprint, request, jsonify
from utils.ai_helper import generate_quiz_questions, parse_possible_json
from models import create_quiz_record, save_quiz_questions, get_quiz_questions, save_score, get_leaderboard
import random

quiz_bp = Blueprint("quiz", __name__)

BANNED = ["teror", "terror", "rasis", "racis", "rape", "seks", "porn", "sex abuse"]

def contains_banned(text: str) -> bool:
    t = (text or "").lower()
    return any(b in t for b in BANNED)

def make_dummy_questions(category: str, total: int):
    qlist = []
    for i in range(total):
        qtxt = f"[Fallback] Contoh soal {i+1} untuk topik '{category}'. Pilih jawaban yang paling tepat."
        options = ["Pilihan A", "Pilihan B", "Pilihan C", "Pilihan D"]
        correct = random.choice(options)
        qlist.append({"index": i, "q": qtxt, "options": options, "answer": correct})
    return qlist

def norm(s: str) -> str:
    return (s or "").strip().lower()

@quiz_bp.route("", methods=["POST"])
def generate_quiz():
    data = request.get_json() or {}
    category = (data.get("category") or "").strip()
    try:
        total = int(data.get("total", 15))
    except Exception:
        total = 15
    username = data.get("username") or "anonymous"

    if not category:
        return jsonify({"error": "Category required"}), 400

    if contains_banned(category):
        return jsonify({"error": "Category contains disallowed content."}), 400

    raw = generate_quiz_questions(category, total=total)
    print("DEBUG RAW QUIZ OUTPUT:", raw[:500])  # 🔎 log isi awal dari Gemini

    try:
        parsed = parse_possible_json(raw)
        questions = []
        for idx, item in enumerate(parsed):
            q_text = item.get("q") or item.get("question") or ""
            options = item.get("options") or item.get("choices") or []
            answer = item.get("answer") or item.get("correct") or ""

            options = [str(o).strip() for o in options if str(o).strip()]
            if not options:
                options = ["True", "False", "Not sure", "Maybe"]

            ans_raw = str(answer).strip()
            if len(ans_raw) == 1 and ans_raw.upper() in ["A", "B", "C", "D"]:
                map_idx = ord(ans_raw.upper()) - ord("A")
                answer_text = options[map_idx] if 0 <= map_idx < len(options) else options[0]
            else:
                found = None
                for opt in options:
                    if opt.lower() in ans_raw.lower() or ans_raw.lower() in opt.lower():
                        found = opt
                        break
                answer_text = found if found else (options[0] if options else "")

            questions.append({"index": idx, "q": q_text, "options": options, "answer": answer_text})

        if len(questions) < total:
            questions.extend(make_dummy_questions(category, total - len(questions)))
    except Exception as e:
        print("PARSE ERROR:", e)  # 🔎 log error parse
        questions = make_dummy_questions(category, total)

    if len(questions) > total:
        questions = questions[:total]
    elif len(questions) < total:
        questions.extend(make_dummy_questions(category, total - len(questions)))

    quiz_id = create_quiz_record(username, category, total)
    save_quiz_questions(quiz_id, questions)

    return jsonify({"quiz_id": quiz_id, "questions": questions}), 201


@quiz_bp.route("/<int:quiz_id>/questions", methods=["GET"])
def get_questions(quiz_id):
    qs = get_quiz_questions(quiz_id)
    return jsonify({"quiz_id": quiz_id, "questions": qs})


@quiz_bp.route("/<int:quiz_id>/submit", methods=["POST"])
def submit_quiz(quiz_id):
    data = request.get_json() or {}
    answers = data.get("answers") or {}
    username = data.get("username") or "anonymous"

    questions = get_quiz_questions(quiz_id)
    total = len(questions)
    correct = 0
    wrong = 0
    details = []

    for q in questions:
        qid = str(q.get("index"))
        correct_answer = (q.get("answer") or "").strip()
        user_ans = (answers.get(qid) or "").strip()

        is_correct = norm(user_ans) == norm(correct_answer) if user_ans else False

        # fleksibilitas: jika correct_answer cuma huruf A/B/C/D
        if not is_correct and len(correct_answer) == 1 and correct_answer.upper() in ["A","B","C","D"]:
            idx = ord(correct_answer.upper()) - ord("A")
            opts = q.get("options") or []
            if 0 <= idx < len(opts) and norm(user_ans) == norm(opts[idx]):
                is_correct = True

        if is_correct:
            correct += 1
        else:
            wrong += 1

        details.append({
            "index": q.get("index"),
            "q": q.get("q"),
            "options": q.get("options"),
            "user_answer": user_ans,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

    score_percent = int((correct / total) * 100) if total > 0 else 0
    save_score(username, quiz_id, correct, wrong, total, score_percent)

    return jsonify({
        "quiz_id": quiz_id,
        "correct": correct,
        "wrong": wrong,
        "total": total,
        "score_percent": score_percent,
        "details": details
    })


@quiz_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    top = get_leaderboard(limit=10)
    return jsonify({"leaders": top})


