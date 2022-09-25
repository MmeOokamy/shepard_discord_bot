# coding: utf-8
import discord
from discord.ext import commands

from db import db_fight_get_adversary_by_id_for_create, db_fight_get_user_special_for_create_fighter, \
    db_fight_get_adversary


def special_txt(player):
    return (f"Force : {player.strength} :muscle:, Perception : {player.perception} :eye:, "
            f"Endurance : {player.endurance} :person_running:, "
            f"Charisme : {player.charisma} :superhero:, "
            f"Intelligence : {player.intelligence}:brain:, "
            f"Agilité : {player.agility} :person_doing_cartwheel:, "
            f"Chance : {player.luck}:four_leaf_clover:")


def embed_one(player, color, race):
    embed = discord.Embed(description=f"", color=color)
    embed.set_author(name=f"{player.name} ({race})")
    embed.add_field(name="S.P.E.C.I.A.L",
                    value=f"{player.strength} :muscle: | "
                          f"{player.perception} :eye: | "
                          f"{player.endurance} :person_running: | "
                          f"{player.charisma} :superhero: | "
                          f"{player.intelligence} :brain: | "
                          f"{player.agility} :person_doing_cartwheel: | "
                          f"{player.luck} :four_leaf_clover:")
    return embed


def embed_atk(step, atk_a, atk_b, rip_a, rip_b, result):
    # 1 embed pour les 2 actions
    embed = discord.Embed(title=f"Round {step}", description=f"=)", color=discord.Colour.random())
    # celui qui attak
    embed.add_field(name=f"{atk_a}", value=f"{atk_b}", inline=False)
    # la riposte
    embed.add_field(name=f"{rip_a}", value=f"{rip_b}", inline=False)
    # resultat vie
    embed.set_footer(text=f"{result}")
    return embed


def embed_adv(ctx):
    adv_list = db_fight_get_adversary()
    embeds = []
    files = []
    colors = ('', 0x1abc9c, 0xe91e63, 0xf1c40f, 0xe74c3c)
    for adv in adv_list:
        special = db_fight_get_adversary_by_id_for_create(adv['id'], ctx.author.id)
        file = discord.File(f"/home/ookamy/Dev/shepard_discord_bot/battle/img/{adv['adv_img']}",
                            filename=adv['adv_img'])
        files.append(file)
        img = f"attachment://{adv['adv_img']}"
        embed = discord.Embed(description=f"{special['xp_win']} pts / victoire", color=colors[adv['id']])
        embed.set_author(name=f"{adv['adv_name']} ({adv['adv_race']})", icon_url=f"{img}")
        embed.set_thumbnail(url=img)
        embed.add_field(name="S.P.E.C.I.A.L",
                        value=f"{special['strength']} :muscle: | "
                              f"{special['perception']} :eye: | "
                              f"{special['endurance']} :person_running: | "
                              f"{special['charisma']} :superhero: | "
                              f"{special['intelligence']} :brain: | "
                              f"{special['agility']} :person_doing_cartwheel: | "
                              f"{special['luck']} :four_leaf_clover:")
        embeds.append(embed)

    ef = {
        "files": files,
        "embeds": embeds
    }
    return ef

# def embed_fighter(ctx, adv):
#     colors = ('', 0x1abc9c, 0xe91e63, 0xf1c40f, 0xe74c3c)
#     player_special = db_fight_get_user_special_for_create_fighter(ctx.author.id)
#     adv_special = db_fight_get_adversary_by_id_for_create(adv['id'], ctx.author.id)
#     file = discord.File(f"/home/ookamy/Dev/shepard_discord_bot/battle/img/{adv['adv_img']}",
#                         filename=adv['adv_img'])
#     files.append(file)
#     img = f"attachment://{adv['adv_img']}"
#     embed = discord.Embed(description=f"{player_special['xp_win']} pts / victoire", color=colors[adv['id']])
#     embed.set_author(name=f"{adv['adv_name']} ({adv['adv_race']})", icon_url=f"{img}")
#     embed.set_thumbnail(url=img)
#     embed.add_field(name="S.P.E.C.I.A.L",
#                     value=f"{player_special['strength']} :muscle: | "
#                           f"{player_special['perception']} :eye: | "
#                           f"{player_special['endurance']} :person_running: | "
#                           f"{player_special['charisma']} :superhero: | "
#                           f"{player_special['intelligence']} :brain: | "
#                           f"{player_special['agility']} :person_doing_cartwheel: | "
#                           f"{player_special['luck']} :four_leaf_clover:")
#


# value=f"Force : {special['strength']} :muscle:, Perception : {special['perception']} :eye:,"
#                                   f"Endurance : {special['endurance']} :person_running:, \n"
#                                   f"Charisme : {special['charisma']} :superhero:, "
#                                   f"Intelligence : {special['intelligence']} :brain:, "
#                                   f"Agilité : {special['agility']} :person_doing_cartwheel:, "
#                                   f"Chance : {special['luck']} :four_leaf_clover:")

# def gestion_special_txt(u):
#     print(u)
#     return (f"|   :muscle:  |:eye:|:person_running:|:superhero:|:brain:|:person_doing_cartwheel:|:four_leaf_clover:|\n"
#             f"| Force | Perception | Endurance | Charisme | Intelligence | Agilité | Chance |\n"
#             f"|{u['strength']}|{u['perception']} |{u['endurance']}|{u['charisma']}|{u['intelligence']}"
#             f"|{u['agility']}|{u['luck']}|")
# def adv_embed():
#     file = discord.File("path/to/my/image.png", filename="image.png")
#     embed = discord.Embed(title="Title here", description="description here", color=0x552E12)
#     embed.set_author(name=self.bot.user,
#                      icon_url="")
#     embed.add_field(name="Field title", value="Fielf value", inline=False)
#     embed.set_image(url="attachment://image.png")
#     await ctx.send(embed=embed)
