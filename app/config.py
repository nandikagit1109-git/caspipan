import os
from dotenv import load_dotenv

load_dotenv()

CASPIAN_API_KEY = os.getenv("CASPIAN_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")