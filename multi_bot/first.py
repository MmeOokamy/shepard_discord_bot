import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print('------')
    print('Ready first')
    print('------')


@bot.command()
async def cmd1(ctx):
    await ctx.send("Bot1")


bot.run(os.getenv("TESTEURBOT"))
