# coding: utf-8
from unicodedata import name
import discord
from discord.ui import View, Button
from discord.ext import commands
from battle.battle_buttons import *
from battle.def_utils_battle import *
from def_utils import user_exist


class HelpBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} --- OK")

    @commands.command(name="help", Hidden=True)
    @user_exist()
    async def help_commands(self, ctx):
        embed = discord.Embed(
            title="__Besoin d'aide ?!__",
            description="*Pensez bien a préfixer les commandes pas un ! ( pas deux)*",
            color=discord.Colour.random(),
        )
        file = discord.File(f"asset/img/help.png", filename="help.png")
        embed.set_thumbnail(url="attachment://help.png")

        embed.add_field(
            name="> *Jeux*",
            value=f"**!battle** : fight club =) \n"
            f"**!nb_magic** : Devine le nombre mystérieux \n",
            inline=False,
        )
        embed.add_field(
            name=f"> *Quotes Quotes*",
            value=f"**!qhelp** : tuto pour la création de quote \n"
            f"**!qall** : affiche toute les quotes \n"
            f"**!qr** : retourne une quote aléatoirement \n"
            f'**!qadd "message de la quote" "auteur"**: pour ajouter une quote \n',
            inline=False,
        )

        embed.add_field(
            name="> Players",
            value="**!podium** : Le top 3 \n"
            "**!player_stat** @nom : stats du membre, si pas de nom renseigné c'est le tien qui "
            "s'affiche. \n ",
            inline=False,
        )
        # embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
        # embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
        # embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
        # embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
        # embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
        # embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
        # embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
        # les autre
        # embed.set_footer(text=f"")

        await ctx.send(file=file, embed=embed)


async def setup(bot):
    await bot.add_cog(HelpBot(bot))
