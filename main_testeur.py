import os
import sys
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from db import *  # sqlite execute fonction =)
import datetime
from sentence import botcommand

load_dotenv()

intents = discord.Intents.default()

intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


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


@bot.command(name='help_createquote')
async def add_quote(ctx):
    await ctx.reply("Créer une quote, easy!", mention_author=True)
    await ctx.reply('C\'est simple:   $createquote "le texte que tu veux enregistrer" "nom de la personne",'
                    'ne pas oublier les "" ', mention_author=True)
    await ctx.reply(
        '$createquote "Appelle moi encore une fois ma princesse et tu vas devoir ramasser tes dents avec tes doigts cassés!'
        'cassés" "Commandant Shepard ME1 <3 "', mention_author=True)
    await ctx.reply('Tu auras un petit message si c\'est bon, pour les voir toutes $listeQ .', mention_author=True)


@bot.command(name='createquote')
async def add_quote(ctx, quote, username):
    db_create_quote(username, quote)
    await ctx.send(f'Quote ajouté !')


@bot.command(name='listeQ')
async def liste_quote(ctx):
    quotes = db_get_quote()
    if quotes:
        for q in quotes:
            await ctx.send(f" \"{q['quote']}\", {q['user_name']}")
    else:
        await ctx.send("C'est vide")


@bot.command(name='randomQ')
async def liste_quote(ctx):
    q = []
    quotes = db_get_quote()
    if quotes:
        for item in quotes:
            q.append(f" \"{item['quote']}\", {item['user_name']}")
        quote = random.choice(q)
    else:
        quote = "C'est vide"

    await ctx.send(quote)


@bot.event
async def on_message(message):
    if "bot testeur" in message.content.lower():
        await message.reply(content=f"@{message.author.display_name}, {random.choice(botcommand)}", mention_author=True)


bot.run(os.getenv("TESTEURBOT"))
