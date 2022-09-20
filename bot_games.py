# coding: utf-8
import random
import discord
import asyncio
from discord.ext import commands
from db import *  # sqlite execute fonction =)
from sentence import *
from def_utils import *
from Buttons import *


class BotGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} --- OK")

    @commands.command(name='btn', help="btn")
    async def btn_test(self, ctx: commands.Context):
        view = Confirm()
        await ctx.send('Veut-tu continer?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()

        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Confirmed...')
        else:
            print('Cancelled...')

        print(view.value)

    @commands.command(name='nb_magic', help="Devine le nombre secret !")
    async def game_number(self, ctx):
        guess = ''
        # choisit l'écart et la réponse
        nb_min = random.randint(1, 9)
        nb_max = random.randint(10, 20)
        answer = random.randint(nb_min, nb_max)

        await ctx.reply(f"Devine le nombre magique.\n Je pense a une numéro entre {nb_min} et {nb_max}. \n"
                        f"Tu as 10 secondes", mention_author=True)

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.reply('Dommage tu as mis du temps a répondre :worried:', mention_author=True)

        if int(guess.content) == answer:
            await ctx.reply('GG!')
        else:
            await ctx.reply(f"Oops, PERDU! c'était : {answer}", mention_author=True)


async def setup(bot):
    await bot.add_cog(BotGames(bot))
