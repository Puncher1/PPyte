from __future__ import annotations

import os
import traceback
import sys
from typing import TYPE_CHECKING, Any

import discord
from discord import Embed, File
from discord.ext import commands
from discord.ext.commands import errors

from .common import Color
from .utils.dt import Datetime
from .utils.debug import log, LogLevel

if TYPE_CHECKING:
    from bot import PPyte
    from .utils.types import Context


ERROR_LOG_CHANNEL_ID = 1086756809995468922


def get_full_traceback(error: commands.CommandError, /) -> str:
    """Returns the full traceback."""

    etype = type(error)
    trace = error.__traceback__

    lines = traceback.format_exception(etype, error, trace)
    full_traceback_text = ''.join(lines)

    return full_traceback_text


class _ErrorEmbed(Embed):
    def __init__(self, content: str, *, ctx: Context, try_again: bool = True, usage: bool = True):
        content += "\nPlease try again." if try_again else ""

        if usage:
            signature = f"{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}"
            content += f"\n\n**Usage:**\n`{signature}`"

        kwargs = {
            "color": Color.ERROR,
            "description": content,
        }
        self.set_author(name="Error")

        super().__init__(**kwargs)


class ErrorHandler(commands.Cog):
    """Handles command errors globally."""

    def __init__(self, bot: PPyte):
        self.bot: PPyte = bot

    def _get_log_file(self, error: commands.CommandError, /) -> File:
        dt = Datetime.get_local_datetime()
        dt_fm = dt.strftime("%y%m%d_%H%M%S")

        filename = f"error_{dt_fm}.txt"
        filepath = f"./log/{filename}"
        with open(filepath, "w+") as file:
            file.write(get_full_traceback(error))

        error_file = File(filepath, filename=filename)
        return error_file

    async def _send_to_log(self, description: str, error_file: File, /):
        error_log_channel: discord.TextChannel = self.bot.get_channel(ERROR_LOG_CHANNEL_ID)  # type: ignore
        await error_log_channel.send(content=description, file=error_file)

        os.remove(error_file.fp.name)  # type: ignore

    async def _process_ctx_error(self, *, error: Any, ctx: Context):
        error_file = self._get_log_file(error)
        description = (
            f"**Guild:** `{ctx.guild.name}` | `{ctx.guild.id}` \n"  # type: ignore
            f"**Short Traceback** \n"
            f"```{error.__class__.__name__}: {error}``` \n"
            f"**Full Traceback**"
        )
        await self._send_to_log(description, error_file)

        content = "**An unexpected error has occurred!** \n The full traceback has been sent to the owner."
        embed = _ErrorEmbed(content, ctx=ctx, try_again=False, usage=False)

        await ctx.send(embed=embed)

    async def _process_event_error(self, *, error: Any, event: str):
        error_file = self._get_log_file(error)
        description = (
            f"**Event:** `{event}` \n"  # type: ignore
            f"**Short Traceback** \n"
            f"```{error.__class__.__name__}: {error}``` \n"
            f"**Full Traceback**"
        )
        await self._send_to_log(description, error_file)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, errors.CommandNotFound):
            return

        elif isinstance(error, errors.MissingRequiredArgument):
            content = "**A required argument is missing!**"

            embed = _ErrorEmbed(content, ctx=ctx)
            await ctx.send(embed=embed)

        else:
            await self._process_ctx_error(error=error, ctx=ctx)
            log(f"{error.__class__.__name__}: {error}", level=LogLevel.ERROR, context=f"command:{ctx.command.name}")

    async def on_error(self, event: str):
        error = sys.exc_info()[1]
        await self._process_event_error(error=error, event=event)
        log(f"{error.__class__.__name__}: {error}", level=LogLevel.ERROR, context=f"event:{event}")


async def setup(bot: PPyte):
    await bot.add_cog(ErrorHandler(bot))
