import os
import sys
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import asyncio
import sqlite3

from db import *  # sqlite execute fonction =)
from Fighter import create_fighter
from sentence import say_hello

load_dotenv()

intents = discord.Intents.default()

intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)


async def db_create_user_if_exist(message):
    response = db_create_user(message.author.id, message.author)
    print(response)


class CommandantShepard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!!")

    async def on_ready(self):
        print(f"{self.user.name} is ready")
        print('Database Initiation ....')
        try:
            db_connect()
            print('Database OK')
        except OSError as err:
            print("OS error: {0}".format(err))
            print("Unexpected error:", sys.exc_info()[0])

        print(self.user.id)
        print(self.user)
        print('------')

    async def on_message(self, message):

        if "shepard" in message.content.lower():
            await message.channel.send(content=f"@{message.author.display_name}, {random.choice(say_hello)}")

        elif message.content.startswith('!cmd'):
            await message.reply('hello, game(Nombre Mystère), fight(ToiVSGrunt)', mention_author=True)
            await message.reply('Il est aussi possible de connaitre ses scores avec la commande !stats',
                                mention_author=True)

        elif message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        # Mini mystery number Game
        elif message.content.startswith('!game'):
            await message.reply('entre 1 et 10', mention_author=True)

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, tu as pris trop de temps, c\'était {}.'.format(answer),
                                                  mention_author=True)

            if int(guess.content) == answer:
                await message.channel.send('GG!')
            else:
                await message.channel.send('Oops. Perdu c\'était {}.'.format(answer), mention_author=True)

        # Mini Rpg Fight Game
        elif message.content.startswith('!fight'):
            async def status_fighter(player, adv):
                await message.channel.send(f"{player.name} : {player.pv}")
                await message.channel.send(f"{player.special()}")
                await message.channel.send(f"{adv.name} : {adv.pv}")
                await message.channel.send(f"{adv.special()}")

            async def battle(player, adv):
                # player_one attaque ou rate
                if player.touch_or_esquive(adv):
                    if player.is_critical():
                        damage_crit = player.critical_attack()
                        adv.reduction_of_pv(damage_crit)
                        await message.channel.send(f"{player.name} fait un critique, {adv.name} prend {damage_crit} "
                                                   f"de dégâts")
                    else:
                        damage = player.attack()
                        adv.reduction_of_pv(damage)
                        await message.channel.send(f"{player.name} attaque, {adv.name} prend {damage} de dégâts")
                else:
                    await message.channel.send(f"{player.name} attaque mais {adv.name} esquive =p !")

                # Check adv mort ou en vie
                if adv.alive is False:
                    await message.channel.send(f"{adv.name} n'a plus de pv.")
                else:
                    # player_two attaque ou rate
                    if adv.touch_or_esquive(player):
                        adv_damage = adv.attack()
                        player.reduction_of_pv(adv_damage)
                        await message.channel.send(f"{adv.name} riposte, {player.name} perd {adv_damage} de pv")
                    else:
                        await message.channel.send(f"{adv.name} attaque mais {player.name} réussi a esquiver !")

                if player.alive is False:
                    await message.channel.send(f"{player.name} n'a plus de pv.")

                await message.channel.send(f"{player.name} : {player.pv} pv, {adv.name} : {adv.pv} pv")

            async def healer(player):
                await message.channel.send(
                    f"{player.name} plonge la main dans sa poche et en sort une petite fiole....")
                await message.channel.send(f"Hé hop! Dans le gosier !")
                pv_potion = player.take_care_of_yourself()
                await message.channel.send(f"La potion de vitalité lui donne {pv_potion} de pv en plus")
                await message.channel.send(f"{player.name} a maintenant {player.pv} pv ...")

            await message.channel.send("Un combat contre un Krogan ???")
            await message.reply('1 <-Oui , 2 <-Non', mention_author=True)

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            try:
                guess = await self.wait_for('message', check=is_correct)
            except asyncio:
                return await message.channel.send("C'est 1 ou 2", mention_author=True)

            if int(guess.content) == 1:
                # init both fighters
                # player = Fighter(name=,strength=, perception=, endurance=, charisma=, intelligence=, agility=, luck=)
                # player_one = Fighter(name=message.author.name, strength=7, perception=4, endurance=10, charisma=5,
                #                      intelligence=7, agility=5, luck=2)
                # player_two = Fighter(name="Grunt", strength=7, perception=4, endurance=15, charisma=5,
                #                      intelligence=5, agility=3, luck=4)
                player_one = create_fighter(message.author.name)
                await db_create_user_if_exist(message)  # insert in db user information for stat
                player_two = create_fighter("Grunt")

                # presentation of the characteristics of the fighters
                await message.channel.send(f"Bienvenue pour le combat entre deux poids lourd :imp:")
                await message.channel.send(
                    f"Dans le coin rouge: :point_left:{player_one.name} avec {player_two.pv} PV, {player_one.heal} "
                    f"Potions de soin et une force estimé a {player_one.strength} :muscle: !")
                await message.channel.send(f"Dans le coin bleu: :point_right:{player_two.name} avec {player_two.pv} PV,"
                                           f" pas besoin de potion pour un Krogan, la force de ce guerrier est de "
                                           f"{player_two.strength} :muscle: !")

                await message.channel.send("🥊")
                await message.channel.send("Fight!!")

                # first round
                await battle(player_one, player_two)

                # Tant que les deux sont en vies
                while player_one.alive and player_two.alive:

                    if player_one.heal == 0:
                        await message.reply("1<- Attaquer ||  3 <- Etat PV", mention_author=True)
                    else:
                        await message.reply(f"1<- Attaquer |-| 2<- Potion de Soin reste : {player_one.heal} |-| 3 <- "
                                            f"Etat PV",
                                            mention_author=True)
                    try:
                        decision = await self.wait_for('message', check=is_correct)
                    except asyncio:
                        await message.channel.send("il faut faire un choix!!")
                    else:
                        pass

                    if int(decision.content) == 1:
                        await battle(player_one, player_two)
                    elif int(decision.content) == 2:
                        if player_one.heal != 0:
                            await healer(player_one)
                        else:
                            await message.channel.send("Tu n'as plus de potion !")
                    elif int(decision.content) == 3:
                        await status_fighter(player_one, player_two)
                    elif int(decision.content) == 4:
                        stat = player_one.is_critical()
                        damage = 0
                        if stat:
                            damage = player_one.critical_attack()
                        await message.channel.send(f"{stat} -> {damage}")
                else:
                    if not player_one.alive:
                        await message.channel.send(f"{player_two.name} est le grand gagnant :muscle:!")
                        db_fight_add_score(message.author.id, 0)
                    elif not player_two.alive:
                        await message.channel.send(f"{player_one.name} gagne contre {player_two.name} :muscle:!")
                        db_fight_add_score(message.author.id, 1)

            else:
                await message.channel.send("Ok ciao !", mention_author=True)

        elif message.content.startswith('!color'):
            await message.channel.send("```diff\n- hellow\n```", mention_author=True)

        elif message.content.startswith('!stats'):
            fight_stats = db_fight_user_stats(message.author.id)
            user_stats = db_user_stats(message.author.id)
            await message.channel.send(f"{user_stats['user']}, "
                                       f"tu as {'0' if user_stats['xp'] is None else user_stats['xp']} points d'xp, "
                                       f"avec un score à {'0' if user_stats['score'] is None else user_stats['score']} "
                                       f"points")
            await message.channel.send(f"{user_stats['user']}, tu as un ratio de {user_stats['fight_win']} victoire "
                                       f"pour {int(user_stats['fight_win']) + int(user_stats['fight_loose'])} combats")

        # @bot.command()
        # async def test(ctx, arg):
        #     await ctx.send(arg)


shepard = CommandantShepard()

shepard.run(os.getenv("TOKEN"))
