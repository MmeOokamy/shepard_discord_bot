import asyncio

import discord
from discord.ext import commands

from db import *  # sqlite execute fonction =)
from Fighter import create_fighter


async def db_create_user_if_exist(message):
    response = db_create_user(message.author.id, message.author)
    print(response)


class FightCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.command(name="kick")  # Your command decorator.
async def my_kick_command(self, ctx):  # ctx is a representation of the
    # command. Like await ctx.send("") Sends a message in the channel
    # Or like ctx.author.id <- The authors ID
    print(f'{self.id} kick')
    await ctx.send("ctx")


# Mini Rpg Fight Game
@commands.command(name="really")
async def fight_game(ctx):
    async def status_fighter(player, adv):
        await ctx.send(f"{player.name} : {player.pv}")
        await ctx.send(f"{player.special()}")
        await ctx.send(f"{adv.name} : {adv.pv}")
        await ctx.send(f"{adv.special()}")

    async def battle(player, adv):
        # player_one attaque ou rate
        if player.touch_or_esquive(adv):
            if player.is_critical():
                damage_crit = player.critical_attack()
                adv.reduction_of_pv(damage_crit)
                await ctx.send(f"{player.name} fait un critique, {adv.name} prend {damage_crit} "
                               f"de dégâts")
            else:
                damage = player.attack()
                adv.reduction_of_pv(damage)
                await ctx.send(f"{player.name} attaque, {adv.name} prend {damage} de dégâts")
        else:
            await ctx.send(f"{player.name} attaque mais {adv.name} esquive =p !")

        # Check adv mort ou en vie
        if adv.alive is False:
            await ctx.send(f"{adv.name} n'a plus de pv.")
        else:
            # player_two attaque ou rate
            if adv.touch_or_esquive(player):
                adv_damage = adv.attack()
                player.reduction_of_pv(adv_damage)
                await ctx.send(f"{adv.name} riposte, {player.name} perd {adv_damage} de pv")
            else:
                await ctx.send(f"{adv.name} attaque mais {player.name} réussi a esquiver !")

        if player.alive is False:
            await ctx.send(f"{player.name} n'a plus de pv.")

        await ctx.send(f"{player.name} : {player.pv} pv, {adv.name} : {adv.pv} pv")

    async def healer(player):
        await ctx.send(
            f"{player.name} plonge la main dans sa poche et en sort une petite fiole....")
        await ctx.send(f"Hé hop! Dans le gosier !")
        pv_potion = player.take_care_of_yourself()
        await ctx.send(f"La potion de vitalité lui donne {pv_potion} de pv en plus")
        await ctx.send(f"{player.name} a maintenant {player.pv} pv ...")

    await ctx.send("Un combat contre un Krogan ???")
    await ctx.reply('1 <-Oui , 2 <-Non', mention_author=True)

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    try:
        guess = await self.wait_for('message', check=is_correct)
    except asyncio:
        return await ctx.send("C'est 1 ou 2", mention_author=True)

    if int(guess.content) == 1:
        # init both fighters
        # player = Fighter(name=,strength=, perception=, endurance=, charisma=, intelligence=, agility=, luck=)
        # player_one = Fighter(name=message.author.name, strength=7, perception=4, endurance=10, charisma=5,
        #                      intelligence=7, agility=5, luck=2)
        # player_two = Fighter(name="Grunt", strength=7, perception=4, endurance=15, charisma=5,
        #                      intelligence=5, agility=3, luck=4)
        player_one = create_fighter(ctx.author.name)
        await db_create_user_if_exist(ctx)  # insert in db user information for stat
        player_two = create_fighter("Grunt")

        # presentation of the characteristics of the fighters
        await ctx.send(f" HELLLOOO, Bienvenue pour le combat entre deux poids lourd :imp:")
        await ctx.send(
            f"Dans le coin rouge: :point_left:{player_one.name} avec {player_two.pv} PV, {player_one.heal} "
            f"Potions de soin et une force estimé a {player_one.strength} :muscle: !")
        await ctx.send(f"Dans le coin bleu: :point_right:{player_two.name} avec {player_two.pv} PV,"
                       f" pas besoin de potion pour un Krogan, la force de ce guerrier est de "
                       f"{player_two.strength} :muscle: !")

        await ctx.send("🥊")
        await ctx.send("Fight!!")

        # first round
        await battle(player_one, player_two)

        # Tant que les deux sont en vies
        while player_one.alive and player_two.alive:

            if player_one.heal == 0:
                await ctx.reply("1<- Attaquer ||  3 <- Etat PV", mention_author=True)
            else:
                await ctx.reply(f"1<- Attaquer |-| 2<- Potion de Soin reste : {player_one.heal} |-| 3 <- "
                                f"Etat PV",
                                mention_author=True)
            try:
                decision = await self.wait_for('message', check=is_correct)
            except asyncio:
                await ctx.send("il faut faire un choix!!")
            else:
                pass

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
                stat = player_one.is_critical()
                damage = 0
                if stat:
                    damage = player_one.critical_attack()
                await ctx.send(f"{stat} -> {damage}")
        else:
            if not player_one.alive:
                await ctx.send(f"{player_two.name} est le grand gagnant :muscle:!")
                # /db_fight_add_score(ctx.author.id, 0)
            elif not player_two.alive:
                await ctx.send(f"{player_one.name} gagne contre {player_two.name} :muscle:!")
                # db_fight_add_score(ctx.author.id, 1)

    else:
        await ctx.send("Ok ciao !", mention_author=True)
