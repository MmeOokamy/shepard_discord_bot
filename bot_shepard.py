# coding: utf-8
from unicodedata import name
import discord
from discord.ui import View, Button
from discord.ext import commands
from battle.battle_buttons import *
from battle.def_utils_battle import *
from def_utils import user_exist


class CommandantShepard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_chan = 1031895034439675986
        self.prod_chan = 861613275414528030

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.test_chan)
        print("Logged in as ---->", self.bot.user)
        print(f"{self.__class__.__name__} --- OK")
        await channel.send(":sunglasses: I'm back bitches")
        # await channel.send("https://tenor.com/tk8a.gif")  # loool

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send("Hey bienvenue !!")


async def setup(bot):
    await bot.add_cog(CommandantShepard(bot))
