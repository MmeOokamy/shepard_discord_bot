from Fighter import Fighter


# enemies = [
#     {
#         id: 1,
#         name: 'BadBlob',
#         strength: 0,
#         perception: 0,
#         endurance: 0,
#         charisma: 0,
#         intelligence: 0,
#         agility: 0,
#         luck: 0
#     },
# ]


class Enemies(Fighter):

    def __init__(self, name, strength, perception, endurance, charisma, intelligence, agility, luck):
        super().__init__(name, strength, perception, endurance, charisma, intelligence, agility, luck)
        self.critical_rate = 0.30
        self.pv = 45
        self.heal = 0

    def balanced_stats_for_fight(self, lvl_of_player):
        # ajuste special de l'adversaire pour avoir une difficulté croissante
        pass
