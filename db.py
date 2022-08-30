import os
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect('shepard.db')
db.row_factory = dict_factory
c = db.cursor()


def db_connect():
    with open('init.sql', 'r') as sql_file:
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
             INSERT INTO fight_user (user_id)
             VALUES ('{user_id}');
         ''')
        db.commit()


###################
#   BOT COMMAND   #
###################
def db_create_quote(user, quote):
    c.execute(f'''
        INSERT INTO quotes ( quote, user_name, since)
        VALUES ('{quote}', '{user}', DateTime('now'));
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
               fu.fight_win as win, fu.fight_loose as loose, fu.fight_xp as f_xp,
               fl.lvl_name as rang, fl.lvl_nb as lvl
        FROM user u
        JOIN fight_user fu ON u.user_id = fu.user_id
        JOIN fight_level fl ON fu.fight_lvl = fl.lvl_nb
        WHERE u.user_id = {user_id}
    ''').fetchone()


# retourne les info special pour la creation Fighter
def db_fight_get_user_special(user_id):
    return c.execute(f'''
            SELECT u.user AS name,
                fu.fight_strength AS strength, fu.fight_perception AS perception,
                fu.fight_endurance AS endurance, fu.fight_charisma AS charisma,
                fu.fight_intelligence AS intelligence, fu.fight_agility AS agility,
                fu.fight_luck AS luck, fu.fight_lvl AS lvl, fu.fight_xp AS xp
            FROM user u
            JOIN fight_user fu ON u.user_id = fu.user_id
            WHERE u.user_id = {user_id}
        ''').fetchone()


# retourne les informations calculer pour la creation de l'objet Fighter
def db_fight_get_user_special_for_create_fighter(user_id):
    user = db_fight_get_user_special(user_id)
    special = db_fight_get_special_by_lvl(user['lvl'])
    s = 0 if (int(special['stats_strength']) + int(user['strength'])) < 0 \
        else (int(special['stats_strength']) + int(user['strength']))

    p = 0 if (int(special['stats_perception']) + int(user['perception'])) < 0 \
        else (int(special['stats_perception']) + int(user['perception']))

    e = 0 if (int(special['stats_endurance']) + int(user['endurance'])) < 0 \
        else (int(special['stats_endurance']) + int(user['endurance']))

    c = 0 if (int(special['stats_charisma']) + int(user['charisma'])) < 0 \
        else (int(special['stats_charisma']) + int(user['charisma']))

    i = 0 if (int(special['stats_intelligence']) + int(user['intelligence'])) < 0 \
        else (int(special['stats_intelligence']) + int(user['intelligence']))

    a = 0 if (int(special['stats_agility']) + int(user['agility'])) < 0 \
        else (int(special['stats_agility']) + int(user['agility']))

    l = 0 if (int(special['stats_luck']) + int(user['luck'])) < 0 \
        else (int(special['stats_luck']) + int(user['luck']))

    user_obj = {
        'name': user['name'],
        'lvl': user['lvl'],
        'strength': s,
        'perception': p,
        'endurance': e,
        'charisma': c,
        'intelligence': i,
        'agility': a,
        'luck': l,
        'xp': user['xp']
    }
    return user_obj


# retourne le lvl et l'xp total obtenir avec le jeu fight
# ('xp':0, 'lvl':1)
def db_fight_get_user_xp_lvl(user_id):
    return c.execute(f'''
        SELECT fight_xp AS xp, fight_lvl AS lvl
        FROM fight_user
        WHERE user_id = {user_id}
    ''').fetchone()


def db_fight_add_score(user_id, win_or_loose, xp=0):
    fight = c.execute(f"SELECT * FROM fight_user WHERE user_id = '{user_id}'").fetchone()
    fight_win = int(fight['fight_win'])
    fight_xp = int(fight['fight_xp'])
    fight_loose = int(fight['fight_loose'])

    if int(win_or_loose) == 1:
        # print('gagné')
        fight_win += 1
        fight_xp += xp
    elif int(win_or_loose) == 0:
        # print('perdu')
        fight_loose += 1

    c.execute(f'''
        UPDATE fight_user
        SET fight_win = {fight_win},
            fight_loose = {fight_loose},
            fight_xp = {fight_xp}
        WHERE
            user_id = {user_id}
        LIMIT 1
    ''')
    db.commit()


# retourne la liste des niveaux
def db_fight_get_level():
    return c.execute('''
        SELECT * FROM fight_level
        ORDER BY lvl_nb ASC
    ''').fetchall()


# retourne un niveau par son numéro
def db_fight_get_level_by_lvl(lvl_nb):
    return c.execute(f'''
        SELECT * FROM fight_level
        WHERE lvl_nb = {lvl_nb}
    ''').fetchone()


# retourne un niveau en fonction du nombre d'xp que le user possede
def db_fight_get_level_by_gap(user_xp):
    fight_level_all = db_fight_get_level()
    for fl in fight_level_all:
        if fl['lvl_gap_down'] <= user_xp < fl['lvl_gap_up']:
            print(fl)
            return fl


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

    s = 0 if (int(special['stats_strength']) + int(adv_select['adv_strength'])) < 0 \
        else (int(special['stats_strength']) + int(adv_select['adv_strength']))

    p = 0 if (int(special['stats_perception']) + int(adv_select['adv_perception'])) < 0 \
        else (int(special['stats_perception']) + int(adv_select['adv_perception']))

    e = 0 if (int(special['stats_endurance']) + int(adv_select['adv_endurance'])) < 0 \
        else (int(special['stats_endurance']) + int(adv_select['adv_endurance']))

    c = 0 if (int(special['stats_charisma']) + int(adv_select['adv_charisma'])) < 0 \
        else (int(special['stats_charisma']) + int(adv_select['adv_charisma']))

    i = 0 if (int(special['stats_intelligence']) + int(adv_select['adv_intelligence'])) < 0 \
        else (int(special['stats_intelligence']) + int(adv_select['adv_intelligence']))

    a = 0 if (int(special['stats_agility']) + int(adv_select['adv_agility'])) < 0 \
        else (int(special['stats_agility']) + int(adv_select['adv_agility']))

    l = 0 if (int(special['stats_luck']) + int(adv_select['adv_luck'])) < 0 \
        else (int(special['stats_luck']) + int(adv_select['adv_luck']))

    adv = {
        'name': adv_select['adv_name'],
        'lvl': special['stats_lvl'],
        'strength': s,
        'perception': p,
        'endurance': e,
        'charisma': c,
        'intelligence': i,
        'agility': a,
        'luck': l,
        'race': adv_select['adv_race']
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
        WHERE stats_lvl = {lvl}
    ''').fetchone()
