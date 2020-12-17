import os

from discord.ext import commands
from dotenv import load_dotenv

from cogs import core

load_dotenv()

bot = commands.Bot(command_prefix="?")

bot.run(os.environ['DISCORD_TOKEN'])
