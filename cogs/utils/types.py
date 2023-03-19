from __future__ import annotations

from typing import TYPE_CHECKING, Union

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import PPyte


class Context(commands.Context):
    author: Union[discord.User, discord.Member]
    channel: Union[
        discord.TextChannel,
        discord.StageChannel,
        discord.VoiceChannel,
        discord.Thread,
        discord.DMChannel,
        discord.GroupChannel,
    ]
    command: commands.Command
    prefix: str
    bot: PPyte


class GuildContext(Context):
    author: discord.Member
    channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.Thread]
    guild: discord.Guild
