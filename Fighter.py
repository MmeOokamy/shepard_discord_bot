# coding:utf-8
import discord
import random


class Fighter:
    alive = True
    heal = 2
    pv = 50  # pv for all?
    critical_rate = 0.25

    def __init__(self, name, strength, perception, endurance, charisma, intelligence, agility, luck):
        assert name.isalnum(), "Attribut 'name': alphanumeric "
        assert isinstance(strength, int) and 0 < strength <= 20, "Attribut Strength : entier entre 1 et 20"
        assert isinstance(perception, int) and 0 < perception <= 20, "Attribut perception : entier entre 1 et 20"
        assert isinstance(endurance, int) and 0 <= endurance <= 15, "Attribut Endurance entier entre 7 et 15"
        assert isinstance(charisma, int) and 0 < charisma <= 20, "Attribut charisma : entier entre 1 et 20"
        assert isinstance(intelligence, int) and 0 < intelligence <= 20, "Attribut intelligence : entier entre 1 et 20"
        assert isinstance(agility, int) and 0 < agility <= 20, "Attribut Agility: entier entre 1 et 20"
        assert isinstance(luck, int) and 0 < luck <= 20, "Attribut Lucky: entier entre 1 et 20"

        self.name = name
        self.strength = strength  # force
        self.perception = perception  # precision
        self.endurance = endurance  # def
        self.charisma = charisma
        self.intelligence = intelligence
        self.agility = agility  # agi
        self.luck = luck

    def special(self):
        return f"name={self.name}, strength={self.strength}, perception={self.perception}, endurance={self.endurance}" \
               f", charisma={self.charisma}, intelligence={self.intelligence}, agility={self.agility}, luck={self.luck}"

    def touch_or_esquive(self, adversary):
        d20 = random.randint(1, 20)
        atk = (d20 * self.strength) / self.agility
        adv = (adversary.endurance * adversary.perception) / adversary.luck
        toe = True if atk >= adv else False
        return toe

    def is_critical(self):
        return True if random.randint(1, (self.luck + self.agility)) == 1 else False

    def critical_attack(self):
        return round(self.attack() * self.critical_rate)

    def attack(self):
        x = random.randint(1, 10)
        damage = int(self.strength) + x
        damage = round(damage)
        return damage

    def take_care_of_yourself(self):
        pv_potion = random.randint(15, 25)
        self.heal -= 1
        self.pv += pv_potion
        return pv_potion

    def reduction_of_pv(self, damage):
        self.pv -= damage
        if self.pv <= 0:
            self.pv = 0
            self.alive = False


# Function for random stat and create fighter
# return Fighter Objects
def create_fighter(player_name):
    # strength 0 < strength <= 20
    s = random.randint(1, 20)
    # perception 0 < perception <= 20
    p = random.randint(1, 10)
    # endurance 7 <= endurance <= 15
    e = random.randint(7, 15)
    # charisma 0 < charisma <= 20
    c = random.randint(1, 10)
    # intelligence 0 < intelligence <= 20
    i = random.randint(1, 10)
    # agility 0 < agility <= 20
    a = random.randint(1, 10)
    # luck 0 < luck <= 20
    lu = random.randint(1, 10)

    return Fighter(player_name, s, p, e, c, i, a, lu)
