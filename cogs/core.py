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
        print(datetime.now())
        print(f'Successfully connected as {self.bot.user}')

    @commands.command()
    async def doodle(self, ctx, *args):
        r = ["You are not alone. You have us.", "Life is challenging. It really is... I don't have many inspirational words for you this time. Just do your best and hopefully that works out.", "Sometimes it's okay to cry.", "Don't start smoking or you'll get nicotine withdrawals if you don't smoke. Then you'll become an asshole.", "Your life makes a difference in this world.", "Be inspired by your idols. Walk your own path.", "No matter how bad things may seem, the pain is only in your head.", "Make the best of all your years, because soon enough the year will be your last.", "Remember to drink water.",
             "You are the source of your own happiness. Explore what brings you joy.", "Don't be afraid to befriend someone out of your social norms or comfort zone.", "You have to take action to change something. You can't stay in silence and expect something to change.", "Stars cannot shine without darkness", "You're amazing. And one day, someone who matters more to you will know it too.", "Go outside in the sun and park. Read or get away from what you are doing! Distract yourself.", "I just want you all to find what makes you happy and stick to it. Don't get sucked into bad vibes okay?", "Proper sleep is necessary for the body to function at it's best"]
        random_thing = random.randint(0, len(r))
        embed = discord.Embed(title=r[random_thing], color=0xFBAED2)
        embed.set_footer(text="Stay hydrated")
        await ctx.message.channel.send(embed=embed)
