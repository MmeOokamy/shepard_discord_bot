# coding: utf-8
import os
import sys
import asyncio

# Rendre le package `shepard` importable (layout src/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import discord
from discord import app_commands
from discord.ext import commands

from shepard.config import PREFIX, TOKEN, GUILD_ID
from shepard.core.database import connect, close
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
            await connect()
            logger.info("Database connection successful")
        except Exception as err:
            logger.error(f"Database connection error: {err}")
            sys.exit(1)
        logger.info("---Load Extensions---")
        await load_extensions()
        logger.info("---Start Bot---")
        try:
            await bot.start(TOKEN)
        except Exception as e:
            logger.error(f"Bot start error: {e}")
        finally:
            await close()


# ------------------------------------------------------------------ #
#  Gestionnaires d'erreurs globaux                                   #
# ------------------------------------------------------------------ #
@bot.event
async def on_command_error(ctx, error):
    """Erreurs des commandes prefix / hybrides (filet de sécurité global)."""
    if isinstance(error, commands.CommandNotFound):
        return
    # laisser les handlers spécifiques (cog ou commande) gérer leurs propres erreurs
    if (ctx.command and ctx.command.has_error_handler()) or (
        ctx.cog and ctx.cog.has_error_handler()
    ):
        return

    error = getattr(error, "original", error)
    if isinstance(error, commands.CheckFailure):
        await ctx.send("⛔ Tu n'as pas le droit d'utiliser cette commande.", delete_after=8)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❓ Argument manquant : `{error.param.name}`.", delete_after=8)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❓ Argument invalide.", delete_after=8)
    else:
        logger.error(f"Erreur dans la commande {ctx.command} : {error}", exc_info=error)


@bot.tree.error
async def on_app_command_error(interaction, error):
    """Erreurs des slash commands pures (filet de sécurité)."""
    if isinstance(error, app_commands.CheckFailure):
        msg = "⛔ Tu n'as pas le droit d'utiliser cette commande."
    else:
        msg = "⛔ Une erreur est survenue."
        logger.error(f"Erreur slash command : {error}", exc_info=error)
    try:
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except discord.HTTPException:
        pass


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
