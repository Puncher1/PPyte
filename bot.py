from discord import Intents
from discord.ext import commands

from cogs.utils.debug import log, LogLevel

extensions = (
    'cogs.admin',
    'cogs.error',
)


class PPyte(commands.Bot):

    def __init__(self):
        command_prefix = "$"
        intents = Intents().all()

        super().__init__(
            command_prefix=command_prefix,
            intents=intents
        )

    async def _get_extensions(self):
        for ext in extensions:
            try:
                await self.load_extension(ext)
            except commands.ExtensionAlreadyLoaded:
                await self.reload_extension(ext)

    async def setup_hook(self):
        await self._get_extensions()

    async def on_connect(self):
        log("Connected to Discord.", level=LogLevel.INFO)

    async def on_ready(self):
        log("Ready!", level=LogLevel.INFO)
