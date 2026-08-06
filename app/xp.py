import sqlite3

DB = "quantum_odyssey.db"


def add_xp(user):

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS xp(
        user TEXT PRIMARY KEY,
        points INTEGER
    )
    """)

    cursor.execute(
        "SELECT points FROM xp WHERE user=?",
        (user,)
    )

    row = cursor.fetchone()

    if row:

        points = row[0] + 10

        cursor.execute(
            "UPDATE xp SET points=? WHERE user=?",
            (points, user)
        )

    else:

        points = 10

        cursor.execute(
            "INSERT INTO xp VALUES(?,?)",
            (user, points)
        )

    conn.commit()

    conn.close()

    return points


def get_level(points):

    return points // 100 + 1