# coding: utf-8
import discord
from discord.ext import commands

from shepard.config import TEST_CHANNEL_ID, PROD_CHANNEL_ID
from shepard.core.checks import is_me
from shepard.core.system import check_service_status


class CommandantShepard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_chan = TEST_CHANNEL_ID
        self.prod_chan = PROD_CHANNEL_ID

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.test_chan)
        print("Logged in as ---->", self.bot.user)
        print(f"{self.__class__.__name__} --- OK")
        await channel.send(":sunglasses: I'm back bitches :sunglasses:")
        # await channel.send("https://tenor.com/tk8a.gif")  # loool

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send("Hey bienvenue !!")

    @commands.command(name="status", help="Voir l'état du serveur.")
    @is_me()
    async def status(self, ctx):
        # aequilibris = check_service_status("aequilibris.service")
        iot = check_service_status("monitoring_app.service")

        response = f"""
        IOT         -> {iot}  <3
        """
        await ctx.reply(response)


async def setup(bot):
    await bot.add_cog(CommandantShepard(bot))
