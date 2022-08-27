import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from sentence_response import SentenceResponse

from db import *  # sqlite execute fonction =)

load_dotenv()

intents = discord.Intents.default()

intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Put all of your cog files in here like 'moderation_commands'
# If you have a folder called 'commands' for example you could do #'commands.moderation_commands'
cog_files = ['sentence_response']


async def load_extensions():
    for cog_file in cog_files:  # Cycle through the files in array
        await bot.load_extension(cog_file)  # Load the file
        print("%s has loaded." % cog_file)  # Print a success message.


@bot.event
async def on_ready():
    print('------')
    try:
        db_connect()
        print('Database OK')
    except OSError as err:
        print("OS error: {0}".format(err))
        print("Unexpected error:", sys.exc_info()[0])
    print('------')


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TESTEURBOT"))


asyncio.run(main())
