""" The counting channel specific commands of the discord bot. """
from discord.ext import commands
import re


class Counting(commands.Cog):
    """ The counting channel specific commands of the bot. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def recount(self, ctx: commands.Context, *args):
        """ Recounts counting-channel, skipping first arg[0] numbers.\n
            Syntax:
                - ?recount [start_from | 0] [delete_after | None]
        """

        # Only checks messages in counting-channel
        if ctx.channel.id != 699762298721665158:
            return

        await ctx.message.delete()

        # Initialise variables
        start_from = None
        limited = False
        previous_message = "0 0"
        count = 0
        delete_after = None

        if len(args) > 0:
            start_from = int(args[0])
            limited = True

        if len(args) > 1:
            delete_after = int(args[1])

        # Iterate over list of all messages in counting-channel
        async for m in ctx.channel.history(limit=None, oldest_first=True):

            if limited:
                count += 1
                limited = count < start_from

            if not limited:
                pre = previous_message.replace("(", " ").split(" ")[0].strip()
                pre = re.sub("[^0-9]", "", pre)
                message_content = m.content

                try:
                    if not message_content.startswith(str(int(pre)+1)):
                        print("Bad count:", int(previous_message.split(" ")[0]), int(m.content.split(" ")[0]))
                        await ctx.channel.send(m.jump_url, delete_after=delete_after)
                except ValueError:
                    pass

                previous_message = message_content

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Counting channel check listener. """

        # Ignore messages from the bot
        if message.author == self.bot.user:
            return

        # Only checks messages in counting-channel
        if message.channel.id != 699762298721665158:
            return

        # gets the last 2 messages
        messages = await message.channel.history(limit=2).flatten()

        # Process the older message
        pre = messages[1].content.replace("(", " ").split(" ")[0].strip()
        pre = re.sub("[^0-9]", " ", pre)

        # Process the current message
        message_content = messages[0].content

        # Delete the current message if the number is wrong
        if not message_content.startswith(str(int(pre)+1)):
            await message.channel.send("Check yourself before you wreck yourself.", delete_after=3)
            await message.delete()
