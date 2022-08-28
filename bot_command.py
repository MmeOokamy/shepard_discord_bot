# coding: utf-8
import random
import discord
from discord.ext import commands
from db import *  # sqlite execute fonction =)
from sentence import brooklyn_99_quotes, botcommand


class BotCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def is_me():
        def predicate(ctx):
            return ctx.message.author.id == 283935710858313730
        return commands.check(predicate)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.command(name='fait_dodo')
    @is_me()
    async def kill_proc(self, ctx):
        await ctx.send(f'Bonne nuit!')
        await self.bot.close()  # don't forget this!
        
    
    
    @commands.command(name='ctx__')
    async def ctx_detail(self, ctx):
        await ctx.send(f'{ctx}')
        await ctx.send(f'{ctx.author.id}')
        
        await ctx.send(f'{ctx.prefix}')
        await ctx.send(f'{ctx.guild}')
        await ctx.send(f'{ctx.me}')
        await ctx.send(f'{ctx.permissions}')
            
    # @commands.command()  # Your command decorator.
    # async def hello(self, ctx):  # ctx is a representation of the
    #     # command. Like await ctx.send("") Sends a message in the channel
    #     # Or like ctx.author.id <- The authors ID
    #     await ctx.send('helloooooo')  # <- Your command code here
        
        
    @commands.command(name='help_quote')
    async def help_quote(self, ctx):
        await ctx.reply('Créer une quote, easy! \n'
                        'C\'est simple:  \n!qadd "le texte que tu veux enregistrer" "nom de la personne", ne pas oublier les "" \n' 
                        '!qadd "Appelle moi encore une fois ma princesse et tu vas devoir ramasser tes dents avec tes doigts cassés!" "Commandant Shepard ME1 <3 "\n'
                        'Tu auras un petit message si c\'est bon, pour les voir toutes !lq .', mention_author=True)
                        
    
        
        
    @commands.command(name='qadd')
    async def add_quote(self, ctx, quote, username):
        db_create_quote(username, quote)
        await ctx.send(f'Quote ajouté !')

    @commands.command(name='qall')
    async def all_quote(self, ctx):
        quotes = db_get_quote()
        if quotes:
            for q in quotes:
                await ctx.send(f" \"{q['quote']}\", {q['user_name']}")
        else:
            await ctx.send("C'est vide")

        
    @commands.command(name='qr')
    async def random_quote(self, ctx):
        q = []
        quotes = db_get_quote()
        if quotes:
            for item in quotes:
                q.append(f" \"{item['quote']}\", {item['user_name']}")
            quote = random.choice(q)
        else:
            quote = "C'est vide"
        await ctx.send(quote)

    
    # reaction en fonction d'un mot
    @commands.Cog.listener()
    async def on_message(self, message):
        if "botbot" in message.content.lower():
            await message.reply(content=f"@{message.author.display_name}, :o ", mention_author=True)
            
        elif "superbot" in message.content.lower():
            await message.reply(content=f"@{message.author.display_name}, {random.choice(botcommand)}", mention_author=True)
            
        elif "99" in message.content.lower():
            await message.reply(content=f"{random.choice(brooklyn_99_quotes)}",
                            mention_author=True)



async def setup(bot):
    await bot.add_cog(BotCommand(bot))
