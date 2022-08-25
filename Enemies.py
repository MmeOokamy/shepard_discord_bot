from Fighter import Fighter

# (lvl, player_name, s, p, e, c, i, a, lu)
enemies = [
    (1, "debutant", 2, 1, 2, 1, 1, 2, 1),
    (2, "novice", 2, 1, 2, 1, 1, 2, 1),
    (3, "intermediaire", 2, 1, 2, 1, 1, 2, 1),
    (4, "pro", 2, 1, 2, 1, 1, 2, 1),
]


class Enemies(Fighter):

    def __init__(self, name, strength, perception, endurance, charisma, intelligence, agility, luck):
        super().__init__(name, strength, perception, endurance, charisma, intelligence, agility, luck)
        self.critical_rate = 0.30
        self.pv = 45
        self.heal = 0

    def balanced_stats_for_fight(self, lvl_of_player):
        # ajuste special de l'adversaire pour avoir une difficulté croissante
        pass


e = {}
for x in enemies:
    i = Enemies(x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    e[x[0]] = i
    # print(i)

for item in e:
    print(e[item].name)
