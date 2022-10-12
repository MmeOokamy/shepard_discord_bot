# coding: utf-8
import os
import sys
import asyncio
import discord
from discord.ext import commands
from db import *  # sqlite execute fonction =)
from dotenv import load_dotenv

load_dotenv()


# Admin action
def is_me():
    def predicate(ctx):
        # 283935710858313730
        return ctx.message.author.id == int(os.getenv("ADMIN_ID"))

    return commands.check(predicate)


# action need data
def user_exist():
    def exist(ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        # regarde si l'user existe en bdd
        if db_user_exist(ctx.message.author.id) is False:
            # /!\ ajoute le nom du compte pas du discord à modif
            db_user_create(ctx.message.author.id, member.display_name)

        return db_user_exist(ctx.message.author.id)

    return commands.check(exist)


def member_details(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    print('member all')
    print("member.accent_colour")
    print(member.accent_colour)
    print("member.activities")
    print(member.activities)
    print("member.activity")
    print(member.activity)
    print("member.avatar")
    print(member.avatar)
    print("member.banner")
    print(member.banner)
    print("member.bot")
    print(member.bot)
    print("member.color")
    print(member.color)
    print("member.colour")
    print(member.colour)
    print("member.created_at")
    print(member.created_at)
    print("member.default_avatar")
    print(member.default_avatar)
    print("member.desktop_status")
    print(member.desktop_status)
    print("member.discriminator")
    print(member.discriminator)
    print("member.display_avatar")
    print(member.display_avatar)
    print("member.display_icon")
    print(member.display_icon)
    print("member.display_name")
    print(member.display_name)
    print("member.dm_channel")
    print(member.dm_channel)
    print("member.guild")
    print(member.guild)
    print("member.guild_avatar")
    print(member.guild_avatar)
    print("member.guild_permissions")
    print(member.guild_permissions)
    print("member.id")
    print(member.id)
    print("member.joined_at")
    print(member.joined_at)
    print("member.mention")
    print(member.mention)
    print("member.mobile_status")
    print(member.mobile_status)
    print("member.mutual_guilds")
    print(member.mutual_guilds)
    print("member.name")
    print(member.name)
    print("member.nick")
    print(member.nick)
    print("member.pending")
    print(member.pending)
    print("member.premium_since")
    print(member.premium_since)
    print("member.public_flags")
    print(member.public_flags)
    print("member.raw_status")
    print(member.raw_status)
    print("member.resolved_permissions")
    print(member.resolved_permissions)
    print("member.roles")
    print(member.roles)
    print("member.status")
    print(member.status)
    print("member.system")
    print(member.system)
    print("member.timed_out_until")
    print(member.timed_out_until)
    print("member.top_role")
    print(member.top_role)
    print("member.voice")
    print(member.voice)
    print("member.web_status")
    print(member.web_status)
