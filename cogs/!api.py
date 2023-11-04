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

    @commands.command()
    async def create(self, ctx: commands.Context):
        file = open("./sound.mp3", "rb")
        b = file.read()

        sound = await ctx.guild.create_soundboard_sound(name="test", sound=b)

    @commands.command()
    async def edit(self, ctx: commands.Context):
        sound = ctx.guild.get_soundboard_sound(1169019023334318150)
        print(sound)
        sound = await sound.edit(name="asd", volume=0.34, emoji="👍", reason="LolTEst")
        print(sound)

    @commands.command()
    async def sounds(self, ctx: commands.Context):
        sounds = ctx.guild.soundboard_sounds
        print(list(sounds))

    @commands.command()
    async def delete(self, ctx: commands.Context):
        sound = ctx.guild.get_soundboard_sound(1169019023334318150)
        await sound.delete()

    @commands.command()
    async def request(self, ctx: commands.Context):
        sounds = await ctx.guild.request_soundboard_sounds()
        print(sounds)

    @commands.command()
    async def fetch(self, ctx: commands.Context):
        sounds = await self.bot.fetch_soundboard_default_sounds()
        print(sounds)

    @commands.command()
    async def client_get(self, ctx: commands.Context, id: int):
        sound = self.bot.get_soundboard_sound(id)
        print(sound, sound.guild)

    @commands.command()
    async def client_sounds(self, ctx: commands.Context):
        sounds = []
        for sound in self.bot.soundboard_sounds:
            sounds.append((sound.guild.name, sound))

        print(sounds)

    @commands.Cog.listener()
    async def on_voice_channel_effect(self, effect: discord.VoiceChannelEffect):
        string = ("VOICE CHANNEL EFFECT\n"
                  "---------------------\n"
                  f"{effect.channel=}, {effect.user=}, {effect.animation=}, {effect.emoji=}, {effect.sound=}")

        if effect.is_sound():
            sound = effect.sound
            string += f", {sound.id}, {sound.volume}, {sound.created_at}, {sound.is_default()}, {sound.file}"

        string += "\n"
        print(string)

    @commands.Cog.listener()
    async def on_soundboard_sound_create(self, sound: discord.SoundboardSound):
        print("SOUNDBOARD CREATE\n"
              "------------------\n"
              f"{sound.available=}, {sound.created_at=}, {sound.emoji=}, {sound.guild=}, "
              f"{sound.guild_id=}, {sound.id=}, {sound.name=}, {sound.user=}, {sound.volume=}\n")

    @commands.Cog.listener()
    async def on_soundboard_sound_update(self, before: discord.SoundboardSound, after: discord.SoundboardSound):
        print("SOUNDBOARD UPDATE\n"
              "------------------\n"
              f"{before=}, {after=}\n")

    @commands.Cog.listener()
    async def on_soundboard_sound_delete(self, sound: discord.SoundboardSound):
        print("SOUNDBOARD DELETE\n"
              "------------------\n"
              f"{sound}\n")


async def setup(bot: Punchax):
    await bot.add_cog(APITests(bot))
