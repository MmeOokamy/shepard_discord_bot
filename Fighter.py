# coding:utf-8
import discord
import random


class Fighter:
    alive = True
    heal = 2
    pv = 50  # pv for all?

    def __init__(self, name, strength, perception, endurance, charisma, intelligence, agility, luck):
        assert name.isalnum(), "Attribut 'name': alphanumeric "
        assert isinstance(strength, int) and 0 < strength <= 20, "Attribut Strength : entier entre 0 et 20"
        assert isinstance(perception, int) and 0 < perception <= 20, "Attribut perception : entier entre 0 et 20"
        assert isinstance(endurance, int) and 7 < endurance <= 15, "Attribut Endurance / pv : entier entre 15 et 25"
        assert isinstance(charisma, int) and 0 < charisma <= 20, "Attribut charisma : entier entre 0 et 20"
        assert isinstance(intelligence, int) and 0 < intelligence <= 20, "Attribut intelligence : entier entre 0 et 20"
        assert isinstance(agility, int) and 0 < agility <= 20, "Attribut Agility: entier entre 0 et 20"
        assert isinstance(luck, int) and 0 < luck <= 20, "Attribut Lucky: entier entre 0 et 20"

        self.name = name
        self.strength = strength  # force
        self.perception = perception  # precision
        self.endurance = endurance  # def
        self.charisma = charisma
        self.intelligence = intelligence
        self.agility = agility  # agi
        self.luck = luck

    def touch_or_esquive(self, adversary):
        d20 = random.randint(1, 20)
        toe = True if (d20 * self.strength) >= adversary.endurance else False
        return toe

    def attack(self, adversary):
        x = random.randint(1, 10)
        damage = int(self.strength) + x
        damage = round(damage)
        return damage

    def take_care_of_yourself(self):
        pv_potion = random.randint(15, 25)
        self.heal -= 1
        return pv_potion

    def reduction_of_pv(self, damage):
        self.pv -= damage
        return self.pv
