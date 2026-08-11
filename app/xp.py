from .database import get_connection


def add_xp(user, amount=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT points FROM xp WHERE user = ?",
        (user,)
    )

    row = cursor.fetchone()

    if row is None:
        new_xp = amount

        cursor.execute(
            "INSERT INTO xp(user, points) VALUES (?, ?)",
            (user, new_xp)
        )
    else:
        new_xp = row[0] + amount

        cursor.execute(
            "UPDATE xp SET points = ? WHERE user = ?",
            (new_xp, user)
        )

    conn.commit()
    conn.close()

    return new_xp


def get_xp(user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT points FROM xp WHERE user = ?",
        (user,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return 0

    return row[0]


def get_level(xp):
    if xp < 100:
        return 1
    elif xp < 250:
        return 2
    elif xp < 500:
        return 3
    elif xp < 800:
        return 4
    elif xp < 1200:
        return 5
    elif xp < 2000:
        return 6
    else:
        return 7