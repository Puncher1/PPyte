from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord import app_commands

from utils.types import Context
from .common import GuildID

if TYPE_CHECKING:
    from main import Punchax


DEV_TEST_GUILD_ID = GuildID.dev_test


class APITests(commands.Cog):
    """Commands and Events to test the API.
    This cog is not loaded on startup and has to be loaded with the `load` command
    """

    def __int__(self, bot: Punchax):
        self.bot: Punchax = bot

    @commands.command()
    async def reply_overload(self, ctx: Context):
        await ctx.send("ctx.send")
        await ctx.reply("ctx.reply")
        pass

    @app_commands.command(name="ephemeral")
    @app_commands.guilds(DEV_TEST_GUILD_ID)
    async def _ephemeral(self, interaction: discord.Interaction):
        await interaction.response.send_message("Command", ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_channel_effect(self, effect: discord.VoiceChannelEffect):
        print(effect)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        print(f"Action: {entry.action}, Extra: {entry.extra}, Changes: {entry.changes}, Target: {entry.target}")


async def setup(bot: Punchax):
    await bot.add_cog(APITests(bot))
