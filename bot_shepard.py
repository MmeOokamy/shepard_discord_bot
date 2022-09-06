# coding: utf-8
import os
import sys
import asyncio
import random
import discord
from discord.ext import commands
from db import *  # sqlite execute fonction =)
from sentence import shepard
from Fighter import Fighter
from def_utils import db_create_user_if_exist


class CommandantShepard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # mumuse 861613275414528030
        # test 860440689355259906
        channel = self.bot.get_channel(860440689355259906)
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        print('------')
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        await channel.send(":sunglasses: I'm back bitches")
        # await channel.send("https://tenor.com/tk8a.gif")  # loool

    @commands.Cog.listener()
    async def on_message(self, message):
        # if "shepard" in message.content.lower():
        #     await message.reply(content=f"@{message.author.display_name}, {random.choice(shepard)}",
        #                         mention_author=True)

        if "leilou dallas, multipass" in message.content.lower():
            await message.reply(content="oui elle sait ce que c’est qu’un multipass.", mention_author=True)

    @commands.command(name="stats", help="Les stats du Fight Club")
    async def fight_stats(self, ctx):
        user = db_fight_get_stats_by_user(ctx.author.id)
        await ctx.reply(f"Salut {ctx.author}, \n"
                        f"tu es niveau {user['lvl']} \n"
                        f"ton de rang est {user['rang']},\n"
                        f"avec {user['win']} victoire sur {int(user['win']) + int(user['loose'])} parties !",
                        mention_author=True)

    # @commands.command(name="rules", help="Les différentes regles du combat")
    # async def fight_rules(self, ctx):
    #     # comment cela fonctionne

    # Mini Rpg Fight Game
    @commands.command(name="fight", help="Fight Club")
    async def fight_game(self, ctx):
        # Fonction utils
        async def status_fighter(player, two):
            await ctx.send(f"{player.name} : {player.pv}")
            await ctx.send(f"{player.special()}")
            await ctx.send(f"{two.name} : {two.pv}")
            await ctx.send(f"{two.special()}")

        async def battle(player, two):
            # player_one attaque ou rate
            if player.touch_or_esquive(two):
                if player.is_critical():
                    damage_crit = player.critical_attack()
                    two.reduction_of_pv(damage_crit)
                    await ctx.send(f"{player.name} fait un critique, {two.name} prend {damage_crit} "
                                   f"de dégâts")
                else:
                    damage = player.attack()
                    two.reduction_of_pv(damage)
                    await ctx.send(f"{player.name} attaque, {two.name} prend {damage} de dégâts")
            else:
                await ctx.send(f"{player.name} attaque mais {two.name} esquive =p !")

            # Check adv mort ou en vie
            if two.alive is False:
                await ctx.send(f"{two.name} n'a plus de pv.")
            else:
                # player_two attaque ou rate
                if two.touch_or_esquive(player):
                    adv_damage = two.attack()
                    player.reduction_of_pv(adv_damage)
                    await ctx.send(f"{two.name} riposte, {player.name} perd {adv_damage} de pv")
                else:
                    await ctx.send(f"{two.name} attaque mais {player.name} réussi a esquiver !")

            if player.alive is False:
                await ctx.send(f"{player.name} n'a plus de pv.")

            await ctx.send(f"{player.name} : {player.pv} pv, {two.name} : {two.pv} pv")

        async def healer(player):
            await ctx.send(
                f"{player.name} plonge la main dans sa poche et en sort une petite fiole....")
            await ctx.send(f"Et hop! Dans le gosier !")
            pv_potion = player.take_care_of_yourself()
            await ctx.send(f"La potion de vitalité lui donne {pv_potion} de pv en plus")
            await ctx.send(f"{player.name} a maintenant {player.pv} pv ...")

        # verif existence user + false create data
        guess = ''
        await db_create_user_if_exist(ctx.author.id, ctx.author.name)
        # propose le combat
        await ctx.reply('Un petit combat ? \n 1-Oui ou 2-Non ?', mention_author=True)

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.reply("Dommage tu es lent :worried:, j'me casse!", mention_author=True)

        if int(guess.content) == 2:
            await ctx.reply("No problèmo !", mention_author=True)

        elif int(guess.content) == 1:
            # selection de l'adv
            adv_list = db_fight_get_adversary()
            adv_all = ""
            max_id = 0
            choice_adv = ''
            r_adv = 0
            for adv in adv_list:
                max_id += 1
                adv_all += f"{adv['id']} : {adv['adv_name']} ({adv['adv_race']}) \n"

            await ctx.reply(f"Super! Tu peux choisir ton adversaire dans cette liste : \n"
                            f"0 : Aléatoire \n"
                            f" {adv_all}"
                            , mention_author=True)

            # en fonction de la reponse on verifi que l'adv est entre 0 - id_max
            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= max_id

            try:
                choice_adv = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.reply("Dommage tu es lent :worried:, j'me casse!", mention_author=True)

            # creation de l'adv en fonction du choix
            if int(choice_adv.content) == 0:
                r_adv = random.randint(1, max_id)
            elif int(choice_adv.content) in range(1, max_id, 1):
                r_adv = int(choice_adv.content)

            # Player_two : adversaire
            adv = db_fight_get_adversary_by_id_for_create(r_adv, ctx.author.id)
            xp_win = adv['xp_win']
            player_two = Fighter(adv['name'], adv['strength'], adv['perception'], adv['endurance'], adv['charisma'],
                                 adv['intelligence'], adv['agility'], adv['luck'])

            # Player_one : user
            po = db_fight_get_user_special_for_create_fighter(ctx.author.id)
            player_one = Fighter(po['name'], po['strength'], po['perception'], po['endurance'], po['charisma'],
                                 po['intelligence'], po['agility'], po['luck'])

            await ctx.send(f"HELLLOOO, Bienvenue pour le combat entre deux poids lourd :imp: \n"
                           f"Dans le coin rouge: :point_left:{player_one.name} avec {player_two.pv} PV,"
                           f" {player_one.heal} Potions de soin et une force estimé a {player_one.strength} :muscle: !")

            await ctx.send(f"Dans le coin bleu: :point_right:{player_two.name} avec {player_two.pv} PV,"
                           f" pas besoin de potion pour un {adv['race']}, la force de ce guerrier est de "
                           f"{player_two.strength} :muscle: !")
            await ctx.send("🥊 !! 🥊 FIGHT 🥊 !! 🥊")

            # first round
            await battle(player_one, player_two)

            while player_one.alive and player_two.alive:
                decision = ""
                if player_one.heal == 0:
                    await ctx.reply("1<- Attaquer ||  3 <- Etat PV", mention_author=True)
                else:
                    await ctx.reply(f"1<- Attaquer |-| 2<- Potion de Soin reste : {player_one.heal} |-| 3 <- "
                                    f"Etat PV", mention_author=True)

                def is_correct(m):
                    return m.author == ctx.author and m.content.isdigit()

                try:
                    decision = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.reply("Dommage tu es lent :worried:, j'me casse!", mention_author=True)

                # choix au combat
                if int(decision.content) == 1:
                    await battle(player_one, player_two)
                elif int(decision.content) == 2:
                    if player_one.heal != 0:
                        await healer(player_one)
                    else:
                        await ctx.send("Tu n'as plus de potion !")
                elif int(decision.content) == 3:
                    await status_fighter(player_one, player_two)
                elif int(decision.content) == 4:
                    await ctx.send(f"Si tu gagne cette partie tu aura {xp_win} pts d'xp")

            else:
                if not player_one.alive:
                    await ctx.send(f"{player_two.name} est le grand gagnant :muscle:!")
                    db_fight_add_score(ctx.author.id, 0, xp_win)
                elif not player_two.alive:
                    await ctx.send(f"{player_one.name} gagne contre {player_two.name} :muscle:!")
                    db_fight_add_score(ctx.author.id, 1)


async def setup(bot):
    await bot.add_cog(CommandantShepard(bot))
