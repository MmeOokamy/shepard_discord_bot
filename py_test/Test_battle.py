# coding:utf-8
# import unittest
import sys

sys.path.insert(0, ".")
from Fighter import Fighter, create_fighter
from Shepard_Origin.Enemies import Enemies


# LVL	XP	NB PTS A ATTRIBUER	STRENGTH	PERCEPTION	ENDURANCE	CHARISMA	INTELLIGENCE	AGILITY	LUCK
# 1	50	10	2	1	2	1	1	2	1
# 2	100	5	3	2	3	1	1	3	2
# 3	300	4	3	3	4	2	1	3	3
# 4	900	3	4	3	6	2	1	3	3
# 5	2700	2	5	3	6	2	1	3	4
# 6	4500	1	5	3	6	2	1	4	4
# 7	6300	1	5	3	6	2	2	4	4
# 8	8100	1	5	3	6	3	2	4	4
# 9	9900	1	6	3	6	3	2	4	4
# 10	11700	2	8	3	6	3	2	4	4


def status_fighter(player, adv):
    # print(f"{adv.name} : {adv.pv}")
    print(f"{player.special()}")
    # print(f"{player.name} : {player.pv}")
    print(f"{adv.special()}")


def battle(player, adv):
    # player_one attaque ou rate
    if player.touch_or_esquive(adv):
        if player.is_critical():
            damage_crit = player.critical_attack()
            adv.reduction_of_pv(damage_crit)
            # print(f"{player.name} fait un critique, {adv.name} prend {damage_crit} de dégâts")
        else:
            damage = player.attack()
            adv.reduction_of_pv(damage)
            # print(f"{player.name} attaque, {adv.name} prend {damage} de dégâts")
    else:
        # print(f"{player.name} attaque mais {adv.name} esquive =p !")
        pass
    # Check adv mort ou en vie
    if adv.alive is False:
        # print(f"{adv.name} n'a plus de pv.")
        pass
    else:
        # player_two attaque ou rate
        if adv.touch_or_esquive(player):
            if adv.is_critical():
                damage_crit = adv.critical_attack()
                player.reduction_of_pv(damage_crit)
                # print(f"{adv.name} fait un critique, {player.name} prend {damage_crit} de dégâts")
            else:
                adv_damage = adv.attack()
                player.reduction_of_pv(adv_damage)
                # print(f"{adv.name} riposte, {player.name} perd {adv_damage} de pv")
        # else:
        # print(f"{adv.name} attaque mais {player.name} réussi a esquiver !")
    # if player.alive is False:
    # print(f"{player.name} n'a plus de pv.")
    # print(f"{player.name} : {player.pv} pv, {adv.name} : {adv.pv} pv")


def round_fight(player_one, player_two):
    tour = 0

    while player_one.alive and player_two.alive:
        tour += 1
        print(f'tour : {tour} <<<<<<<<<<<<<<<<<<<<<')
        battle(player_one, player_two)

    else:
        if not player_one.alive:
            print(f"{player_two.name} win !")
        elif not player_two.alive:
            print(f"{player_one.name} gagne !")


print("start 1")
one = Fighter(name="one", strength=2, perception=1, endurance=2, charisma=1,
              intelligence=1, agility=1, luck=1)
two = Fighter(name="two", strength=1, perception=1, endurance=1, charisma=1,
              intelligence=1, agility=1, luck=1)
round_fight(one, two)
print("end 1")

print(" ")
for x in range(1, 10):
    a = Enemies("a", x + 1, x, x + 2, x, x, x, x)
    b = Enemies("b", x + 2, x, x + 1, x, x, x, x)
    print(f"start {x}")
    status_fighter(a, b)
    round_fight(a, b)
    print(f"end {x}")
    print(" ")

print("Finally")
# get player

# get enemie
# combat jusqua la mort
# avec critique possible et esquive
#
# if __name__ == '__main__':
#     pass
