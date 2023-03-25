from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from .utils.types import Context

if TYPE_CHECKING:
    from main import PPyte


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

    @commands.hybrid_command(name="delete_thread", description="Deletes a thread")
    async def delete_thread(self, ctx, thread_id: int):
        thread = ctx.channel.get_thread(thread_id)
        if thread is None:
            thread = await ctx.guild.fetch_channel(thread_id)

        await thread.delete()

async def setup(bot: PPyte):
    await bot.add_cog(APITests(bot))
