"""The WIP commands of the discord bot."""
from discord.ext import commands
import random
import discord
import datetime
import re


class WIPCommands(commands.Cog):
    """The WIP commands of the bot."""

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def doodle(self, ctx, *args):
        r = ["You are not alone. You have us.", "Life is challenging. It really is... I don't have many inspirational words for you this time. Just do your best and hopefully that works out.", "Sometimes it's okay to cry.", "Don't start smoking or you'll get nicotine withdrawals if you don't smoke. Then you'll become an asshole.", "Your life makes a difference in this world.", "Be inspired by your idols. Walk your own path.", "No matter how bad things may seem, the pain is only in your head.", "Make the best of all your years, because soon enough the year will be your last.", "Remember to drink water.",
             "You are the source of your own happiness. Explore what brings you joy.", "Don't be afraid to befriend someone out of your social norms or comfort zone.", "You have to take action to change something. You can't stay in silence and expect something to change.", "Stars cannot shine without darkness", "You're amazing. And one day, someone who matters more to you will know it too.", "Go outside in the sun and park. Read or get away from what you are doing! Distract yourself.", "I just want you all to find what makes you happy and stick to it. Don't get sucked into bad vibes okay?", "Proper sleep is necessary for the body to function at it's best"]
        random_thing = random.randint(0, len(r))
        embed = discord.Embed(title=r[random_thing], color=0xFBAED2)
        embed.set_footer(text="Stay hydrated")
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def e(self, ctx, *args):
        await ctx.message.channel.send(":bug:")
        await ctx.message.add_reaction("🐛")
        await ctx.message.channel.send("<:zavalasmile:700287723247763536>")
        await ctx.message.add_reaction("<:zavalasmile:700287723247763536>")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def recount(self, ctx: commands.Context, *args):
        await ctx.message.delete()
        if ctx.channel.id == 699762298721665158: # 794908427809062912
            print("success")
            previous_message = "0 0"
            async for m in ctx.channel.history(limit=6000, oldest_first=True):
                try:
                    pre = previous_message.replace("("," ").split(" ")[0].strip()
                    pre = re.sub("[^0-9]", " ", pre)
                    message_content = m.content
                    #if (int(pre) + 1) != int(cur):
                    if not message_content.startswith(str(int(pre)+1)):
                        print("Bad count:", int(previous_message.split(" ")[0]), int(m.content.split(" ")[0]))
                        await ctx.channel.send(m.jump_url, delete_after=120)
                    previous_message = m.content

                except ValueError as e:
                    pass
                    #print(e, previous_message, m.content)
            print("done")

