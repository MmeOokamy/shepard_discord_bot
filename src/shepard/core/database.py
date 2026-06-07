# coding: utf-8
"""Connexion SQLite asynchrone (aiosqlite), initialisée au démarrage via connect()."""
import aiosqlite

from shepard.config import DB_PATH, INIT_SQL_PATH

_db = None


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Retourne la connexion ouverte. Lève si connect() n'a pas été appelé."""
    if _db is None:
        raise RuntimeError(
            "Base de données non initialisée : appeler connect() au démarrage."
        )
    return _db


async def connect():
    """Ouvre la connexion et initialise le schéma (sql/init.sql)."""
    global _db
    _db = await aiosqlite.connect(DB_PATH)
    _db.row_factory = dict_factory
    with open(INIT_SQL_PATH, "r") as sql_file:
        await _db.executescript(sql_file.read())
    await _db.commit()
    return _db


async def close():
    """Ferme la connexion (à appeler à l'arrêt du bot)."""
    global _db
    if _db is not None:
        await _db.close()
        _db = None


# --- Helpers de requête ---
async def fetchone(query, params=()):
    async with get_db().execute(query, params) as cur:
        return await cur.fetchone()


async def fetchall(query, params=()):
    async with get_db().execute(query, params) as cur:
        return await cur.fetchall()


async def execute(query, params=()):
    """Exécute une requête d'écriture et commit."""
    db = get_db()
    await db.execute(query, params)
    await db.commit()
