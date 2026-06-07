# coding: utf-8
"""Requêtes liées aux quotes."""
from shepard.core.database import db, c


def db_create_quote(user, quote):
    c.execute(
        "INSERT INTO quotes (quote, user_name) VALUES (?, ?)",
        (quote, user),
    )
    db.commit()


def db_get_quote():
    return c.execute("SELECT * FROM quotes").fetchall()
