# coding: utf-8
"""Décorateurs de vérification pour les commandes."""
import discord
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
    def exist(ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if db_user_exist(ctx.message.author.id) is False:
            db_user_create(ctx.message.author.id, member.display_name)

        return db_user_exist(ctx.message.author.id)

    return commands.check(exist)
