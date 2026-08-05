from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CASPIAN_API_KEY = os.getenv("CASPIAN_API_KEY")
CASPIAN_BASE_URL = os.getenv("CASPIAN_BASE_URL")