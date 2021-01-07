"""The core of the discord bot."""
from discord.ext import commands
import random
import discord
import datetime


class Core(commands.Cog):
    """The core of the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(datetime.datetime.utcnow())
        print(f'Successfully connected as {self.bot.user}')
