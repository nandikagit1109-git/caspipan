from email.mime import message
import os
from pathlib import Path
from dotenv import load_dotenv

from caspian_sdk import CommClient

from ai import get_ai_response
from xp import add_xp
from database import init_db, save_chat

# Load .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Initialize database
init_db()

# Create Caspian client
client = CommClient()

# -------------------------
# EMAIL
# -------------------------
email = client.connect_email(username="quantumodyssey")
print(f"📧 Email Connected: {email['address']}")

# -------------------------
# DISCORD
# -------------------------
discord_token = os.getenv("DISCORD_BOT_TOKEN")

if discord_token:
    try:
        client.connect_discord(bot_token=discord_token)
        print("💬 Discord Connected")
    except Exception as e:
        print("Discord Error:", e)

print("🚀 Quantum Odyssey Running...")
print("Waiting for messages...\n")


from xp import add_xp, get_level
from database import save_chat
from ai import get_ai_response
from missions import get_mission

@client.on_message
def handle(message):

    user = (
        message.sender["address"]
        if isinstance(message.sender, dict)
        else str(message.sender)
    )

    text = message.text.strip()

    # ---------------- HELP ----------------
    if text.lower() == "/help":

        message.reply("""
🌌 Quantum Odyssey Commands

/help              → Show commands
/xp                → Check XP & Level
/mission           → Get today's mission

Just ask any study question naturally!

Examples:
• Explain Python loops
• Quiz me on AI
• What is Machine Learning?
""")
        return

    # ---------------- XP ----------------
    if text.lower() == "/xp":

        xp = add_xp(user) - 10   # display current XP without awarding extra

        level = get_level(xp)

        message.reply(
            f"""⭐ Your Progress

XP : {xp}

🏆 Level : {level}
"""
        )
        return

    # ---------------- MISSION ----------------
    if text.lower() == "/mission":

        message.reply(get_mission())
        return

    # ---------------- NORMAL AI ----------------

    save_chat(user, "USER", text)

    xp = add_xp(user)

    level = get_level(xp)

    reply = get_ai_response(text)

    save_chat(user, "AI", reply)

    message.reply(
        f"""{reply}

━━━━━━━━━━━━━━
⭐ XP : {xp}
🏆 Level : {level}
"""
    )
client.listen()