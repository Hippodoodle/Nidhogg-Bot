import os

from discord.ext import commands
from dotenv import load_dotenv

from cogs.core import Core

load_dotenv()

bot = commands.Bot(command_prefix="?")

print("Loading Cogs")
bot.add_cog(Core(bot))

print("Running Bot")
bot.run(os.environ['DISCORD_TOKEN'])
