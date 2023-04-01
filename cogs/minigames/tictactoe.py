from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from utils.types import Context

if TYPE_CHECKING:
    from bot import Punchax


class TicTacToe(commands.Cog):
    def __init__(self, bot: Punchax):
        self.bot: Punchax = bot

    @commands.command()
    async def tictactoe(self, ctx: Context):
        await ctx.send("Hello")


async def setup(bot: Punchax):
    await bot.add_cog(TicTacToe(bot))
