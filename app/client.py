"""
This module contains client class BotClient which is used to communicate with DiscordAPI
"""
# Lib includes
from pathlib import Path
import asyncio

from discord.ext import commands
import discord

# App includes
from app.logging.core import Log
from app.prefix_handler import get_server_prefix


class BotClient(commands.Bot):
    """
    The main client used in application to communicate with Discord API.
    It is a Singleton class thus only one instance of this class can be active at once
    Attempting to create second instance of this class will results in RuntimeError

    Raises:
        RuntimeError: When creating more then one instance
        RuntimeError: If discord token file does not exists ".discord."
        RuntimeError: If accesing get_instance() before creating instance of this class

    Returns:
        BotClient: Instance of client class
    """
    _INSTANCE = None

    def __init__(self, *args, **kwargs) -> None:

        # This class is an singleton so there can bo only one instance
        if BotClient._INSTANCE is not None:
            raise RuntimeError(
                'Called BotClient constructor when instance arleady existed')

        # Read discord token file
        token_file = Path('.discord')

        if not token_file.exists():  # Handle if token file does not exists
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
        Log.warning('Loading cogs:')

        path_to_cogs = Path('app/cogs')

        for file in path_to_cogs.iterdir():
            file_name: str = file.name

            if file_name.endswith('.py'):
                cog_name: str = f'app.cogs.{file_name[:-3]}'
                Log.warning(f'\tloading cog: {cog_name}')
                self.load_extension(cog_name)

        # Binding instance
        BotClient._INSTANCE = self

    async def start(self, *args, **kwargs):
        """
        Coroutine that starts the bot client.
        Shorthand for login() and connect()
        """

        await self.login(self.token, bot=True)
        await self.connect(reconnect=True)

    @staticmethod
    def get_instance():
        """
        Returns singleton instance of BotClient class. Raises RuntimeError if it does not exists

        Raises:
            RuntimeError: If the singleton instance is missing

        Returns:
            BotClient: BotClient instance
        """

        if BotClient._INSTANCE is None:
            raise RuntimeError('There is no client instance')
        return BotClient._INSTANCE


def _get_prefix(bot: BotClient, msg: discord.Message):
    bot_user_id = bot.user.id

    # Standard prefixes for direct ping @BOTNAME
    prefixes: list = [f'<@!{bot_user_id}> ', f'<@{bot_user_id} ']

    # Check if it is a private chanell
    if msg.guild is None:
        prefixes.append('!')
        prefixes.append('?')
        Log.info('Invoked in private channel')
    else:
        Log.info('Invoked in serwer')
        guild_id: int = msg.guild.id
        custom_prefix: str = get_server_prefix(guild_id)

        # Check if the prefix is not an empty string
        if custom_prefix:
            prefixes.append(custom_prefix)
        else:
            prefixes.append('?')

    return prefixes
