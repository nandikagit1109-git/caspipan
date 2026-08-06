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


@client.on_message
def handle(message):

    print("\nNew Message")
    print("User :", message.sender)
    print("Text :", message.text)

    user = (
        message.sender["address"]
        if isinstance(message.sender, dict)
        else str(message.sender)
    )

    save_chat(user, "USER", message.text)

    xp = add_xp(user)

    reply = get_ai_response(message.text)

    save_chat(user, "AI", reply)

    final_reply = f"""{reply}

━━━━━━━━━━━━━━
⭐ XP : {xp}
"""

    message.reply(final_reply)

client.listen()