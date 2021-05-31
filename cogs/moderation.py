"""The moderation commands of the discord bot."""
from discord.ext import commands
from unidecode import unidecode
import discord
import datetime
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODERATION_DIR = os.path.join(BASE_DIR, 'files/moderation_keywords.txt')

FLAGGED_DIR = os.path.join(BASE_DIR, 'files/flagged_keywords.txt')


def list_compare(a, b):
    for item in a:
        if item in b:
            return True
    return False


class Moderation(commands.Cog):
    """ The moderation commands of the bot. """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Do things when a message is sent. """

        # Ignore messages from the bot.
        if message.author == self.bot.user:
            return

        # Open moderation keyword file
        try:
            f = open(MODERATION_DIR, "rt")
        except FileNotFoundError as e:
            print(e)
        moderation_key_words = f.read()

        # Open flagged keyword file
        try:
            f = open(FLAGGED_DIR, "rt")
        except FileNotFoundError as e:
            print(e)
        flagged_key_words = f.read()

        # Process keywords into a list
        moderation_key_words = moderation_key_words.split("\n")
        flagged_key_words = flagged_key_words.split("\n")

        # Get the moderation log channel
        log_channel = discord.utils.get(self.bot.get_all_channels(), guild=message.guild, name='moderation-log')

        # Process message words
        the_message = str(message.content).lower().replace(" ", "")
        the_message = unidecode(the_message)

        # Compare words in each list
        to_be_modded = list_compare(moderation_key_words, the_message)
        to_be_flagged = list_compare(flagged_key_words, the_message)

        """ Silence individual users

        if message.author.id == 453226854518751242:
            to_be_modded = True

        """

        if to_be_modded:

            # Moderation log message handling
            if log_channel is not None:
                embed_mod_log = discord.Embed(
                    title="Auto Moderation Used",
                    timestamp=datetime.datetime.utcnow(),
                    color=0xed900c
                )
                embed_mod_log.add_field(name="User:", value=message.author, inline=True)
                embed_mod_log.add_field(name="User id:", value=message.author.id, inline=True)
                embed_mod_log.add_field(name="Nickname:", value=message.author.nick, inline=True)
                embed_mod_log.add_field(name="Channel:", value=message.channel, inline=True)
                embed_mod_log.add_field(name="Message:", value=message.content, inline=True)
                await log_channel.send(embed=embed_mod_log)

            # Moderated message handling
            moderated_message = str(message.content).lower()
            moderated_message = unidecode(moderated_message)
            for key_word in moderation_key_words:
                moderated_message = str(moderated_message).replace(key_word, "[REDACTED]")
            embed_mod = discord.Embed(
                title="Auto Moderation",
                description=str(message.author) + " Please rephrase your sentence and check that it complies with our rules.",
                color=0xed900c
            )
            embed_mod.add_field(name="Message:", value=moderated_message, inline=False)
            await message.channel.send(embed=embed_mod)
            await message.delete()

        elif to_be_flagged:

            # Moderation log message handling
            if log_channel is not None:
                embed_flagged = discord.Embed(
                    title="Potential Problematic Word Flagged",
                    timestamp=datetime.datetime.utcnow(),
                    color=0xed900c
                )
                embed_flagged.add_field(name="User:", value=message.author, inline=True)
                embed_flagged.add_field(name="User id:", value=message.author.id, inline=True)
                embed_flagged.add_field(name="Nickname:", value=message.author.nick, inline=True)
                embed_flagged.add_field(name="Channel:", value=message.channel, inline=True)
                embed_flagged.add_field(name="Message:", value=message.content, inline=True)
                await log_channel.send("<@&721848925887397890>", embed=embed_flagged)
