# coding: utf-8
import os
import sys
import asyncio
import discord
from discord.ext import commands
from db import *  # sqlite execute fonction =)
from dotenv import load_dotenv

load_dotenv()


def is_me():
    def predicate(ctx):
        # 283935710858313730
        return ctx.message.author.id == int(os.getenv("ADMIN_ID"))

    return commands.check(predicate)


async def db_create_user_if_exist(user_id, user_name):
    db_create_user(user_id, user_name)
