# coding: utf-8
import random
import discord
import asyncio
from discord.ext import commands
from db import *  # sqlite execute fonction =)
from sentence import brooklyn_99_quotes, botcommand


class BotGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # @commands.command()  # Your command decorator.
    # async def hello(self, ctx):  # ctx is a representation of the
    #     # command. Like await ctx.send("") Sends a message in the channel
    #     # Or like ctx.author.id <- The authors ID
    #     await ctx.send('helloooooo')  # <- Your command code here

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

    # reaction en fonction d'un mot
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #
    #     if message.content.startswith('chupakabra'):
    #         await message.channel.send('donne un num a cette creature!')
    #
    #         def is_correct(m):
    #             return m.author == message.author and m.channel == message.channel
    #
    #         msg = await self.bot.wait_for('message', check=is_correct)
    #         await message.channel.send(f'Hello {msg}!')


async def setup(bot):
    await bot.add_cog(BotGames(bot))
