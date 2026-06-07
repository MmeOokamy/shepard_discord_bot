# coding: utf-8
"""Requêtes liées aux utilisateurs."""
from shepard.core.database import db, c


def db_user_exist(user_id):
    return c.execute(
        "SELECT 1 FROM user WHERE user_id = ?", (user_id,)
    ).fetchone() is not None


def db_user_exist_return_id(user_id):
    user = c.execute(
        "SELECT user_id FROM user WHERE user_id = ?", (user_id,)
    ).fetchone()
    if user is not None:
        return user["user_id"]


def db_user_create(user_id, user_name):
    c.execute(
        "INSERT INTO user (user_id, user) VALUES (?, ?)",
        (user_id, user_name),
    )
    c.execute(
        "INSERT INTO fight_player (user_id) VALUES (?)",
        (user_id,),
    )
    db.commit()
