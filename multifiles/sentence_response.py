import discord
from discord.ext import commands
from db import *  # sqlite execute fonction =)


class SentenceResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # Your command decorator.
    async def hello(self, ctx):  # ctx is a representation of the
        # command. Like await ctx.send("") Sends a message in the channel
        # Or like ctx.author.id <- The authors ID
        await ctx.send('helloooooo')  # <- Your command code here

    @commands.command(name='lq')
    async def liste_quote(self, ctx):
        quotes = db_get_quote()
        if quotes:
            for q in quotes:
                await ctx.send(f" \"{q['quote']}\", {q['user_name']}")
        else:
            await ctx.send("C'est vide")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "fuck" in message.content.lower():
            await message.reply(content=f"@{message.author.display_name}, :o ", mention_author=True)


async def setup(bot):
    await bot.add_cog(SentenceResponse(bot))
