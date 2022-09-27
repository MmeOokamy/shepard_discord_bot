# coding: utf-8
import os
import sys
import asyncio
import random
import discord
from discord.ext import commands
from battle.Fighter import Fighter
from def_utils import user_exist
from battle.def_utils_battle import special_txt, embed_one, embed_atk, embed_advs, embed_user
from battle.battle_buttons import *


class BotBattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} --- OK")

    # Mini Rpg Fight Game
    @commands.command(name="battle", help="Fight Club")
    @user_exist()
    async def fight_game(self, ctx):
        user = db_fight_get_stats_by_user(ctx.author.id)

        # Fonction utils
        async def status_fighter(player, two):
            await ctx.send(f"{player.name} : {player.pv}")
            await ctx.send(f"{special_txt(player)}")
            await ctx.send(f"{two.name} : {two.pv}")
            await ctx.send(f"{special_txt(two)}")

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

        guess = ''
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
            max_id = 1
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
            elif int(choice_adv.content) in range(1, max_id):
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
            await ctx.reply("C'est parti !", mention_author=True)
            await ctx.send(f"Bienvenue dans l'arène, en ce jour glorieux, deux adversaires s'affrontent !")
            await ctx.send(f"Dans le coin IRL : \n"
                           f":point_left: {player_one.name}, humain de niveau {user['lvl']}, {user['rang']}\n"
                           f"{special_txt(player_one)}")

            await ctx.send(f"Dans le coin Virtuel : \n"
                           f":point_right: {player_two.name}, {adv['race']} du même niveau.\n"
                           f"{special_txt(player_two)}")
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
                    db_fight_win(ctx.author.id, 3)
                elif not player_two.alive:
                    await ctx.send(f"{player_one.name} gagne contre {player_two.name} :muscle:!")
                    db_fight_loose(ctx.author.id)

    # Mini Rpg Fight Game
    @commands.command(name="battest", help="Fight Club Develop")
    @user_exist()
    async def fight_game_test(self, ctx):
        user = db_fight_get_stats_by_user(ctx.author.id)

        # Fonction utils
        async def status_fighter(player, two):
            await ctx.send(f"{player.name} : {player.pv}")
            await ctx.send(f"{special_txt(player)}")
            await ctx.send(f"{two.name} : {two.pv}")
            await ctx.send(f"{special_txt(two)}")

        step = 1  # round

        async def battle(player, two):
            atk_one_a = ''
            atk_one_b = ''
            atk_two_a = ''
            atk_two_b = ''
            atk_result = ''

            # player_one attaque ou rate
            if player.touch_or_esquive(two):
                if player.is_critical():
                    damage_crit = player.critical_attack()
                    two.reduction_of_pv(damage_crit)
                    atk_one_a = f"{player.name} fait un critique"
                    atk_one_b = f"{two.name} prend {damage_crit} de dégâts"
                else:
                    damage = player.attack()
                    two.reduction_of_pv(damage)
                    atk_one_a = f"{player.name} attaque"
                    atk_one_b = f"{two.name} prend {damage} de dégâts"
            else:
                atk_one_a = f"{player.name} attaque"
                atk_one_b = f"{two.name} esquive =p !"
            # await ctx.send(f"{atk_one_a}, {atk_one_b}")

            # Check adv mort ou en vie
            if two.alive is False:
                atk_two_a = f"{two.name} n'a plus de pv."
                atk_two_b = '☠'
            else:
                # player_two attaque ou rate
                if two.touch_or_esquive(player):
                    adv_damage = two.attack()
                    player.reduction_of_pv(adv_damage)
                    # await ctx.send(f"{two.name} riposte, {player.name} perd {adv_damage} de pv")
                    atk_two_a = f"{two.name} riposte"
                    atk_two_b = f"{player.name} perd {adv_damage} de pv"
                else:
                    # await ctx.send(f"{two.name} attaque mais {player.name} réussi a esquiver !")
                    atk_two_a = f"{two.name} attaque"
                    atk_two_b = f"{player.name} réussi a esquiver !"
                # await ctx.send(f"{ atk_two_a}, {atk_two_b}")

            if player.alive is False:
                # await ctx.send(f"{player.name} n'a plus de pv.")
                atk_result = f"{player.name} n'a plus de pv. ☠"
            else:
                atk_result = f"{player.name} : {player.pv} pv, {two.name} : {two.pv} pv"

            # await ctx.send(atk_result)
            await ctx.send(embed=embed_atk(step, atk_one_a, atk_one_b, atk_two_a, atk_two_b, atk_result))

        async def healer(player):
            pv_potion = player.take_care_of_yourself()
            embed = discord.Embed(title="Utilise Soin", color=discord.Colour.random())
            file = discord.File(f"/home/ookamy/Dev/shepard_discord_bot/battle/img/potion.png", filename="potion.png")
            embed.set_author(name=player.name, icon_url="attachment://potion.png")
            embed.add_field(name="Plonge la main dans sa poche et en sort une petite fiole....",
                            value=f"Et hop! Dans le gosier !\n La potion de vitalité lui donne {pv_potion} de pv en plus")
            embed.set_footer(text=f"{player.name} a maintenant {player.pv} pv ...")
            await ctx.send(file=file, embed=embed)

        # propose le combat
        view_fs = FightStart(ctx)
        await ctx.send('Un petit combat ??', view=view_fs, delete_after=20, mention_author=True)
        await view_fs.wait()

        if view_fs.value is True:
            # selection de l'adversaire
            e = embed_advs(ctx)
            files, embeds = e['files'], e['embeds']
            await ctx.send(files=files, embeds=embeds, delete_after=10)
            view = FightAdversary(ctx)
            await ctx.send('Choisi ton adversaire !', view=view)
            await view.wait()
            # print(view.value)
            adv_id = int(view.value)

            await ctx.send(f"**Bienvenue dans l'arène, en ce jour glorieux, deux adversaires s'affrontent !**")
            # Player_one : user
            po = db_fight_get_user_special_for_create_fighter(ctx.author.id)
            # print(po)
            player_one = Fighter(po['name'], po['strength'], po['perception'], po['endurance'], po['charisma'],
                                 po['intelligence'], po['agility'], po['luck'])
            # print(player_one)

            # Player_two : adversaire
            if adv_id == 0:
                adv_id = random.randint(1, 4)
            e = embed_adv(ctx, adv_id)
            file, embed = e['file'], e['embed']
            adv = db_fight_get_adversary_by_id_for_create(adv_id, ctx.author.id)
            # {'name': 'Grunt', 'lvl': 1, 'strength': 4, 'perception': 1, 'endurance': 4, 'charisma': 1,
            # 'intelligence': 0, 'agility': 1, 'luck': 1, 'race': 'Krogan', 'pts': 3}
            pts = int(adv['pts'])
            player_two = Fighter(adv['name'], adv['strength'], adv['perception'], adv['endurance'], adv['charisma'],
                                 adv['intelligence'], adv['agility'], adv['luck'])

            # Embed des combattants
            await ctx.send(f"Dans le coin IRL : \n", embed=embed_user(ctx))
            await ctx.send(f"Dans le coin Virtuel : \n", file=file, embed=embed)
            await ctx.send("**🥊 !! 🥊 FIGHT 🥊 !! 🥊**")

            # first round
            await battle(player_one, player_two)
            step += 1

            while player_one.alive and player_two.alive:
                choice = ''
                view_fc = FightChoices(ctx)
                await ctx.reply('Quelle action fais-tu ?', view=view_fc,  mention_author=True)
                await view_fc.wait()
                choice = view_fc.value
                # choix au combat
                if int(choice) == 1:
                    await battle(player_one, player_two)
                    step += 1
                elif int(choice) == 2:
                    if player_one.heal != 0:
                        await healer(player_one)
                    else:
                        await ctx.send("Tu n'as plus de potion !")
                elif int(choice) == 3:
                    await status_fighter(player_one, player_two)
            else:
                # Player one mort
                if not player_one.alive:
                    db_fight_loose(ctx.author.id)
                    await ctx.send(f"{player_two.name} est le grand gagnant :muscle:!")
                # Player one win
                elif not player_two.alive:
                    db_fight_win(ctx.author.id, pts)
                    await ctx.send(f"{player_one.name} gagne contre {player_two.name} :muscle:!")

    @commands.command(name="win", help="dev")
    @user_exist()
    async def fight_win_test(self, ctx):
        # quand gagne +xp +win chek l'xp si =< palier alors attribution des pts
        pts = 5
        # db_fight_win(ctx.author.id, pts)
        po = db_fight_get_special_total(ctx.author.id, adv_id=0)
        sh = db_fight_get_special_total(ctx.author.id, adv_id=4)
        await ctx.send(f"{po}")
        await ctx.send(f"{sh}")


async def setup(bot):
    await bot.add_cog(BotBattle(bot))
