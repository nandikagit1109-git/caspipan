import os
from pathlib import Path

from dotenv import load_dotenv
from caspian_sdk import CommClient
from app.ai import get_ai_response
from app.xp import add_xp, get_xp, get_level
from app.database import init_db, save_chat
from app.badges import get_badge
from app.streak import init_streak, update_streak
from app.commands import handle_command


# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)


# ==========================================================
# DATABASE
# ==========================================================

init_db()
init_streak()


# ==========================================================
# CASPIAN
# ==========================================================

client = CommClient()


# ==========================================================
# EMAIL
# ==========================================================

try:

    email = client.connect_email(
        username="quantumodyssey"
    )

    print(
        f"📧 Email Connected: {email['address']}"
    )

except Exception as e:

    print("❌ Email Error:", e)


# ==========================================================
# DISCORD
# ==========================================================

discord_token = os.getenv(
    "DISCORD_BOT_TOKEN"
)

if discord_token:

    try:

        client.connect_discord(
            bot_token=discord_token
        )

        print("💬 Discord Connected")

    except Exception as e:

        print("❌ Discord Error:", e)


# ==========================================================
# START
# ==========================================================

print()
print("🚀 Quantum Odyssey Running...")
print("🧠 AI Mentor: Online")
print("⭐ XP System: Online")
print("🏆 Badges: Online")
print("🔥 Streaks: Online")
print("📚 Learning Tools: Online")
print()
print("Waiting for messages...")
print()


# ==========================================================
# MESSAGE HANDLER
# ==========================================================

@client.on_message
def handle(message):

    try:

        # --------------------------------------------------
        # USER
        # --------------------------------------------------

        if isinstance(message.sender, dict):

            user = (
                message.sender.get("address")
                or message.sender.get("name")
                or "unknown-user"
            )

        else:

            user = str(message.sender)


        # --------------------------------------------------
        # TEXT
        # --------------------------------------------------

        text = (
            message.text.strip()
            if message.text
            else ""
        )
        if not text:
            return


        if not text:

            return


        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📩 User: {user}")
        print(f"💬 Message: {text}")


        # ==================================================
        # COMMAND
        # ==================================================

        command = handle_command(
            user,
            text
        )


        if command:

            # ----------------------------------------------
            # NORMAL REPLY
            # ----------------------------------------------

            if command["type"] == "reply":

                message.reply(
                    command["text"]
                )

                return


            # ----------------------------------------------
            # AI COMMAND
            # ----------------------------------------------

            if command["type"] == "ai":

                save_chat(
                    user,
                    "USER",
                    text
                )

                reply = get_ai_response(
                    user,
                    command["prompt"]
                )

                save_chat(
                    user,
                    "AI",
                    reply
                )

                xp = add_xp(
                    user,
                    20
                )

                level = get_level(xp)

                badge = get_badge(xp)

                streak = update_streak(
                    user
                )

                prefix = command.get(
                    "prefix",
                    ""
                )

                message.reply(
                    f"""{prefix}{reply}

━━━━━━━━━━━━━━━━━━

⭐ XP: {xp}
🏆 Level: {level}
🎖 Badge: {badge}
🔥 Streak: {streak} day(s)
"""
                )

                return


        # ==================================================
        # NORMAL AI CHAT
        # ==================================================

        save_chat(
            user,
            "USER",
            text
        )

        reply = get_ai_response(
            user,
            text
        )

        save_chat(
            user,
            "AI",
            reply
        )


        # --------------------------------------------------
        # REWARD
        # --------------------------------------------------

        xp = add_xp(
            user,
            10
        )

        level = get_level(
            xp
        )

        badge = get_badge(
            xp
        )

        streak = update_streak(
            user
        )


        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        message.reply(
            f"""{reply}

━━━━━━━━━━━━━━━━━━

⭐ XP: {xp}
🏆 Level: {level}
🎖 Badge: {badge}
🔥 Streak: {streak} day(s)
"""
        )


        print("✅ Reply sent")


    except Exception as e:

        print(
            "❌ Handler Error:",
            repr(e)
        )

        try:

            message.reply(
                f"❌ Something went wrong: {e}"
            )

        except Exception:

            pass


# ==========================================================
# LISTEN
# ==========================================================

client.listen()