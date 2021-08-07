import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import asyncio

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
        # if "shepard" in message.content.lower():
        #     await message.channel.send(content=f"oui @{message.author.display_name} ?")

        if message.content.startswith('!cmd'):
            await message.reply('hello, game(Nombre Myster), fight(ToiVSGrunt)', mention_author=True)

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
                return await message.channel.send('Sorry, tu as pris trop de temps, c\'etait {}.'.format(answer),
                                                  mention_author=True)

            if int(guess.content) == answer:
                await message.channel.send('GG!')
            else:
                await message.channel.send('Oops. Perdu c\'etait {}.'.format(answer), mention_author=True)

        # Mini Rpg Fight Game
        if message.content.startswith('!fight'):
            class Fighter:
                def __init__(self, name, pv, heal, min_strength, max_strength, alive=True):
                    self.name = name
                    self.pv = pv
                    self.heal = heal
                    self.min_strength = min_strength
                    self.max_strength = max_strength
                    self.alive = alive

            async def attack(f, adv):
                atk_f = random.randint(f.min_strength, f.max_strength)
                adv.pv -= atk_f
                await message.channel.send(f"{f.name} attaque, {adv.name} perd {atk_f} pv")
                atk_b = random.randint(adv.min_strength, adv.max_strength)
                f.pv -= atk_b
                await message.channel.send(f"{adv.name} riposte, {f.name} perd {atk_b} pv")
                await message.channel.send(f"{f.name} : {f.pv} pv, {adv.name} : {adv.pv} pv")

            async def healer(f, adv):
                potion = random.randint(15, 50)
                f.heal -= 1
                f.pv += potion
                await message.channel.send(f"{f.name} utilise une popo de soin et recupere {potion} pv",
                                           mention_author=True)
                atk_b = random.randint(adv.min_strength, adv.max_strength)
                f.pv -= atk_b
                await message.channel.send(f"{adv.name} attaque', {f.name} perd {atk_b} pv {f.name}")
                await message.channel.send(f"{f.name} : {f.pv} pv, {adv.name} : {adv.pv} pv")

            await message.channel.send(f"Un combat contre un Krogan???")
            await message.reply('1<-Oui , 2<-Non', mention_author=True)

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            try:
                guess = await self.wait_for('message', check=is_correct)
            except asyncio:
                return await message.channel.send("c'est 1 ou 2", mention_author=True)

            if int(guess.content) == 1:
                # init both fighters
                fighter = Fighter(message.author.name, 50, 3, 5, 10)
                botghter = Fighter("Grunt", 50, 0, 7, 15)

                # presentation of the characteristics of the fighters
                await message.channel.send(f"Bienvenue pour le combat entre deux poids lourd :devilparrot:")
                await message.channel.send(
                    f"Dans le coin rouge: {fighter.name} avec {fighter.pv} PV, {fighter.heal} Potion de soin, "
                    f" et une force entre {fighter.min_strength} et {fighter.max_strength} ")
                await message.channel.send(f"Dans le coin bleu: {botghter.name} avec {botghter.pv} PV, pas besoin de "
                                           f"potion pour un Krogan, la force de ce guerrier est entre "
                                           f"{botghter.min_strength} et {botghter.max_strength} ")

                await message.channel.send("🥊")
                await message.channel.send("Fight!!")

                # First attaque no choice!
                await attack(fighter, botghter)

                while fighter.alive or botghter.alive:
                    await message.reply('1<- Attaquer || 2<- Potion de Soin', mention_author=True)
                    try:
                        decision = await self.wait_for('message', check=is_correct)
                    except asyncio:
                        await message.channel.send("il faut faire un choix!!")
                    else:
                        if int(decision.content) == 1:
                            await attack(fighter, botghter)
                        else:
                            await healer(fighter, botghter)

                    if botghter.pv <= 0 and fighter.pv <= 0:
                        fighter.alive = False
                        botghter.alive = False
                        await message.channel.send("Les deux combattant sont K.O.")
                        break
                    elif fighter.pv <= 0:
                        fighter.alive = False
                        await message.channel.send(f"{botghter.name} Win!")
                        break
                    elif botghter.pv <= 0:
                        botghter.alive = False
                        await message.channel.send(f"{fighter.name} Win!")
                        break

            else:
                await message.channel.send("Ok a plus", mention_author=True)


shepard = CommandantShepard()

shepard.run(os.getenv("TOKEN"))
