from .database import get_connection


def get_top_users(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user, points
        FROM xp
        ORDER BY points DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def format_leaderboard():
    users = get_top_users()

    if not users:
        return "🏆 No learners on the leaderboard yet!"

    result = "🏆 QUANTUM ODYSSEY LEADERBOARD\n\n"

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for index, (user, points) in enumerate(users):
        medal = medals[index]

        result += f"{medal} {user}\n"
        result += f"   ⭐ {points} XP\n\n"

    return result