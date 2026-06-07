# coding: utf-8
"""Singleton SQLite : la connexion et le curseur sont créés à l'import."""
import sqlite3

from shepard.config import DB_PATH, INIT_SQL_PATH


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


db = sqlite3.connect(DB_PATH)
db.row_factory = dict_factory
c = db.cursor()


def db_connect():
    """Initialise le schéma à partir de sql/init.sql (CREATE TABLE IF NOT EXISTS)."""
    with open(INIT_SQL_PATH, "r") as sql_file:
        c.executescript(sql_file.read())
