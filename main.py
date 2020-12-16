import os

from discord.ext import commands
from dotenv import load_dotenv

import cogs

load_dotenv()

bot = commands.Bot(command_prefix="?")

bot.run(os.environ['DISCORD_TOKEN'])
