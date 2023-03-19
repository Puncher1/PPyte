from __future__ import annotations
from typing import TYPE_CHECKING
from discord.ext import commands

if TYPE_CHECKING:
    from bot import PPyte


class Color(commands.Cog):
    ERROR = 0xB00C0C


async def setup(bot: PPyte):
    await bot.add_cog(Color())
