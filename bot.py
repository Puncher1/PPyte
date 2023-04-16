import os
from typing import List, Any

import discord
from discord.ext import commands

from utils.debug import log, LogLevel
from cogs.error import ErrorHandler

IGNORED_EXTENSIONS = ["!", "__init__"]
EXTENSIONS_DIRS = ["./cogs"]


class Punchax(commands.Bot):
    def __init__(self):
        command_prefix = "$"
        intents = discord.Intents.all()

        super().__init__(command_prefix=command_prefix, intents=intents)

    def get_all_extensions(self) -> List[str]:
        extensions = []

        for ext_dir in EXTENSIONS_DIRS:
            for filename in os.listdir(ext_dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    ext_dir = ext_dir.replace("./", "").replace("/", ".")
                    extensions.append(f"{ext_dir}.{filename[:-3]}")

        return extensions

    def get_allowed_extensions(self) -> List[str]:
        extensions = []

        for ext_dir in EXTENSIONS_DIRS:
            for filename in os.listdir(ext_dir):
                if filename.endswith(".py") and not any(ignore in filename for ignore in IGNORED_EXTENSIONS):
                    ext_dir = ext_dir.replace("./", "").replace("/", ".")
                    extensions.append(f"{ext_dir}.{filename[:-3]}")

        return extensions

    async def init_extensions(self):
        extensions = self.get_allowed_extensions()
        for ext in extensions:
            try:
                await self.load_extension(ext)
            except Exception as e:
                log(f"{e.__class__.__name__}: {e}", level=LogLevel.error)
                raise e

    async def setup_hook(self):
        await self.init_extensions()

    async def on_connect(self):
        log("Connected to Discord.", level=LogLevel.info)

    async def on_ready(self):
        log("Ready!", level=LogLevel.info)

    # on_error isn't applied in Cog.listener
    async def on_error(self, event: str, *args: Any, **kwargs: Any):
        await ErrorHandler(self).on_error(event=event)

    # TODO: remove; for testing burst reactions
    # async def on_raw_reaction_add(self, payload):
    #     print(f"raw_reaction_add {payload=}")
    #
    # async def on_reaction_add(self, reaction, user):
    #     print(f"reaction_add {reaction.burst=}, {reaction.count_details=}, {reaction.burst_colours=}")
    #
    # async def on_raw_reaction_remove(self, payload):
    #     print(f"raw_reaction_add {payload=}")
    #
    # async def on_reaction_remove(self, reaction, user):
    #     print(f"reaction_remove {reaction.burst=}, {reaction.count_details=}, {reaction.burst_colours=}")
