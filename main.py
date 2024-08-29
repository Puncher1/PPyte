import os
from dotenv import load_dotenv

import discord
from discord import app_commands

from bot import Punchax

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    bot = Punchax()

    @bot.tree.context_menu(name="Message call")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def msg_call(interaction: discord.Interaction, message: discord.Message) -> None:
        print(message.mentions)
        print(message.type)

        call = message.call
        await interaction.response.send_message(
            f"{call=}\n\n"
            f"{call.ended_timestamp=}\n\n"
            f"{call.participants=}\n\n"
            f"{call.duration=}\n\n"
            f"{call.is_ended()=}",
            ephemeral=True,
        )

    @bot.tree.context_menu(name="User action")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def user_action(interaction: discord.Interaction, user: discord.User) -> None:
        await interaction.response.send_message(f"Hello {user.name}")

    bot.run(TOKEN)
