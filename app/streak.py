from datetime import date, timedelta
from .database import get_connection


def init_streak():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
            user TEXT PRIMARY KEY,
            streak INTEGER DEFAULT 0,
            last_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def update_streak(user):
    conn = get_connection()
    cursor = conn.cursor()

    today = date.today()

    cursor.execute(
        """
        SELECT streak, last_date
        FROM streaks
        WHERE user = ?
        """,
        (user,)
    )

    row = cursor.fetchone()

    if row is None:
        streak = 1

        cursor.execute(
            """
            INSERT INTO streaks(user, streak, last_date)
            VALUES (?, ?, ?)
            """,
            (user, streak, str(today))
        )

    else:
        streak, last_date = row

        if last_date == str(today):
            pass

        elif last_date == str(today - timedelta(days=1)):
            streak += 1

            cursor.execute(
                """
                UPDATE streaks
                SET streak = ?, last_date = ?
                WHERE user = ?
                """,
                (streak, str(today), user)
            )

        else:
            streak = 1

            cursor.execute(
                """
                UPDATE streaks
                SET streak = ?, last_date = ?
                WHERE user = ?
                """,
                (streak, str(today), user)
            )

    conn.commit()
    conn.close()

    return streak


def get_streak(user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT streak FROM streaks WHERE user = ?",
        (user,)
    )

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else 0