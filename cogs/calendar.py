"""
Main calendar cog
"""
# Library includes
import asyncio
from typing import List


import discord
from discord.ext import commands


# App includes

from app.client import BotClient
from modules.calendar.calendar_handler import load_guild_latest, next_uid


class Calendar(commands.Cog, name='Calendar'):
    """
    Class cog for the calendar extension
    """

    def __init__(self, client: BotClient):
        self.client: BotClient = client
        self.log = client.log

    @commands.group(name='calendar', brief='Manages calendar')
    @commands.guild_only()
    async def calendar_core(self, context: commands.Context):

        if context.invoked_subcommand is None:
            await context.reply('Invalid subcommand')

    @calendar_core.command(name='add', brief='Adds event to calendar')
    async def add(self, context: commands.Context):

        # Binding logger
        log = self.log

        # Holder for message for later deletion
        message_stack: List[discord.Message] = [context.message]
        log = self.log

        # Used to communicate in desired channel
        async def talk(*args, **kwargs) -> discord.Message:
            send_message: discord.Message = await context.send(*args, **kwargs)
            message_stack.append(
                send_message
            )
            return send_message

        # Delete messages
        async def clenup():
            await asyncio.sleep(10)
            for message in message_stack:
                await message.delete()

        # Verifies the author replies

        def check(message: discord.Message) -> bool:
            is_correct_user: bool = message.author == context.author
            is_correct_channel: bool = message.channel == context.channel

            return is_correct_user and is_correct_channel

        await talk('Please reply with __Description__')

        try:
            user_reaction: discord.Message = await self.client.wait_for(
                event='message',
                check=check
            )
            message_stack.append(user_reaction)
            await talk(f'Message content is `{user_reaction.content}`')
        except asyncio.TimeoutError:
            await talk(f'Timed Out!')
            await clenup()

    @calendar_core.command(name='test', brief='For testing only')
    async def test(self, context: commands.Context):
        for _ in range(10):
            await context.send(f'ID: {next_uid(context.guild.id)}')


def setup(client):
    """
    Setup function for testing_cog extension

    Args:
        client (app.client.BotClient): Client that connects to discord API
    """
    client.add_cog(Calendar(client))
