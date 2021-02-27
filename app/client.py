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
            help_command=MyHelp(),
            *args, **kwargs
        )

        # To-do load cogs
        Log.warning('Loading cogs:')

        path_to_cogs = Path('cogs')

        for file in path_to_cogs.iterdir():
            file_name: str = file.name

            if file_name.endswith('.py'):
                cog_name: str = f'cogs.{file_name[:-3]}'
                Log.warning(f'\tloading cog: {cog_name}')
                self.load_extension(cog_name)

        Log.warning('Finished loading cogs')

        # Binding instance
        BotClient._INSTANCE = self

    async def start(self, *args, **kwargs):
        """
        Coroutine that starts the bot client.
        Shorthand for login() and connect()
        """

        await self.login(self.token, bot=True)
        await self.connect(reconnect=True)

    def run(self, *args, **kwargs) -> None:
        """
        Activates and runs the event loop
        This call is blocking and should be last thing that is called

        """
        Log.warning('Starting up connection to discord API')
        return super().run(*args, **kwargs)

    async def close(self) -> None:
        """
        Cleaning up and closing the event loop
        """
        Log.error('Logging out of discord')
        return await super().close()

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


class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.help)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            command_signatures = [
                self.get_command_signature(c) for c in commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(
                    command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


def _get_prefix(bot: BotClient, msg: discord.Message):
    bot_user_id = bot.user.id

    # Standard prefixes for direct ping @BOTNAME
    prefixes: list = [f'<@!{bot_user_id}> ', f'<@{bot_user_id} ']

    # Check if it is a private chanell
    if msg.guild is None:
        prefixes.append('!')
        prefixes.append('?')
        Log.debug('Getting prefix for private DM')
    else:
        Log.debug(f'Getting prefix for server: {msg.guild.name}')
        guild_id: int = msg.guild.id
        custom_prefix: str = get_server_prefix(guild_id)

        # Check if the prefix is not an empty string
        if custom_prefix:
            prefixes.append(custom_prefix)
        else:
            prefixes.append('?')

    return prefixes
