import os
import sqlite3

LVL_PTS = {
    1: 0,
    2: 4,
    3: 3,
    4: 4,
    5: 3,
    6: 4,
    7: 3,
    8: 4,
    9: 3,
    10: 4,
}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect("shepard.db")
db.row_factory = dict_factory
c = db.cursor()


def db_connect():
    with open("sql/init.sql", "r") as sql_file:
        sql_script = sql_file.read()
    c.executescript(sql_script)


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


###########################
# ###   BOT COMMAND   ### #
###########################
def db_create_quote(user, quote):
    c.execute(
        "INSERT INTO quotes (quote, user_name) VALUES (?, ?)",
        (quote, user),
    )
    db.commit()


def db_get_quote():
    return c.execute("SELECT * FROM quotes").fetchall()


###########################
# ###   BOT  BATTLE   ### #
###########################


###################
#  users/players  #
###################
def db_fight_podium():
    return c.execute(
        """
        SELECT u.user as user, fp.win AS partie_gagne, fp.xp as exp, fp.lvl as niveau,
        fp.strength + fs.strength AS force, fp.perception + fs.perception AS perception,
        fp.endurance + fs.endurance AS endurance, fp.charisma + fs.charisma AS charisme,
        fp.intelligence + fs.intelligence AS intelligence, fp.agility + fs.agility AS agility,
        fp.luck + fs.luck as luck
        FROM user u
        JOIN fight_player fp ON u.user_id = fp.user_id
        JOIN fight_special fs ON fp.lvl = fs.lvl
        ORDER BY fp.win DESC, fp.xp DESC, fp.lvl DESC
        """
    ).fetchall()


def db_fight_user_detail(player_id):
    return c.execute(
        """
        SELECT u.user as user, fp.win AS partie_gagne, fp.xp as xp, fp.lvl as niveau,
        fp.strength + fs.strength AS strength, fp.perception + fs.perception AS perception,
        fp.endurance + fs.endurance AS endurance, fp.charisma + fs.charisma AS charisma,
        fp.intelligence + fs.intelligence AS intelligence, fp.agility + fs.agility AS agility,
        fp.luck + fs.luck as luck
        FROM user u
        JOIN fight_player fp ON u.user_id = fp.user_id
        JOIN fight_special fs ON fp.lvl = fs.lvl
        WHERE u.user_id = ?
        """,
        (int(player_id),),
    ).fetchone()


###################
#   user/player   #
###################
def db_fight_get_stats_by_user(user_id):
    return c.execute(
        """
        SELECT u.user as name,
               fp.win as win, fp.loose as loose, fp.xp as xp,
               fl.name as rang, fl.lvl as lvl
        FROM user u
        JOIN fight_player fp ON u.user_id = fp.user_id
        JOIN fight_level fl ON fp.lvl = fl.lvl
        WHERE u.user_id = ?
        """,
        (user_id,),
    ).fetchone()


def db_fight_get_user_special(user_id):
    return c.execute(
        """
        SELECT u.user AS name,
            fu.strength AS strength, fu.perception AS perception,
            fu.endurance AS endurance, fu.charisma AS charisma,
            fu.intelligence AS intelligence, fu.agility AS agility,
            fu.luck AS luck, fu.lvl AS lvl, fu.xp AS xp
        FROM user u
        JOIN fight_player fu ON u.user_id = fu.user_id
        WHERE u.user_id = ?
        """,
        (user_id,),
    ).fetchone()


###################
#      STATS      #
###################
def db_fight_get_user_xp_lvl(user_id):
    return c.execute(
        "SELECT xp, lvl, win FROM fight_player WHERE user_id = ?",
        (user_id,),
    ).fetchone()


def db_fight_get_level():
    return c.execute("SELECT * FROM fight_level ORDER BY lvl ASC").fetchall()


def db_fight_get_level_by_lvl(lvl):
    return c.execute(
        "SELECT * FROM fight_level WHERE lvl = ?", (lvl,)
    ).fetchone()


def db_fight_level_get_xp_if_win(lvl):
    lvl_xp = c.execute(
        "SELECT pts FROM fight_level WHERE lvl = ?", (lvl,)
    ).fetchone()
    return lvl_xp["pts"] if lvl_xp else 0


###################
#   Adversaires   #
###################
def db_fight_get_adversary():
    return c.execute("SELECT * FROM fight_adversary ORDER BY id ASC").fetchall()


def db_fight_get_adversary_by_id(adv_id):
    return c.execute(
        "SELECT * FROM fight_adversary WHERE id = ?", (adv_id,)
    ).fetchone()


###################
#  S.P.E.C.I.A.L  #
###################

def db_fight_get_special():
    """Donne les informations de la table fight_special"""
    return c.execute("SELECT * FROM fight_special").fetchall()


