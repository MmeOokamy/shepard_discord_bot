# coding: utf-8
"""Décorateurs de vérification pour les commandes."""
from discord.ext import commands

from shepard.config import ADMIN_ID
from shepard.db.users import db_user_exist, db_user_create


def is_me():
    """Restreint une commande au propriétaire (ADMIN_ID)."""
    def predicate(ctx):
        return ctx.message.author.id == ADMIN_ID

    return commands.check(predicate)


def user_exist():
    """Crée l'utilisateur en base à la première utilisation si besoin."""
    async def exist(ctx):
        if await db_user_exist(ctx.message.author.id) is False:
            await db_user_create(ctx.message.author.id, ctx.author.display_name)

        return await db_user_exist(ctx.message.author.id)

    return commands.check(exist)
