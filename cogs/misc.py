from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from .utils.types import Context

if TYPE_CHECKING:
    from bot import Punchax


# ----- Default Permissions -----
# Read Messages/View Channels
# Send Messages
# Send Messages in Threads
# Embed Links
# Attach Files
# Read Message History
# Use External Emojis
# Add Reactions
# Connect
# Speak
BOT_DEFAULT_PERMS = "274881432640"


class Misc(commands.Cog):
    def __init__(self, bot: Punchax):
        self.bot: Punchax = bot

    @commands.command()
    async def invite(self, ctx: Context, *, options: str = ""):
        perms = BOT_DEFAULT_PERMS
        if options == "admin":
            perms = "8"

        url = f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions={perms}&scope=bot"  # type ignore
        await ctx.send(url)


async def setup(bot: Punchax):
    await bot.add_cog(Misc(bot))
