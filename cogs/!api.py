from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord import app_commands

from .utils.types import Context
from .common import GuildID

if TYPE_CHECKING:
    from main import PPyte


DEV_TEST_GUILD_ID = GuildID.dev_test


class APITests(commands.Cog):
    """Commands and Events to test the API.
    This cog is not loaded on startup and has to be loaded with the `load` command
    """

    def __int__(self, bot: PPyte):
        self.bot: PPyte = bot

    @commands.command()
    async def reply_overload(self, ctx: Context):
        await ctx.send("ctx.send")
        await ctx.reply("ctx.reply")
        pass

    @app_commands.command(name="ephemeral")
    @app_commands.guilds(DEV_TEST_GUILD_ID)
    async def _ephemeral(self, interaction: discord.Interaction):
        await interaction.response.send_message("Command", ephemeral=True)


async def setup(bot: PPyte):
    await bot.add_cog(APITests(bot))
