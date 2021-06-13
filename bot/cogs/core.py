"""The core of the discord bot."""
from discord.ext import commands
import discord
import datetime
import os


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
    async def welcome(self, ctx: commands.Context, *args) -> None:
        embed = discord.Embed(
            title="Welcome to Nidhogg!",
            colour=discord.Colour(0x77c8f3),
            description="Please read the [rules](https://discord.com/channels/699762297450791025/699762297819758741/711956443921907792)\n\n\n**Here is an invite to the server:**\nhttps://discord.gg/MqhsMKz\n\n\nCheck out these channels too:"
        )

        embed.set_image(url="https://i.imgur.com/Kr2cFzz.png")
        embed.set_footer(text="Brought to you by Hedgehogs")

        embed.add_field(name="#general", value="for general chat", inline=True)
        embed.add_field(name="#lfg-roles", value="for getting lfg roles", inline=True)
        embed.add_field(name="#emotion-pub/cafe", value="for a place to discuss anything on your mind\n\n\n**Have fun and be kind!**", inline=False)

        await ctx.channel.send(embed=embed)
