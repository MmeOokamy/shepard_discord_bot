import os
import sys
import asyncio
import random

import logging
from logging.handlers import RotatingFileHandler
from settings_logs import setup_logging

import discord
from discord.ext import commands

from db import *  # sqlite execute fonction =)
from def_utils import is_me  # fonction utile partout

from dotenv import load_dotenv

# Initialiser le logger
logger = setup_logging()

load_dotenv()
PREFIX = os.getenv("PREFIX")
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

cog_files = ["bot_shepard", "bot_battle", "bot_command", "bot_games", "bot_help"]


async def load_extensions():
    for cog_file in cog_files:  # Cycle through the files in array
        try:
            await bot.load_extension(cog_file)
            logger.info(f"{cog_file} has loaded.")
        except Exception as e:
            logger.error(f"Failed to load {cog_file}: {e}")

async def main():
    logger.info("---Starting Bot Initialization---")
    async with bot:
        logger.info("---Load/Init DB---")
        try:
            db_connect()
            logger.info("Database connection successful")
        except OSError as err:
            logger.error(f"Database connection error: {err}")
            logger.error(f"Unexpected error: {sys.exc_info()[0]}")
            sys.exit(1)
        logger.info("---Load Extensions---")
        await load_extensions()
        logger.info("---Start Bot---")
        # TESTEURBOT  -  TOKEN
        try:
            await bot.start(os.getenv("TOKEN"))
        except Exception as e:
            logger.error(f"Bot start error: {e}")


@bot.command(name="fait_dodo", hidden=True)
@is_me()
async def kill_proc(ctx):
    await ctx.send(f"Bonne nuit!")
    await bot.close()  # don't forget this!


@bot.command(name="reload", hidden=True)
@is_me()
async def reload_proc(ctx):
    await ctx.send(f"Ok je recharge !")
    os.system("python main.py")  # don't forget this!


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
    # asyncio.run(main())
