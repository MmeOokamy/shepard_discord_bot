import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print("Ready bot2")


@client.command()
async def cmd2(ctx):
    await ctx.send("Bot2")


client.run(os.getenv("TOKEN"))
