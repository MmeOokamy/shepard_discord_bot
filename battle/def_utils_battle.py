# coding: utf-8

def special_txt(player):
    return (f"Force : {player.strength} :muscle:, Perception : {player.perception} :eye:, "
            f"Endurance : {player.endurance} :person_running:, "
            f"Charisme : {player.charisma} :superhero:, "
            f"Intelligence : {player.intelligence}:brain:, "
            f"Agilité : {player.agility} :person_doing_cartwheel:, "
            f"Chance : {player.luck}:four_leaf_clover:")


# def gestion_special_txt(u):
#     print(u)
#     return (f"|   :muscle:  |:eye:|:person_running:|:superhero:|:brain:|:person_doing_cartwheel:|:four_leaf_clover:|\n"
#             f"| Force | Perception | Endurance | Charisme | Intelligence | Agilité | Chance |\n"
#             f"|{u['strength']}|{u['perception']} |{u['endurance']}|{u['charisma']}|{u['intelligence']}"
#             f"|{u['agility']}|{u['luck']}|")
# def adv_embed():
#     embed = discord.Embed(title="Title here", description="description here", color=0x552E12)
#     embed.set_author(name=self.bot.user,
#                      icon_url="")
#     embed.add_field(name="Field title", value="Fielf value", inline=False)
#     await ctx.send(embed=embed)
