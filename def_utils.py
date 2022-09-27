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
    def exist(ctx):
        # regarde si l'user existe en bdd
        if db_user_exist(ctx.message.author.id) is False:
            db_user_create(ctx.message.author.id, ctx.message.author.name)

        return db_user_exist(ctx.message.author.id)

    return commands.check(exist)
