import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from db import *  # sqlite execute fonction =)
import datetime

load_dotenv()

intents = discord.Intents.default()

intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
db_connect()


@bot.command()
async def joined(ctx):
    await ctx.send(f'ready too used')


@bot.command(name='help_createquote')
async def add_quote(ctx):
    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    await ctx.reply("Créer une quote, easy!", mention_author=True)
    await ctx.reply('C\'est simple:   $createquote "le texte que tu veux enregistrer" "nom de la personne",'
                    'ne pas oublier les "" ', mention_author=True)
    await ctx.reply('$createquote "Appelle moi encore une fois ma princesse et tu vas devoir ramasser tes dents avec tes doigts cassés!'
                    'cassés" "Commandant Shepard ME1 <3 "', mention_author=True)
    await ctx.reply('Tu auras un petit message si c\'est bon, pour les voir toutes $listeQ .', mention_author=True)


@bot.command(name='createquote')
async def add_quote(ctx, quote, username):
    db_create_quote(username, quote)
    await ctx.send(f'Quote ajouté !')


@bot.command(name='listeQ')
async def liste_quote(ctx):
    quotes = db_get_quote()
    for q in quotes:
        await ctx.send(f" \"{q['quote']}\", {q['user_name']}")


@bot.command(name='randomQ')
async def liste_quote(ctx):
    q = []
    quotes = db_get_quote()
    for item in quotes:
        q.append(f" \"{item['quote']}\", {item['user_name']}")
    quote = random.choice(q)
    await ctx.send(quote)


bot.run(os.getenv("TESTEURBOT"))
