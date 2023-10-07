from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord import app_commands
from discord.audit_logs import _AuditLogProxy

from utils.types import Context
from .common import GuildID

if TYPE_CHECKING:
    from main import Punchax


DEV_TEST_GUILD_ID = GuildID.dev_test


class APITests(commands.Cog):
    """Commands and Events to test the API.
    This cog is not loaded on startup and has to be loaded with the `load` command.
    """

    def __init__(self, bot: Punchax):
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
        extra = None
        if entry.extra is not None:
            if isinstance(entry.extra, _AuditLogProxy):
                attrs = " ".join([f"{k}={v!r}" for k, v in entry.extra.__dict__.items()])
                extra = f"<{entry.extra.__class__.__name__} {attrs}>"
            else:
                extra = entry.extra

        print(f"Action: {entry.action}, Changes: {entry.changes}, Extra: {extra}, Target: {entry.target}")

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

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print("RAW_ADD", payload.burst, payload.burst_colours, payload.burst_colors)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print("RAW_REMOVE", payload.burst, payload.burst_colours, payload.burst_colors)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print("ADD", reaction.me, reaction.me_burst, reaction.burst_colours, reaction.burst_colors, reaction.count_details)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user, is_burst):
        print(
            "REMOVE",
            reaction.me,
            reaction.me_burst,
            reaction.burst_colours,
            reaction.burst_colors,
            reaction.count_details,
            is_burst,
        )

    @commands.command()
    async def add(self, ctx, msg_id: int):
        msg = await ctx.channel.fetch_message(msg_id)
        await msg.add_reaction("👍")

    @commands.command()
    async def remove(self, ctx, msg_id: int):
        msg = await ctx.channel.fetch_message(msg_id)
        await msg.remove_reaction("👍", member=self.bot.user)

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
