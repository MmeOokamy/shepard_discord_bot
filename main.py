import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import asyncio

from Fighter import Fighter

load_dotenv()

intents = discord.Intents.default()

intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)


class CommandantShepard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!!")

    async def on_ready(self):
        print(f"{self.user.name} is ready")
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if "shepard" in message.content.lower():
            await message.channel.send(content=f"oui @{message.author.display_name} ?")

        if message.content.startswith('!cmd'):
            await message.reply('hello, game(Nombre Mystère), fight(ToiVSGrunt)', mention_author=True)

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        # Mini mystery number Game
        if message.content.startswith('!game'):
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
        if message.content.startswith('!fight'):

            async def status_fighter(player, adv):
                await message.channel.send(f"{player.name} - {player.endurance} pv")
                await message.channel.send(f"{adv.name} - {adv.endurance} pv")

            async def battle(player, adv):
                damage = player.attack(adv)
                await message.channel.send(f"{player.name} degat {damage}")

            async def healer(player):
                await message.channel.send(
                    f"{player.name} plonge la main dans sa poche et en sort une petite fiole....")
                await message.channel.send(f"Hé hop! Dans le gosier !")
                pv_potion = player.take_care_of_yourself()
                await message.channel.send(f"La potion de vitalité lui donne {pv_potion} de pv en plus")
                player.endurance += pv_potion
                await message.channel.send(f"{player.name} a maintenant {player.endurance} pv ...")

            await message.channel.send("Un combat contre un Krogan ???")
            await message.reply('1 <-Oui , 2 <-Non', mention_author=True)

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            try:
                guess = await self.wait_for('message', check=is_correct)
            except asyncio:
                return await message.channel.send("c'est 1 ou 2", mention_author=True)

            if int(guess.content) == 1:
                # init both fighters
                # player = Fighter(name=,strength=, perception=, endurance=, charisma=, intelligence=, agility=, luck=)
                player_one = Fighter(name=message.author.name, strength=7, perception=4, endurance=20, charisma=5,
                                     intelligence=7, agility=3, luck=2)
                player_two = Fighter(name="Grunt", strength=7, perception=4, endurance=25, charisma=5,
                                     intelligence=7, agility=3, luck=2)

                # presentation of the characteristics of the fighters
                await message.channel.send(f"Bienvenue pour le combat entre deux poids lourd :imp:")
                await message.channel.send(
                    f"Dans le coin rouge: {player_one.name} avec {player_two.endurance} PV, {player_one.heal} Potion "
                    f"de soin et une force estimé a {player_two.strength} ")
                await message.channel.send(f"Dans le coin bleu: {player_two.name} avec {player_two.endurance} PV, pas "
                                           f"besoin de potion pour un Krogan, la force de ce guerrier est de "
                                           f"{player_two.strength} !")

                await message.channel.send("🥊")
                await message.channel.send("Fight!!")

                # first round
                await battle(player_one, player_two)

                while player_one.alive or player_two.alive:
                    if player_one.heal == 0:
                        await message.reply("1<- Attaquer ||  3 <- Etat", mention_author=True)
                    else:
                        await message.reply(f"1<- Attaquer |-| 2<- Potion de Soin reste : {player_one.heal} |-| 3 <- "
                                            f"Etat",
                                            mention_author=True)
                    try:
                        decision = await self.wait_for('message', check=is_correct)
                    except asyncio:
                        await message.channel.send("il faut faire un choix!!")
                    else:
                        if int(decision.content) == 1:
                            await battle(player_one, player_two)
                        elif int(decision.content) == 2:
                            if player_one.heal != 0:
                                await message.channel.send("Tu n'as plus de potion !")
                            else:
                                await healer(player_one)
                        elif int(decision.content) == 3:
                            await status_fighter(player_one, player_two)

                # First attaque no choice!
                # await attack(fighter, botghter)
                #
                # while fighter.alive or botghter.alive:
                #     if fighter.heal == 0:
                #         await message.reply('1<- Attaquer || Tu n\'as plus de potion', mention_author=True)
                #     else:
                #         await message.reply(
                #             f'1<- Attaquer |-| 2<- Potion de Soin reste : {fighter.heal} - || 3 <= pour test',
                #             mention_author=True)
                #
                #     try:
                #         decision = await self.wait_for('message', check=is_correct)
                #     except asyncio:
                #         await message.channel.send("il faut faire un choix!!")
                #     else:
                #         if int(decision.content) == 1:
                #             await attack(fighter, botghter)
                #         elif int(decision.content) == 3:
                #             await fighter.action(botghter)
                #         elif int(decision.content) == 4:
                #             await fighter.take_care_of_yourself()
                #         else:
                #             await healer(fighter, botghter)
                #
                #     if botghter.pv <= 0 and fighter.pv <= 0:
                #         fighter.alive = False
                #         botghter.alive = False
                #         await message.channel.send("Les deux combattant sont K.O.")
                #         break
                #     elif fighter.pv <= 0:
                #         fighter.alive = False
                #         await message.channel.send(f"{botghter.name} Win!")
                #         break
                #     elif botghter.pv <= 0:
                #         botghter.alive = False
                #         await message.channel.send(f"{fighter.name} Win!")
                #         break

            else:
                await message.channel.send("Ok a plus", mention_author=True)

        if message.content.startswith('!color'):
            await message.channel.send("```diff\n- hellow\n```", mention_author=True)

        # @bot.command()
        # async def test(ctx, arg):
        #     await ctx.send(arg)


shepard = CommandantShepard()

shepard.run(os.getenv("TOKEN"))
