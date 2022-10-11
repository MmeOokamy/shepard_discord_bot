# coding: utf-8
import discord
from discord.ext import commands

from db import *


def special_txt(player):
    return (f"Force : {player.strength} :muscle:, Perception : {player.perception} :eye:, "
            f"Endurance : {player.endurance} :person_running:, "
            f"Charisme : {player.charisma} :superhero:, "
            f"Intelligence : {player.intelligence}:brain:, "
            f"Agilité : {player.agility} :person_doing_cartwheel:, "
            f"Chance : {player.luck}:four_leaf_clover:")


def embed_stats(user_id):
    user = db_fight_get_stats_by_user(user_id)
    embed = discord.Embed(description=f"", color=discord.Colour.random())
    embed.set_author(name=f"")
    embed.add_field(name="S.P.E.C.I.A.L",
                    value=f"")
    return embed


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


def embed_user(ctx):
    special = db_fight_get_user_special_for_create_fighter(ctx.author.id)
    xlw = db_fight_get_user_xp_lvl(ctx.author.id)
    avatar = ctx.author.display_avatar
    embed = discord.Embed(description=f">>> Niv.{xlw['lvl']}/Vic.{xlw['win']}/Exp.{xlw['xp']}", color=0xe67e22)
    embed.set_author(name=ctx.author.display_name, icon_url=avatar)
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="S.P.E.C.I.A.L",
                    value=f"{special['strength']} :muscle: | "
                          f"{special['perception']} :eye: | "
                          f"{special['endurance']} :person_running: | "
                          f"{special['charisma']} :superhero: | "
                          f"{special['intelligence']} :brain: | "
                          f"{special['agility']} :person_doing_cartwheel: | "
                          f"{special['luck']} :four_leaf_clover:")
    return embed


def embed_adv(ctx, adv_id):
    adv = db_fight_get_adversary_by_id(adv_id)
    colors = ('', 0x1abc9c, 0xe91e63, 0xf1c40f, 0xe74c3c)
    special = db_fight_get_adversary_by_id_for_create(adv['id'], ctx.author.id)
    # file = discord.File(f"/home/container/battle/img/{adv['img']}", filename=adv['img'])
    file = discord.File(f"battle/img/{adv['img']}", filename=adv['img'])
    img = f"attachment://{adv['img']}"
    embed = discord.Embed(description=f">>> {special['pts']} pts / victoire", color=colors[adv['id']])
    embed.set_author(name=f"{adv['name']} ({adv['race']})", icon_url=f"{img}")
    embed.set_thumbnail(url=img)
    embed.add_field(name="S.P.E.C.I.A.L",
                    value=f"{special['strength']} :muscle: | "
                          f"{special['perception']} :eye: | "
                          f"{special['endurance']} :person_running: | "
                          f"{special['charisma']} :superhero: | "
                          f"{special['intelligence']} :brain: | "
                          f"{special['agility']} :person_doing_cartwheel: | "
                          f"{special['luck']} :four_leaf_clover:")

    ef = {
        "file": file,
        "embed": embed
    }
    return ef


def embed_advs(ctx):
    adv_list = db_fight_get_adversary()
    embeds = []
    files = []
    colors = ('', 0x1abc9c, 0xe91e63, 0xf1c40f, 0xe74c3c)
    for adv in adv_list:
        special = db_fight_get_adversary_by_id_for_create(adv['id'], ctx.author.id)
        # file = discord.File(f"/home/container/battle/img/{adv['img']}", filename=adv['img'])
        file = discord.File(f"battle/img/{adv['img']}", filename=adv['img'])
        files.append(file)
        img = f"attachment://{adv['img']}"
        embed = discord.Embed(description=f">>> {special['pts']} pts / victoire", color=colors[adv['id']])
        embed.set_author(name=f"{adv['name']} ({adv['race']})", icon_url=f"{img}")
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
