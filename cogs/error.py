from typing import Callable

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog, Context, CommandError, errors

from .utils.common import Color
from .utils.dt import TIMEZONE, Datetime


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

        parent = super().__init__(**kwargs)
        parent.set_author(name="Error")


class ErrorHandler(Cog):
    """Handles command errors globally."""

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):

        if isinstance(error, errors.CommandNotFound):
            return

        elif isinstance(error, errors.MissingRequiredArgument):
            content = "**A required argument is missing!**"

            embed = _ErrorEmbed(content, ctx=ctx)
            await ctx.send(embed=embed)

        else:
            dt = Datetime.get_local_datetime()
            dt.strftime("%y%m%d_")

            content = """
            **An unexpected error has occurred!**
            The full traceback has been sent to the owner.
            """

            # TODO send full traceback via .txt to log channel
            #   - only short traceback as content

            raise error


async def setup(bot):
    await bot.add_cog(ErrorHandler())
