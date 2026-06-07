# coding: utf-8
import os
import sys
import asyncio

# Rendre le package `shepard` importable (layout src/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import discord
from discord.ext import commands

from shepard.config import PREFIX, TOKEN, GUILD_ID
from shepard.core.database import db_connect
from shepard.core.checks import is_me
from shepard.core.logging_setup import setup_logging

logger = setup_logging()

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

COGS = [
    "shepard.cogs.shepard",
    "shepard.cogs.battle",
    "shepard.cogs.commands",
    "shepard.cogs.games",
    "shepard.cogs.help",
    "shepard.cogs.moderation",
]


async def load_extensions():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logger.info(f"{cog} has loaded.")
        except Exception as e:
            logger.error(f"Failed to load {cog}: {e}")


@bot.event
async def setup_hook():
    """Synchronise les slash commands (appelé automatiquement au démarrage)."""
    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info(f"{len(synced)} slash commands synchronisées sur la guild {GUILD_ID}")
        else:
            synced = await bot.tree.sync()
            logger.info(
                f"{len(synced)} slash commands synchronisées globalement "
                f"(propagation jusqu'à ~1h)"
            )
    except Exception as e:
        logger.error(f"Échec de la synchro des slash commands : {e}")


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
        try:
            await bot.start(TOKEN)
        except Exception as e:
            logger.error(f"Bot start error: {e}")


@bot.command(name="fait_dodo", hidden=True)
@is_me()
async def kill_proc(ctx):
    await ctx.send("Bonne nuit!")
    await bot.close()


@bot.command(name="reload", hidden=True)
@is_me()
async def reload_proc(ctx):
    await ctx.send("Ok je recharge !")
    os.system("python main.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by keyboard interrupt")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
