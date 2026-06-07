# coding: utf-8
"""Requêtes liées aux utilisateurs."""
from shepard.core.database import fetchone, get_db


async def db_user_exist(user_id):
    row = await fetchone("SELECT 1 FROM user WHERE user_id = ?", (user_id,))
    return row is not None


async def db_user_exist_return_id(user_id):
    user = await fetchone("SELECT user_id FROM user WHERE user_id = ?", (user_id,))
    if user is not None:
        return user["user_id"]


async def db_user_create(user_id, user_name):
    db = get_db()
    await db.execute(
        "INSERT INTO user (user_id, user) VALUES (?, ?)",
        (user_id, user_name),
    )
    await db.execute(
        "INSERT INTO fight_player (user_id) VALUES (?)",
        (user_id,),
    )
    await db.commit()