def db_fight_get_special_by_lvl(lvl):
    """Donne le detail du special en fonction du lvl"""
    return c.execute(
        "SELECT * FROM fight_special WHERE lvl = ?", (lvl,)
    ).fetchone()


def db_fight_get_special_by_user(user_id):
    """Donne le special d'un membre"""
    return c.execute(
        """
        SELECT fs.strength AS strength, fs.perception AS perception,
                fs.endurance AS endurance, fs.charisma AS charisma,
                fs.intelligence AS intelligence, fs.agility AS agility,
                fs.luck AS luck, fp.lvl AS lvl
        FROM fight_special fs
        JOIN fight_player fp on fp.lvl = fs.lvl
        WHERE fp.user_id = ?
        """,
        (user_id,),
    ).fetchone()


def db_fight_special_add_pts(
    user_id,
    strength=0,
    perception=0,
    endurance=0,
    charisma=0,
    intelligence=0,
    agility=0,
    luck=0,
):
    """Fonction pour mettre à jour le SPECIAL du joueur"""
    c.execute(
        """
        UPDATE fight_player
        SET strength = strength + ?,
            perception = perception + ?,
            endurance = endurance + ?,
            charisma = charisma + ?,
            intelligence = intelligence + ?,
            agility = agility + ?,
            luck = luck + ?
        WHERE user_id = ?
        """,
        (strength, perception, endurance, charisma, intelligence, agility, luck, int(user_id)),
    )
    db.commit()


def _add_stat(a, b):
    return max(0, int(a) + int(b))


def db_fight_get_special_total(user_id, adv_id=0):
    """Donne le special du member ou de l'adversaire par rapport au niveau du member"""
    special = db_fight_get_special_by_user(user_id)
    player = db_fight_get_user_special(user_id) if adv_id == 0 else db_fight_get_adversary_by_id(adv_id)

    return {
        "name": player["name"],
        "lvl": special["lvl"],
        "strength": _add_stat(special["strength"], player["strength"]),
        "perception": _add_stat(special["perception"], player["perception"]),
        "endurance": _add_stat(special["endurance"], player["endurance"]),
        "charisma": _add_stat(special["charisma"], player["charisma"]),
        "intelligence": _add_stat(special["intelligence"], player["intelligence"]),
        "agility": _add_stat(special["agility"], player["agility"]),
        "luck": _add_stat(special["luck"], player["luck"]),
    }


def db_fight_get_user_special_for_create_fighter(user_id):
    """Donne les informations calculées pour la création de l'objet Fighter"""
    user = db_fight_get_user_special(user_id)
    special = db_fight_get_special_by_lvl(user["lvl"])

    return {
        "name": user["name"],
        "lvl": user["lvl"],
        "strength": _add_stat(special["strength"], user["strength"]),
        "perception": _add_stat(special["perception"], user["perception"]),
        "endurance": _add_stat(special["endurance"], user["endurance"]),
        "charisma": _add_stat(special["charisma"], user["charisma"]),
        "intelligence": _add_stat(special["intelligence"], user["intelligence"]),
        "agility": _add_stat(special["agility"], user["agility"]),
        "luck": _add_stat(special["luck"], user["luck"]),
        "xp": user["xp"],
    }


def db_fight_get_adversary_by_id_for_create(adv_id, user_id):
    adv_select = db_fight_get_adversary_by_id(adv_id)
    user_lvl = db_fight_get_user_xp_lvl(user_id)
    special = db_fight_get_special_by_lvl(user_lvl["lvl"])
    pts = db_fight_level_get_xp_if_win(user_lvl["lvl"])

    return {
        "name": adv_select["name"],
        "lvl": special["lvl"],
        "strength": _add_stat(special["strength"], adv_select["strength"]),
        "perception": _add_stat(special["perception"], adv_select["perception"]),
        "endurance": _add_stat(special["endurance"], adv_select["endurance"]),
        "charisma": _add_stat(special["charisma"], adv_select["charisma"]),
        "intelligence": _add_stat(special["intelligence"], adv_select["intelligence"]),
        "agility": _add_stat(special["agility"], adv_select["agility"]),
        "luck": _add_stat(special["luck"], adv_select["luck"]),
        "race": adv_select["race"],
        "pts": pts,
    }


###################
#      SCORES     #
###################
def db_fight_win(user_id, xp=0):
    c.execute(
        "UPDATE fight_player SET win = win + 1, xp = xp + ? WHERE user_id = ?",
        (xp, user_id),
    )
    db.commit()


def db_fight_loose(user_id):
    c.execute(
        "UPDATE fight_player SET loose = loose + 1 WHERE user_id = ?",
        (user_id,),
    )
    db.commit()
