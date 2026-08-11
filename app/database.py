import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "quantum_odyssey.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xp (
            user TEXT PRIMARY KEY,
            points INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def save_chat(user, role, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chats(user, role, message)
        VALUES (?, ?, ?)
        """,
        (user, role, message)
    )

    conn.commit()
    conn.close()


def get_history(user, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM chats
        WHERE user = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user, limit)
    )

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    history = []

    for role, message in rows:
        history.append({
            "role": "user" if role == "USER" else "assistant",
            "content": message
        })

    return history
def save_performance(user, topic, score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            topic TEXT,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        "INSERT INTO performance (user, topic, score) VALUES (?, ?, ?)",
        (user, topic, score)
    )

    conn.commit()
    conn.close()


def get_average_score(user, topic):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(score)
        FROM performance
        WHERE user = ? AND topic = ?
        """,
        (user, topic)
    )

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return None

    return round(result)