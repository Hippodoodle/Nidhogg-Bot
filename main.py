import os

from discord.ext import commands
from dotenv import load_dotenv

from cogs.core import Core
from cogs.WIPCommands import WIPCommands
from cogs.moderation import Moderation
from cogs.counting import Counting


load_dotenv()


bot = commands.Bot(command_prefix="?")


print("Loading Cogs ...")

bot.add_cog(Core(bot))
print("Core cog loaded")

bot.add_cog(WIPCommands(bot))
print("WIPCommands cog loaded")

bot.add_cog(Moderation(bot))
print("Moderation cog loaded")

bot.add_cog(Counting(bot))
print("Counting cog loaded")


print("Running Bot...")
bot.run(os.environ['DISCORD_TOKEN'])
