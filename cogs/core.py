"""The core of the discord bot."""
from discord.ext import commands
import random
import discord
import datetime
import os
import re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




class Core(commands.Cog):
    """The core of the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(datetime.datetime.utcnow())
        print(f'Successfully connected as {self.bot.user}')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def recount(self, ctx: commands.Context, *args):
        await ctx.message.delete()
        if ctx.channel.id == 699762298721665158 or ctx.channel.id == 794908427809062912:
            print("success", args)
            mes_limit = None
            bool_limit = False
            limited = False
            if args != ():
                mes_limit = int(args[0])
                bool_limit = True
                limited = True
            previous_message = "0 0"
            count = 0
            async for m in ctx.channel.history(limit=None, oldest_first=True):
                try:
                    if bool_limit and limited:
                        count += 1
                        if count >= mes_limit:
                            limited = False
                    if not limited:
                        pre = previous_message.replace("("," ").split(" ")[0].strip()
                        pre = re.sub("[^0-9]", " ", pre)
                        message_content = m.content
                        #if (int(pre) + 1) != int(cur):
                        if not message_content.startswith(str(int(pre)+1)):
                            print("Bad count:", int(previous_message.split(" ")[0]), int(m.content.split(" ")[0]))
                            #await ctx.channel.send(m.jump_url, delete_after=120)
                            await ctx.channel.send(m.jump_url)
                        previous_message = m.content

                except ValueError as e:
                    pass
                    #print(e, previous_message, m.content)
            print("done")
