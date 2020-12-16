from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()

bot = commands.Bot()

bot.run(os.environ['DISCORD_TOKEN'])