import os
from typing import List, Any

from discord import Intents
from discord.ext import commands

from cogs.utils.debug import log, LogLevel
from cogs.error import ErrorHandler

IGNORED_EXTENSIONS = ["!", "__init__"]
EXTENSION_PATHS = ["cogs"]

class PPyte(commands.Bot):
    def __init__(self):
        command_prefix = "$"
        intents = Intents().all()

        super().__init__(command_prefix=command_prefix, intents=intents)

    def get_extensions(self) -> List[str]:
        extensions = []

        for ext in EXTENSION_PATHS:
            ext_dir = f"./{ext.replace('.', '/')}"
            for filename in os.listdir(ext_dir):
                if filename.endswith(".py") and not any(ignore in filename for ignore in IGNORED_EXTENSIONS):
                    extensions.append(f"{ext}.{filename[:-3]}")

        return extensions

    async def init_extensions(self):
        extensions = self.get_extensions()
        for ext in extensions:
            try:
                await self.load_extension(ext)
            except Exception as e:
                log(f"{e.__class__.__name__}: {e}", level=LogLevel.ERROR)
                raise e

    async def setup_hook(self):
        await self.init_extensions()

    async def on_connect(self):
        log("Connected to Discord.", level=LogLevel.INFO)

    async def on_ready(self):
        log("Ready!", level=LogLevel.INFO)
