import os
from dotenv import load_dotenv

from bot import Punchax

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    Punchax().run(TOKEN)  # type: ignore
