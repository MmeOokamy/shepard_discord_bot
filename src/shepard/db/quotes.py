# coding: utf-8
"""Requêtes liées aux quotes."""
from shepard.core.database import execute, fetchall


async def db_create_quote(user, quote):
    await execute(
        "INSERT INTO quotes (quote, user_name) VALUES (?, ?)",
        (quote, user),
    )


async def db_get_quote():
    return await fetchall("SELECT * FROM quotes")
