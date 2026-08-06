import sqlite3

DB_NAME = "quantum_odyssey.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        role TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_chat(user, role, message):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(user,role,message) VALUES(?,?,?)",
        (user, role, message)
    )

    conn.commit()
    conn.close()


def get_history(user):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT role,message FROM chats WHERE user=? ORDER BY id DESC LIMIT 10",
        (user,)
    )

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    history = []

    for role, message in rows:

        if role == "USER":

            history.append({
                "role": "user",
                "content": message
            })

        else:

            history.append({
                "role": "assistant",
                "content": message
            })

    return history