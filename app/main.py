import os
from pathlib import Path
from dotenv import load_dotenv
from caspian_sdk import CommClient

# Load the .env file from the project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

print("API KEY:", os.getenv("CASPIAN_API_KEY"))

client = CommClient()

# Connect Email
email = client.connect_email(username="quantumodyssey")
print("Agent email:", email["address"])

# Connect Discord
client.connect_discord(
    bot_token=os.getenv("DISCORD_BOT_TOKEN")
)

# One handler for ALL channels
@client.on_message
def handle(message):
    print(f"Message from {message.sender}: {message.text}")

    reply = (
        "🌌 Welcome to Quantum Odyssey!\n\n"
        "I'm your AI Quantum Mentor.\n"
        "How can I help you today?"
    )

    message.reply(reply)

print("✅ Agent is running...")
client.listen()