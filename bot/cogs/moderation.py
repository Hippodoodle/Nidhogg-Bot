"""The moderation commands of the discord bot."""
from discord.ext import commands
from unidecode import unidecode
from bot.models import FlaggedWarning, Guild, ModerationLog
from asgiref.sync import sync_to_async
import discord
import datetime
import os
import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODERATION_DIR = os.path.join(BASE_DIR, 'files/moderation_keywords.txt')

FLAGGED_DIR = os.path.join(BASE_DIR, 'files/flagged_keywords.txt')


django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clicker_png.settings')


def list_compare(a, b) -> bool:
    for item in a:
        if item in b:
            return True
    return False


def add_flagged_warning(message_id: int, moderation_log_channel_id: int, message_content: str):
    log = ModerationLog.objects.filter(channel_id=moderation_log_channel_id)[0]
    f = FlaggedWarning.objects.get_or_create(
        message_id=message_id,
        moderation_log_channel_id=log
    )[0]
    f.message_content = message_content
    f.save()
    return f


class Moderation(commands.Cog):
    """ The moderation commands of the bot. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setLog(self, ctx: commands.Context, *args) -> None:
        """
        Set the moderation log channel.\n
        No attributes defaults to looking for a channel with name 'moderation-log'\n
        Syntax:
        - ?setLog
        - ?setLog [channel_id]
        """
        g = await sync_to_async(Guild.objects.get_or_create)(guild_id=int(ctx.guild.id))
        g = g[0]
        g.name = ctx.guild.name
        await sync_to_async(g.save)()

        if args != ():
            channel_id = int(args[0])
        else:
            channel_id = int(discord.utils.get(self.bot.get_all_channels(), guild=ctx.guild, name='moderation-log').id)

        log = await sync_to_async(ModerationLog.objects.get_or_create)(channel_id=channel_id, guild=g)
        log = log[0]
        await sync_to_async(log.save)()

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
                embed_flagged.set_footer(text="Vote 🟩 to keep or 🟥 to remove")
                flagged_warning_message = await log_channel.send("<@&721848925887397890>", embed=embed_flagged)
                await flagged_warning_message.add_reaction("🟩")
                await flagged_warning_message.add_reaction("🟥")
                await sync_to_async(add_flagged_warning)(int(flagged_warning_message.id), int(log_channel.id), message.content)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Do something when a reaction is added to a message"""

        flagged_warning_message_queryset = await sync_to_async(FlaggedWarning.objects.filter)(message_id=int(payload.message_id))

        await sync_to_async(print)(flagged_warning_message_queryset)

        if not await sync_to_async(flagged_warning_message_queryset.exists)():
            print('a')
            return

        flagged_warning_message_id = await sync_to_async(lambda x: x[0].message_id)(flagged_warning_message_queryset)

        moderation_log_channel_id = await sync_to_async(lambda x: x[0].moderation_log_channel_id.channel_id)(flagged_warning_message_queryset)

        print(flagged_warning_message_id, type(flagged_warning_message_id))
        print(moderation_log_channel_id, type(moderation_log_channel_id))

        moderation_channel = discord.Client.get_channel(moderation_log_channel_id)

        # flagged_warning_message = await moderation_channel.fetch_message(int(flagged_warning_message_id))
