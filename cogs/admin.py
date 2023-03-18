from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Cog, Context

if TYPE_CHECKING:
    from main import PPyte


class Admin(Cog):
    """Admin-only commands which only can be used by the owner."""

    def __init__(self, bot: PPyte):
        self.bot: PPyte = bot

    async def cog_check(self, ctx: Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="eval")
    async def _eval(self, ctx: Context, *, code: str):
        """Evaluates Python code provided by the user. """
        print("pass")
        pass


async def setup(bot):
    await bot.add_cog(Admin(bot))
