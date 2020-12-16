"""The core of the discord bot."""
from discord.ext import commands


class Core(commands.Cog):
    """The core of the bot."""

    def __init__(self, bot):
        self.bot = bot
