# coding: utf-8
import os
import sys
import subprocess
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


def check_service_status(service_name):
    """Vérifie l'état d'un service systemd."""
    try:
        # Exécute la commande systemctl
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Retourne True si le service est actif
        return result.stdout.strip() == "active"
    except Exception:
        return False
