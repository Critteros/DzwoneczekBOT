"""
Extension that contains event listeners that do not fall under their own category
"""


# Library includes
from discord.ext import commands


# App includes
from app.client import BotClient
from app.logging.core import Log


class ListenerCog(commands.Cog):
    """
    Class cog for the main_listener cog extension
    """

    def __init__(self, client: BotClient):
        self.client: BotClient = client

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Action that will be invoked when bot logs in into discord
        """
        Log.info('Bot is ready')
        Log.info(self.client.emojis)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """
        Listener to handle error caused by improper use of bot commands

        Args:
            ctx (commands.Context): context that invoked error
            error (commands.CommandError): error that was invoked
        """
        Log.error(f'Command error: "{error}"')

        # Check for error caused by DM bot directly with forbitted command
        if isinstance(error, commands.NoPrivateMessage):
            Log.warning(
                f'User: "{ctx.author.name}" id:{ctx.author.id} '
                'attempted to use command'
                f'"{ctx.command}" in private DM which is not permitted')
            await ctx.reply(
                f'Command "{ctx.command}" cannot be used in a private message. Sorry :(')

        if isinstance(error, commands.MissingPermissions):
            Log.warning(
                f'User: "{ctx.author.name}" id:{ctx.author.id}'
                f'attempted to use command "{ctx.command}" without needed permissions')
            await ctx.reply('You need Admin permissions to use that command')


def setup(client):
    """
    Setup function for main_listener extension

    Args:
        client (app.client.BotClient): Client that connects to discord API
    """
    client.add_cog(ListenerCog(client))
