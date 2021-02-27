"""
Extension desined to test bot functionality, just for testing
"""
# Library includes

from discord.ext import commands


# App includes

from app.client import BotClient
from app.logging.core import Log


class TestCog(commands.Cog):
    """
    Class cog for the testing_cog cog extension
    """

    def __init__(self, client: BotClient):
        self.client: BotClient = client

    @commands.command(help='test')
    @commands.guild_only()
    async def echo(self, ctx: commands.Context, *args):
        """
        Testing fuction designed to print context to logging output

        Args:
            ctx (commands.Context): Context of invocation
        """

        Log.debug('Executing echo command')
        Log.debug(f'Context is: {ctx.__dict__}')
        Log.debug(f'Context type is {type(ctx)}')
        Log.debug(f'Context message: {ctx.args}')

        Log.debug(f'data is: /{args}/\n data type is{type(args)}')
        await ctx.message.reply("Hi")


def setup(client):
    """
    Setup function for testing_cog extension

    Args:
        client (app.client.BotClient): Client that connects to discord API
    """
    client.add_cog(TestCog(client))
