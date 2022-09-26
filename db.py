import os
import sqlite3

LVL_PTS = {
    1: 0, 2: 4, 3: 3,
    4: 4, 5: 3, 6: 4,
    7: 3, 8: 4, 9: 3,
    10: 4
    # LVL_PTS[x]
}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect('shepard.db')
db.row_factory = dict_factory
c = db.cursor()


def db_connect():
    with open('sql/init.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    c.executescript(sql_script)


# Creer le membre dans la bdd et init toutes les tables necessaries
def db_create_user(user_id, user):
    user_obj = c.execute(f"SELECT 1 FROM user WHERE user_id = '{user_id}'")
    if user_obj.fetchone() is None:
        c.execute(f'''
            INSERT INTO user (user_id, user)
            VALUES ('{user_id}', '{user}');
        ''')
        c.execute(f'''
             INSERT INTO fight_player (user_id)
             VALUES ('{user_id}');
         ''')
        db.commit()


###################
#   BOT COMMAND   #
###################
def db_create_quote(user, quote):
    c.execute(f'''
        INSERT INTO quotes ( quote, user_name)
        VALUES ('{quote}', '{user}');
    ''')
    db.commit()


def db_get_quote():
    return c.execute('''
        SELECT * FROM quotes;
    ''').fetchall()


###################
#   BOT SHEPARD   #
###################

# retourne les informations du joueur
def db_fight_get_stats_by_user(user_id):
    return c.execute(f'''
        SELECT u.user as name, 
               fp.win as win, fp.loose as loose, fp.xp as xp,
               fl.name as rang, fl.lvl as lvl
        FROM user u
        JOIN fight_player fp ON u.user_id = fp.user_id
        JOIN fight_level fl ON fp.lvl = fl.lvl
        WHERE u.user_id = {user_id}
    ''').fetchone()


# retourne les info special pour la creation Fighter
def db_fight_get_user_special(user_id):
    return c.execute(f'''
            SELECT u.user AS name,
                fu.strength AS strength, fu.perception AS perception,
                fu.endurance AS endurance, fu.charisma AS charisma,
                fu.intelligence AS intelligence, fu.agility AS agility,
                fu.luck AS luck, fu.lvl AS lvl, fu.xp AS xp
            FROM user u
            JOIN fight_player fu ON u.user_id = fu.user_id
            WHERE u.user_id = {user_id}
        ''').fetchone()


# ajoute des points dans le special du joueur
def db_fight_special_add_pts(user_id, strength=0, perception=0, endurance=0, charisma=0, intelligence=0, agility=0, luck=0):
    # mets a jours le special
    c.execute(f''' 
        UPDATE fight_player
        SET strength = strength + {strength},
            perception = perception + {perception},
            endurance = endurance + {endurance},
            charisma = charisma + {charisma},
            intelligence = intelligence+ {intelligence},
            agility = agility + {agility},
            luck = luck + {luck}
        WHERE user_id = {int(user_id)}
    ''')
    db.commit()


# retourne les informations calculer pour la creation de l'objet Fighter
def db_fight_get_user_special_for_create_fighter(user_id):
    user = db_fight_get_user_special(user_id)
    special = db_fight_get_special_by_lvl(user['lvl'])
    s = 0 if (int(special['strength']) + int(user['strength'])) < 0 \
        else (int(special['strength']) + int(user['strength']))

    p = 0 if (int(special['perception']) + int(user['perception'])) < 0 \
        else (int(special['perception']) + int(user['perception']))

    e = 0 if (int(special['endurance']) + int(user['endurance'])) < 0 \
        else (int(special['endurance']) + int(user['endurance']))

    ch = 0 if (int(special['charisma']) + int(user['charisma'])) < 0 \
        else (int(special['charisma']) + int(user['charisma']))

    i = 0 if (int(special['intelligence']) + int(user['intelligence'])) < 0 \
        else (int(special['intelligence']) + int(user['intelligence']))

    a = 0 if (int(special['agility']) + int(user['agility'])) < 0 \
        else (int(special['agility']) + int(user['agility']))

    lu = 0 if (int(special['luck']) + int(user['luck'])) < 0 \
         else (int(special['luck']) + int(user['luck']))

    user_obj = {
        'name': user['name'],
        'lvl': user['lvl'],
        'strength': s,
        'perception': p,
        'endurance': e,
        'charisma': ch,
        'intelligence': i,
        'agility': a,
        'luck': lu,
        'xp': user['xp']
    }
    return user_obj


# retourne le lvl et l'xp total obtenir avec le jeu fight
# ('xp':0, 'lvl':1)
def db_fight_get_user_xp_lvl(user_id):
    return c.execute(f'''
        SELECT xp, lvl
        FROM fight_player
        WHERE user_id = {user_id}
    ''').fetchone()


def db_fight_win(user_id, xp=0):
    c.execute(f'''
        UPDATE fight_player
        SET win = win + 1,
            xp = xp + {xp}
        WHERE
            user_id = {user_id}
    ''')
    db.commit()
    
def db_fight_loose(user_id):
    c.execute(f'''
        UPDATE fight_player
        SET loose = loose + 1
        WHERE
            user_id = {user_id}
    ''')
    db.commit()
    
# retourne la liste des niveaux
def db_fight_get_level():
    return c.execute('''
        SELECT * FROM fight_level
        ORDER BY lvl ASC
    ''').fetchall()


# retourne un niveau par son numéro
def db_fight_get_level_by_lvl(lvl):
    return c.execute(f'''
        SELECT * FROM fight_level
        WHERE lvl = {lvl}
    ''').fetchone()


# retourne l'xp gagné par combat en fonction du niveau
def db_fight_level_get_xp_if_win(lvl):
    lvl_xp = c.execute(f'''
        SELECT total_xp as xp
        FROM fight_level
        WHERE lvl = {lvl}
    ''').fetchone()
    return lvl_xp['xp']


# retourne la liste des adv
def db_fight_get_adversary():
    return c.execute(f'''
        SELECT * FROM fight_adversary
        ORDER BY id ASC
    ''').fetchall()


# retourne un adv par son id
def db_fight_get_adversary_by_id(adv_id):
    return c.execute(f'''
        SELECT * FROM fight_adversary
        WHERE id = {adv_id}
    ''').fetchone()


# retourne l'adversaire avec son special calculé
# pour la creation de l'objet Fighter
def db_fight_get_adversary_by_id_for_create(adv_id, user_id):
    adv_select = db_fight_get_adversary_by_id(adv_id)
    user_lvl = db_fight_get_user_xp_lvl(user_id)
    special = db_fight_get_special_by_lvl(user_lvl['lvl'])
    xp_win = db_fight_level_get_xp_if_win(user_lvl['lvl'])

    s = 0 if (int(special['strength']) + int(adv_select['strength'])) < 0 \
        else (int(special['strength']) + int(adv_select['strength']))

    p = 0 if (int(special['perception']) + int(adv_select['perception'])) < 0 \
        else (int(special['perception']) + int(adv_select['perception']))

    e = 0 if (int(special['endurance']) + int(adv_select['endurance'])) < 0 \
        else (int(special['endurance']) + int(adv_select['endurance']))

    ch = 0 if (int(special['charisma']) + int(adv_select['charisma'])) < 0 \
        else (int(special['charisma']) + int(adv_select['charisma']))

    i = 0 if (int(special['intelligence']) + int(adv_select['intelligence'])) < 0 \
        else (int(special['intelligence']) + int(adv_select['intelligence']))

    a = 0 if (int(special['agility']) + int(adv_select['agility'])) < 0 \
        else (int(special['agility']) + int(adv_select['agility']))

    lu = 0 if (int(special['luck']) + int(adv_select['luck'])) < 0 \
        else (int(special['luck']) + int(adv_select['luck']))

    adv = {
        'name': adv_select['name'],
        'lvl': special['lvl'],
        'strength': s,
        'perception': p,
        'endurance': e,
        'charisma': ch,
        'intelligence': i,
        'agility': a,
        'luck': lu,
        'race': adv_select['race'],
        'xp_win': xp_win
    }
    # print(adv)
    return adv


# retourne la liste des special
def db_fight_get_special():
    return c.execute('''
        SELECT * FROM fight_special
    ''').fetchall()


# retourne special par son niveau(joueur ou adversaire)
def db_fight_get_special_by_lvl(lvl):
    return c.execute(f'''
        SELECT * FROM fight_special
        WHERE lvl = {lvl}
    ''').fetchone()
