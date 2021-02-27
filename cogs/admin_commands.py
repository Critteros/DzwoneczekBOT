"""
Cog that holds command that will be only used by the discord server administrators
"""
# Library includes
from discord.ext import commands


# App includes

from app.client import BotClient
from app.logging.core import Log

from app.prefix_handler import set_server_prefix


class AdminCommands(commands.Cog):
    """
    Class cog for the admin_commands cog extension
    """

    def __init__(self, client: BotClient):
        self.client: BotClient = client

    @commands.group(name='prefix')
    @commands.guild_only()
    async def prefix_core(self, context: commands.Context):
        """
        Main handler for the prefix command

        Args:
            context (commands.Context): context of the invocation
        """
        if context.invoked_subcommand is None:
            await context.reply('Invalid Subcommand')

    @prefix_core.command(name='set')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def prefix_change(self, context: commands.Context, new_prefix: str):
        """
        Changes the current server command prefix

        Args:
            context (commands.Context): context of invocation
            new_prefix (str): the new prefix to be set
        """
        guild_id: int = context.guild.id
        Log.info(
            f'Changing prefix in guild "{context.guild.name} to "{new_prefix}"')

        set_server_prefix(guild_id, new_prefix)

        await context.send(f'Changed server prefix to {new_prefix}')

    @prefix_core.command(name='current')
    @commands.guild_only()
    async def prefix_current(self, context: commands.Context):
        """
        Retrives the current prefix

        Args:
            context (commands.Context): context of the invocation
        """
        curr_prefix: str = (await self.client.get_prefix(context))[2]
        await context.send(f'Current prefix is set to "{curr_prefix}"')


def setup(client):
    """
    Setup function for admin_commands extension

    Args:
        client (app.client.BotClient): Client that connects to discord API
    """
    client.add_cog(AdminCommands(client))
