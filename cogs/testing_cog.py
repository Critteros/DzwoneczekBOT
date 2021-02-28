"""
Extension desined to test bot functionality, just for testing
"""
# Library includes

from discord.ext import commands


# App includes

from app.client import BotClient


class TestCog(commands.Cog):
    """
    Class cog for the testing_cog cog extension
    """

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.log = client.log

    @commands.command(help='test', brief='Testing command')
    async def echo(self, ctx: commands.Context, *args):
        """
        Testing fuction designed to print context to logging output

        Args:
            ctx (commands.Context): Context of invocation
        """
        log = self.log

        log.debug('Executing echo command')
        log.debug(f'Context is: {ctx.__dict__}')
        log.debug(f'Context type is {type(ctx)}')
        log.debug(f'Context message: {ctx.args}')

        log.debug(f'data is: /{args}/\n data type is{type(args)}')
        await ctx.message.reply("Hi <:python:815369954224373760>")


def setup(client):
    """
    Setup function for testing_cog extension

    Args:
        client (app.client.BotClient): Client that connects to discord API
    """
    client.add_cog(TestCog(client))
