# coding:utf-8
import unittest
import sys
import random

sys.path.insert(0, ".")
from battle.Fighter import Fighter
from db import *
from dotenv import load_dotenv

load_dotenv()


class TestFighter(unittest.TestCase):

    def setUp(self):
        # self.player_one = create_fighter('Shepard commander')
        # self.player_two = create_fighter('Grunt')
        # Player Two Bot
        user_id = int(os.getenv("ADMIN_ID"))
        po = db_fight_get_user_special_for_create_fighter(user_id)
        self.player_one = Fighter(po['name'], po['strength'], po['perception'], po['endurance'], po['charisma'],
                                  po['intelligence'], po['agility'], po['luck'])
        adv = db_fight_get_adversary_by_id_for_create(2, user_id)
        self.pts = int(adv['pts'])
        self.player_two = Fighter(adv['name'], adv['strength'], adv['perception'], adv['endurance'], adv['charisma'],
                                  adv['intelligence'], adv['agility'], adv['luck'])

    def test_special(self):
        print(self.__class__.test_special.__name__)
        print(self.player_one.special())
        print(self.player_two.special())

    def test_player_is_instance_of_fighter(self):
        print(self.__class__.test_player_is_instance_of_fighter.__name__)
        self.assertIsInstance(self.player_one, Fighter)
        self.assertIsInstance(self.player_two, Fighter)

    def test_critical_attack(self):
        print(self.__class__.test_critical_attack.__name__)
        crit_list = []
        # i = 0
        for i in range(10):
            i += 1
            critical = self.player_one.critical_attack()
            self.assertGreater(critical, 0)
            crit_list.append(critical)
        print(crit_list)

    def test_attack(self):
        print(self.__class__.test_attack.__name__)
        atk_list = []
        # i = 0
        for i in range(10):
            i += 1
            atk = self.player_one.attack()
            self.assertGreater(atk, 0)
            atk_list.append(atk)
        print(atk_list)

    def test_attack_critical_attack(self):
        print(self.__class__.test_attack_critical_attack.__name__)
        atk_list = {}
        # i = 0
        for i in range(10):
            i += 1
            atk = self.player_one.attack()
            critical = self.player_one.critical_attack(atk)
            self.assertGreater(atk, 0)
            self.assertGreater(critical, 0)
            self.assertGreater(critical, atk)
            atk_list[atk] = critical
        print(atk_list)


if __name__ == '__main__':
    unittest.main()
