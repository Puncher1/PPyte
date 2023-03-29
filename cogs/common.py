from __future__ import annotations
from typing import TYPE_CHECKING
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Punchax


class Color(commands.Cog):
    info = 0x3A99DE
    error = 0xB00C0C


class Emoji(commands.Cog):
    x = "❌"
    white_check_mark = "✅"

    arrows_counterclockwise = "🔄"
    arrow_up = "⬆️"
    arrow_down = "⬇️"


class GuildID(commands.Cog):
    dev_test = 673600173615611913


async def setup(bot: Punchax):
    await bot.add_cog(Color())
    await bot.add_cog(Emoji())
