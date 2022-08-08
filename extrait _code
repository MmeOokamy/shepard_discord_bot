class Fighter:
    def __init__(self, name, pv, heal, min_strength, max_strength, alive=True):
        self.name = name
        self.pv = pv
        self.heal = heal
        self.min_strength = min_strength
        self.max_strength = max_strength
        self.alive = alive

    async def action(self, adversary):
        # lance le de de force
        power = random.randint(self.min_strength, self.max_strength)
        adversary.pv = int(adversary.pv) - int(power)
        await message.channel.send(f"{adversary.name} est attaqué par {self.name} mais ne riposte pas")

    async def take_care_of_yourself(self):
        # boit la potion
        await message.channel.send(
            f"{self.name} plonge la main dans sa poche et en sort une petite fiole....")
        await message.channel.send(f"Hé hop! Dans le gosier !")
        pv_potion = random.randint(15, 50)

        await message.channel.send(f"La potion de vitalité lui donne {pv_potion} de pv en plus")
        self.pv += pv_potion
        await message.channel.send(f"{self.name} a maintenant {self.pv} pv ...")


async def attack(f, adv):
    atk_f = random.randint(f.min_strength, f.max_strength)
    adv.pv -= atk_f
    await message.channel.send(f"{f.name} attaque, {adv.name} perd {atk_f} pv")
    if adv.pv > 0:
        atk_b = random.randint(adv.min_strength, adv.max_strength)
        f.pv -= atk_b
        await message.channel.send(f"{adv.name} riposte, {f.name} perd {atk_b} pv")
        if f.pv > 0:
            await message.channel.send(f"{f.name} : {f.pv} pv, {adv.name} : {adv.pv} pv")
        else:
            await message.channel.send(f"{f.name} n'a plus de pv.")
    else:
        await message.channel.send(f"{adv.name} n'a plus de pv.")


async def healer(f, adv):
    potion = random.randint(15, 50)
    f.heal -= 1
    f.pv = int(f.pv) + int(potion)
    await message.channel.send(f"{f.name} utilise une popo de soin et recupere {potion} pv",
                               mention_author=True)
    atk_b = random.randint(adv.min_strength, adv.max_strength)
    f.pv -= atk_b
    await message.channel.send(f"{adv.name} attaque, {f.name} perd {atk_b} pv {f.name}")
    await message.channel.send(f"{f.name} : {f.pv} pv, {adv.name} : {adv.pv} pv")



                # fighter = Fighter(message.author.name, 50, 3, 5, 10)
                # botghter = Fighter("Grunt", 50, 0, 7, 15)

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
                    if fighter.heal == 0:
                        await message.reply('1<- Attaquer || Tu n\'as plus de potion', mention_author=True)
                    else:
                        await message.reply(
                            f'1<- Attaquer |-| 2<- Potion de Soin reste : {fighter.heal} - || 3 <= pour test',
                            mention_author=True)

                    try:
                        decision = await self.wait_for('message', check=is_correct)
                    except asyncio:
                        await message.channel.send("il faut faire un choix!!")
                    else:
                        if int(decision.content) == 1:
                            await attack(fighter, botghter)
                        elif int(decision.content) == 3:
                            await fighter.action(botghter)
                        elif int(decision.content) == 4:
                            await fighter.take_care_of_yourself()
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
