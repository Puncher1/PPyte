from __future__ import annotations

import os
from typing import TYPE_CHECKING, List, Optional
from enum import Enum

import discord
from discord.ext import commands
from discord.ext.commands import errors

from .common import Color, Emoji

if TYPE_CHECKING:
    from bot import PPyte
    from .utils.types import Context


class _ExtensionState(Enum):
    loaded = 0
    unloaded = 1
    reloaded = 2


class Admin(commands.Cog):
    """Admin-only commands which only can be used by the owner."""

    def __init__(self, bot: PPyte):
        self.bot: PPyte = bot

    async def cog_check(self, ctx: Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def load(self, ctx: Context, *, extension: str):
        try:
            await self.bot.load_extension(extension)
        except Exception as e:
            content = f"**Failed loading `{extension}`!**\n```{e.__class__.__name__}: {e}```"
        else:
            content = f"**Successfully loaded `{extension}`!**"

        await ctx.reply(content, mention_author=True)

    @commands.command()
    async def unload(self, ctx: Context, *, extension: str):
        try:
            await self.bot.unload_extension(extension)
        except Exception as e:
            content = f"**Failed unloading `{extension}`!**\n```{e.__class__.__name__}: {e}```"
        else:
            content = f"**Successfully unloaded `{extension}`!**"

        await ctx.reply(content, mention_author=True)

    @commands.group(name="reload", invoke_without_command=True)
    async def _reload(self, ctx: Context, *, extension: str):
        try:
            await self.bot.reload_extension(extension)
        except Exception as e:
            content = f"**Failed reloading `{extension}`!**\n```{e.__class__.__name__}: {e}```"
        else:
            content = f"**Successfully reloaded `{extension}`!**"

        await ctx.reply(content, mention_author=True)

    async def reload_or_load_extension(self, extension: str) -> _ExtensionState:
        try:
            await self.bot.load_extension(extension)
            ext_state = _ExtensionState.loaded
        except errors.ExtensionAlreadyLoaded:
            await self.bot.reload_extension(extension)
            ext_state = _ExtensionState.reloaded

        return ext_state

    def get_cogs_embed(
        self,
        *,
        loaded: List[str],
        unloaded: List[str],
        reloaded: Optional[List[str]] = None,
        failed: Optional[List[str]] = None,
    ) -> discord.Embed:

        if reloaded is None:
            reloaded = []

        if failed is None:
            failed = []

        loaded_content = "\n".join(loaded)
        unloaded_content = "\n".join(unloaded)
        reloaded_content = "\n".join(reloaded)
        failed_content = "\n".join(failed)

        if len(loaded) > 0:
            loaded_content = f"{Emoji.arrow_up} **Loaded - [{len(loaded)}]**\n{loaded_content}\n\n"

        if len(unloaded) > 0:
            unloaded_content = f"{Emoji.arrow_down} **Unloaded - [{len(unloaded)}]**\n{unloaded_content}\n\n"

        if len(reloaded) > 0:
            reloaded_content = f"{Emoji.arrows_counterclockwise} **Reloaded - [{len(reloaded)}]**\n{reloaded_content}\n\n"

        if len(failed) > 0:
            failed_content = f"{Emoji.x} **Failed - [{len(failed)}]**\n{failed_content}"

        description = f"{loaded_content}{unloaded_content}{reloaded_content}{failed_content}"
        embed = discord.Embed(color=Color.info, description=description)

        return embed

    @_reload.command(name="all")
    async def _reload_all(self, ctx: Context):
        available_extensions = self.bot.get_extensions()

        loaded = []
        unloaded = []
        reloaded = []
        failed = []

        future_unload = [ext for ext in self.bot.extensions if ext not in available_extensions]
        for extension in future_unload:
            try:
                await self.bot.unload_extension(extension)
                unloaded.append(f"`{extension}`")
            except Exception as e:
                failed.append(f"`{extension}`: `{e.__class__.__name__}`")

        for extension in available_extensions:
            try:
                ext_state = await self.reload_or_load_extension(extension)
            except Exception as e:
                failed.append(f"`{extension}`: `{e.__class__.__name__}`")
            else:
                ext_str = f"`{extension}`"
                if ext_state == _ExtensionState.loaded:
                    loaded.append(ext_str)
                elif ext_state == _ExtensionState.reloaded:
                    reloaded.append(ext_str)

        embed = self.get_cogs_embed(loaded=loaded, unloaded=unloaded, reloaded=reloaded, failed=failed)
        embed.title = "Cogs Update"

        await ctx.reply(embed=embed, mention_author=True)

    def get_all_extensions(self) -> List[str]:
        all_extensions = []

        ext_dir = f"./cogs"
        for filename in os.listdir(ext_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                all_extensions.append(f"cogs.{filename[:-3]}")

        return all_extensions

    @commands.group(name="cogs")
    async def _cogs(self, ctx: Context):
        pass

    @_cogs.command(name="list")
    async def _reload_list(self, ctx: Context):
        all_extensions = self.get_all_extensions()
        unloaded = [f"`{ext}`" for ext in all_extensions if ext not in self.bot.extensions]
        loaded = [f"`{ext}`" for ext in self.bot.extensions]

        embed = self.get_cogs_embed(loaded=loaded, unloaded=unloaded)
        embed.title = "Cogs List"

        await ctx.reply(embed=embed)

    @commands.command(name="eval")
    async def _eval(self, ctx: Context, *, code: str):
        """Evaluates Python code provided by the user."""
        raise TypeError("test lololol")


async def setup(bot: PPyte):
    await bot.add_cog(Admin(bot))
