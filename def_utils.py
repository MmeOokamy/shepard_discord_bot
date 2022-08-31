# coding: utf-8
import os
import sys
import asyncio
import discord
from discord.ext import commands
from db import *  # sqlite execute fonction =)


def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 283935710858313730

    return commands.check(predicate)


async def db_create_user_if_exist(user_id, user_name):
    db_create_user(user_id, user_name)
