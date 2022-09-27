# coding: utf-8
import discord
from discord.ui import View, Button
from discord.ext import commands
from battle.battle_buttons import *
from battle.def_utils_battle import *
from def_utils import user_exist


class CommandantShepard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # mumuse 861613275414528030
        # test 860440689355259906
        channel = self.bot.get_channel(860440689355259906)
        print('Logged in as ---->', self.bot.user)
        # print('ID:', self.bot.user.id)
        print(f"{self.__class__.__name__} --- OK")
        await channel.send(":sunglasses: I'm back bitches")
        # await channel.send("https://tenor.com/tk8a.gif")  # loool

    @commands.command(name="stats", help="Les stats du Fight Club")
    @user_exist()
    async def fight_stats(self, ctx):
        user = db_fight_get_stats_by_user(ctx.author.id)
        await ctx.reply(f"Salut {ctx.author}, \n"
                        f"tu es niveau {user['lvl']} \n"
                        f"ton de rang est {user['rang']},\n"
                        f"avec {user['win']} victoire sur {int(user['win']) + int(user['loose'])} parties !",
                        mention_author=True)

    @commands.command(name="menu", help="Le menu")
    @user_exist()
    async def fight_menu(self, ctx):
        view = FightMenu(ctx)
        await ctx.reply('Quelle action fais-tu ?', view=view, mention_author=True)

    # carte des adversaires
    @commands.command(name="adv", help="Details des adversaires")
    @user_exist()
    async def fight_adv_embed(self, ctx):
        e = embed_advs(ctx)
        files, embeds = e['files'], e['embeds']
        await ctx.send(files=files, embeds=embeds, delete_after=40)

    @commands.command(name="btn",hidden=True)
    @user_exist()
    async def fight_adv_btn(self, ctx):
        # advs = db_fight_get_adversary()

        view = FightAdversary(ctx)
        await ctx.send('Choisi ton adversaire !', view=view)
        await view.wait()
        print(view.value)
        e = embed_adv(ctx, view.value)
        file, embed = e['file'], e['embed']
        await ctx.send(file=file, embed=embed)


async def setup(bot):
    await bot.add_cog(CommandantShepard(bot))
