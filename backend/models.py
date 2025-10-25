import json
from database import get_db

# Users
def create_user(username, hashed_password):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return row

# Chats
def save_chat(username, role, message):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO chats (username, role, message) VALUES (?, ?, ?)", (username, role, message))
    conn.commit()
    conn.close()

def get_chats_for_user(username, limit=200):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT role, message, created_at FROM chats WHERE username=? ORDER BY id ASC LIMIT ?", (username, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Quiz flow
def create_quiz_record(username, category, total):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO quizzes (username, category, total) VALUES (?, ?, ?)", (username, category, total))
    qid = cur.lastrowid
    conn.commit()
    conn.close()
    return qid

def save_quiz_questions(quiz_id, questions):
    """
    questions: list of dicts with keys q, options (list), answer
    """
    conn = get_db()
    cur = conn.cursor()
    for idx, item in enumerate(questions):
        cur.execute(
            "INSERT INTO quiz_questions (quiz_id, q_index, question, options, answer) VALUES (?,?,?,?,?)",
            (quiz_id, idx,  # ✅ FIX: pakai idx mulai dari 0, bukan idx+1
             item.get("q") or item.get("question"),
             json.dumps(item.get("options") or item.get("choices") or []),
             item.get("answer"))
        )
    conn.commit()
    conn.close()

def get_quiz_questions(quiz_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT q_index, question, options, answer FROM quiz_questions WHERE quiz_id=? ORDER BY q_index ASC", (quiz_id,))
    rows = cur.fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({
            "index": r["q_index"],
            "question": r["question"],
            "options": json.loads(r["options"]),
            "answer": r["answer"]
        })
    return out

# Scores
def save_score(username, quiz_id, correct, wrong, total, score):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (username, quiz_id, correct, wrong, total, score) VALUES (?,?,?,?,?,?)",
                (username, quiz_id, correct, wrong, total, score))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, SUM(score) as total_score FROM scores GROUP BY username ORDER BY total_score DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"username": r["username"], "total_score": r["total_score"]} for r in rows]

