import os

from discord.ext import commands
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from bot.cogs.core import Core
from bot.cogs.WIPCommands import WIPCommands
from bot.cogs.moderation import Moderation
from bot.cogs.counting import Counting


load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **options):

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
