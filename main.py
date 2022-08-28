import os
import sys
import asyncio
import random

import discord
from discord.ext import commands

from db import *  # sqlite execute fonction =)

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

cog_files = ['bot_shepard', 'bot_command', 'bot_games']

async def load_extensions():
    for cog_file in cog_files:  # Cycle through the files in array
        await bot.load_extension(cog_file)  # Load the file
        print("%s has loaded." % cog_file)  # Print a success message.


async def main():
    async with bot:
        print('---Load Extensions---')
        await load_extensions()
        print('---Load DB---')
        try:
            db_connect()
            print('Database OK')
        except OSError as err:
            print("OS error: {0}".format(err))
            print("Unexpected error:", sys.exc_info()[0])
        print('---Start Bot---')
        await bot.start(os.getenv("TESTEURBOT"))
        

asyncio.run(main())