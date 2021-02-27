

# Lib includes
from pathlib import Path
import asyncio

from discord.ext import commands
import discord

# App includes
from app.logging.core import Log
from app.prefix_handler import set_server_prefix, get_server_prefix


class BotClient(commands.Bot):

    INSTANCE = None

    def __init__(self, *args, **kwargs) -> None:

        # This class is an singleton so there can bo only one instance
        if BotClient.INSTANCE is not None:
            raise RuntimeError(
                'Called BotClient constructor when instance arleady existed')

        # Read discord token file
        token_file = Path('.discord')

        if not token_file.exists():
            raise RuntimeError('Discord token file does not exists')

        with token_file.open(mode='rt', encoding='utf-8') as file:
            self.token = file.read()

        # Retrive event loop
        self.loop = asyncio.get_event_loop()

        # Initialize Bot class constructor
        super().__init__(
            command_prefix=_get_prefix,
            *args, **kwargs
        )

        # To-do load cogs

    async def start(self, *args, **kwargs):
        """
        Coroutine that starts the bot client.
        Shorthand for login() and connect()
        """

        await self.login(self.token, bot=True)
        await self.connect(reconnect=True)

    @staticmethod
    def get_instance():

        if BotClient.INSTANCE is None:
            raise RuntimeError('There is no client instance')
        return BotClient.INSTANCE


def _get_prefix(bot: BotClient, msg: discord.Message):
    bot_user_id = bot.user.id
    prefixes: list = [f'<@!{bot_user_id}> ', f'<@{bot_user_id} ']

    if msg.guild is None:
        prefixes.append('!')
        prefixes.append('?')
        Log.info('Invoked in private channel')
    else:
        Log.info('Invoked in serwer')
        guild_id: int = msg.guild.id
        custom_prefix: str = get_server_prefix(guild_id)

        if custom_prefix:
            prefixes.append(custom_prefix)
            return prefixes
        else:
            prefixes.append('?')
            return prefixes
