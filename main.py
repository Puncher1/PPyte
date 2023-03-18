import os
from dotenv import load_dotenv

from bot import PPyte

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    PPyte().run(TOKEN)  # type: ignore
