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

    @commands.command()
    async def automodruleaction_overload(self, ctx: Context):
        rule_action = discord.AutoModRuleAction(type=discord.AutoModRuleActionType.block_message, channel_id=123)

    @app_commands.command(name="ephemeral")
    @app_commands.guilds(DEV_TEST_GUILD_ID)
    async def _ephemeral(self, interaction: discord.Interaction):
        await interaction.response.send_message("Command", ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_channel_effect(self, effect: discord.VoiceChannelEffect):
        if effect.is_sound():
            default = await effect.sound.is_default()
        else:
            default = None
        print(effect, default, effect.sound.id)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        print(f"Action: {entry.action}, Extra: {entry.extra}, Changes: {entry.changes}, Target: {entry.target}")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        print(interaction.channel_id)
        print(interaction.channel)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        print(f"USER_UPDATE")
        print(before != after)
        print(f"Avatar: {before.avatar}, {after.avatar}")
        print(f"Avatar Decoration: {before.avatar_decoration}, {after.avatar_decoration}")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.guild.id == DEV_TEST_GUILD_ID:
            print(f"MEMBER_UPDATE")
            print(f"Avatar: {before.avatar}, {after.avatar}")
            print(f"Avatar Decoration: {before.avatar_decoration}, {after.avatar_decoration}")

    # @commands.Cog.listener()
    # async def on_soundboard_sound_create(self, sound: discord.SoundboardSound):
    #     print("CREATE")
    #     print(sound)
    #
    # @commands.Cog.listener()
    # async def on_soundboard_sound_update(self, before: discord.SoundboardSound, after: discord.SoundboardSound):
    #     print("UPDATE")
    #     print(f"{before=}, {after=}")
    #
    # @commands.Cog.listener()
    # async def on_soundboard_sound_delete(self, sound: discord.SoundboardSound):
    #     print("DELETE")
    #     print(sound)

async def setup(bot: Punchax):
    await bot.add_cog(APITests(bot))
