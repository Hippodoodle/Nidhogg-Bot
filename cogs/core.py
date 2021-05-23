"""The core of the discord bot."""
from discord.ext import commands
import random
import discord
import datetime
import os
import re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODERATION_DIR = os.path.join(BASE_DIR, 'files/moderation_keywords.txt')

WARNING_DIR =  os.path.join(BASE_DIR, 'files/warning_keywords.txt')



def list_compare(a, b):
    for item in a:
        if item in b:
            return True
    return False

class Core(commands.Cog):
    """The core of the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(datetime.datetime.utcnow())
        print(f'Successfully connected as {self.bot.user}')

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Do things when a message is sent. """

        """ Ignore messages from the bot. """
        if message.author == self.bot.user:
            return

        """ Open moderation keyword file """
        try:
            f = open(MODERATION_DIR, "rt")
        except FileNotFoundError:
            print(os.getcwd())
        moderation_key_words = f.read()

        """ Process moderation keywords into a list """
        moderation_key_words = moderation_key_words.split("\n")

        """ Get the moderation log channel """
        log_channel = discord.utils.get(self.bot.get_all_channels(), guild=message.guild ,name='moderation-log')

        """ Process message words into a list """
        the_message = str(message.content).lower().replace(" ","")

        """ Compare words in each list """
        to_be_modded = list_compare(moderation_key_words, the_message)

        """ Silence individual users

        if message.author.id == 453226854518751242:
            to_be_modded = True
        
        """

        if to_be_modded:
            
            """ Moderation log message handling """
            if log_channel != None:
                embed = discord.Embed(title="Auto Moderation Used", timestamp=datetime.datetime.utcnow(), color=0xed900c)
                embed.add_field(name="User:", value=message.author, inline=True)
                embed.add_field(name="User id:", value=message.author.id, inline=True)
                embed.add_field(name="Nickname:", value=message.author.nick, inline=True)
                embed.add_field(name="Channel:", value=message.channel, inline=True)
                embed.add_field(name="Message:", value=message.content, inline=True)
                await log_channel.send(embed=embed)
            
            """ Moderated message handling """
            moderated_message = str(message.content).lower()
            for key_word in moderation_key_words:
                moderated_message = str(moderated_message).replace(key_word, "[REDACTED]")
            embed2 = discord.Embed(title="Auto Moderation", description= str(message.author) + " Please rephrase your sentence and check that it complies with our rules.", color=0xed900c)
            embed2.add_field(name="Message:", value=moderated_message, inline=False)
            await message.channel.send(embed=embed2)
            await message.delete()
