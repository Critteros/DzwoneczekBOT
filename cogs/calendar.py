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
from modules.calendar.calendar_handler import load_guild_latest


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
        def talk(*args, **kwargs):
            message_stack.append(
                context.send(*args, **kwargs)
            )

        # Verifies the author replies
        def check(message: discord.Message):
            is_correct_user: bool = message.author == context.author
            is_correct_channel: bool = message.channel == context.channel

            return is_correct_user and is_correct_channel

    @calendar_core.command(name='test', brief='For testing only')
    async def test(self, context: commands.Context):

        message_stack: List[discord.Message] = [context.message]
        log = self.log

        message_stack.append(
            await context.send('Please reply with __description__')
        )

        def check(message: discord.Message):
            return (message.author == context.author and message.channel == context.channel)

        try:
            reaction: discord.Message = await self.client.wait_for(
                'message', check=check, timeout=10)

            message_stack.append(reaction)
            message_stack.append(
                await context.send(f"Reaction was `{reaction.content}`")
            )
        except asyncio.TimeoutError:
            message_stack.append(
                await context.send('Timed out')
            )

        await asyncio.sleep(10)
        for msg in message_stack:
            await msg.delete()

        # load_guild_latest(context.guild.id)
        # await asyncio.sleep(3)
        # await context.send('After 3 seconds')


def setup(client):
    """
    Setup function for testing_cog extension

    Args:
        client (app.client.BotClient): Client that connects to discord API
    """
    client.add_cog(Calendar(client))
