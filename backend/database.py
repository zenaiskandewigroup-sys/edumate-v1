import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "edumate.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    # users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # chats (per user)
    c.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT, -- 'user' or 'bot'
        message TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # quizzes (metadata)
    c.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        category TEXT,
        total INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # quiz_questions (store JSON strings)
    c.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        q_index INTEGER,
        question TEXT,
        options TEXT, -- JSON stringified list
        answer TEXT,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    )""")
    # scores
    c.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        quiz_id INTEGER,
        correct INTEGER,
        wrong INTEGER,
        total INTEGER,
        score INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()


