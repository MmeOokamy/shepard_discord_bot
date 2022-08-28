# coding:utf-8
import unittest
import sys

sys.path.insert(0, ".")
from Fighter import Fighter, create_fighter
from Shepard_Origin.Enemies import Enemies


class TestFighter(unittest.TestCase):

    def test_Enemies_is_subclass_of_Fighter(self):
        issubclass(Enemies, Fighter)

    def setUp(self):
        self.player_one = create_fighter('Shepard')
        self.player_two = create_fighter('Grunt')
        self.enemie_one = Enemies(name="Soverein", strength=7, perception=5, endurance=10, charisma=6,
                                  intelligence=5, agility=5, luck=4)
        self.enemie_two = Enemies(name="Queen", strength=8, perception=4, endurance=15, charisma=5,
                                  intelligence=5, agility=3, luck=4)

    def test_special(self):
        print(self.player_one.special())
        print(self.player_two.special())
        print(self.enemie_one.special())
        print(self.enemie_two.special())

    def test_player_is_instance_of_fighter(self):
        self.assertIsInstance(self.player_one, Fighter)
        self.assertIsInstance(self.player_two, Fighter)

    def test_enemies_is_instance_of_enemie(self):
        self.assertIsInstance(self.enemie_one, Enemies)
        self.assertIsInstance(self.enemie_two, Enemies)

    def test_damage_is_positive(self):
        self.assertGreater(self.player_one.attack(), 0)
        self.assertGreater(self.enemie_one.attack(), 0)
        self.assertGreater(self.player_two.attack(), 0)

    def test_critical_attack(self):
        self.assertGreater(self.player_one.critical_attack(), 0)
        self.assertGreater(self.player_two.critical_attack(), 0)

    def test_is_critical(self):
        # self.assertIs(self.player_two.is_critical(), False, msg='No Critical attack')
        bool_type = True if type(self.player_two.is_critical()) is bool \
                            and type(self.player_one.is_critical()) is bool else False
        self.assertTrue(bool_type, msg='Not boolean response')


if __name__ == '__main__':
    unittest.main()
