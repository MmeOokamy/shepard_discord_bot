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
        c.execute(f'''
            INSERT INTO fight_user_level (user_id, ul_lvl, ul_pts, ul_used)
            VALUES ('{user_id}', 1, 0, 1)
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
def db_fight_get_user_special(user_id, ):
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


# ajoute des points dans le special du joueur
def db_fight_special_add_pts(user_id, strength=0, perception=0, endurance=0, charisma=0, intelligence=0, agility=0,
                             luck=0):
    user_id = int(user_id)
    # recuper le special initia
    infos = db_fight_get_user_special(user_id)
    # addition le spécial
    s = int(infos['strength']) + strength
    p = int(infos['perception']) + perception
    e = int(infos['endurance']) + endurance
    ch = int(infos['charisma']) + charisma
    i = int(infos['intelligence']) + intelligence
    a = int(infos['agility']) + agility
    lu = int(infos['luck']) + luck
    # mets a jours le special
    c.execute(f''' 
        UPDATE fight_user
        SET fight_strength={s},
            fight_perception={p},
            fight_endurance={e},
            fight_charisma={ch},
            fight_intelligence={i},
            fight_agility={a},
            fight_luck={lu}
        WHERE user_id = {user_id}
    ''')
    db.commit()


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

    ch = 0 if (int(special['stats_charisma']) + int(user['charisma'])) < 0 \
        else (int(special['stats_charisma']) + int(user['charisma']))

    i = 0 if (int(special['stats_intelligence']) + int(user['intelligence'])) < 0 \
        else (int(special['stats_intelligence']) + int(user['intelligence']))

    a = 0 if (int(special['stats_agility']) + int(user['agility'])) < 0 \
        else (int(special['stats_agility']) + int(user['agility']))

    lu = 0 if (int(special['stats_luck']) + int(user['luck'])) < 0 \
        else (int(special['stats_luck']) + int(user['luck']))

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
        SELECT fight_xp AS xp, fight_lvl AS lvl
        FROM fight_user
        WHERE user_id = {user_id}
    ''').fetchone()


def db_fight_add_score(user_id, win_or_loose=0, xp=0):
    fight = c.execute(f'''
        SELECT fight_win as win, fight_loose as loose, fight_xp as xp
        FROM fight_user
        WHERE user_id = {user_id}
    ''').fetchone()
    o_win = int(fight['win'])
    o_xp = int(fight['xp'])
    o_loose = int(fight['loose'])

    if int(win_or_loose) == 1:
        o_xp += xp
        o_win += 1
    elif int(win_or_loose) == 0:
        o_loose += 1

    c.execute(f'''
        UPDATE fight_user
        SET fight_win = {o_win},
            fight_loose = {o_loose},
            fight_xp = {o_xp}
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
            return fl


# retourne l'xp gagné par combat en fonction du niveau
def db_fight_level_get_xp_if_win(lvl):
    lvl_xp = c.execute(f'''
        SELECT lvl_xp
        FROM fight_level
        WHERE lvl_nb = {lvl}
    ''').fetchone()
    return lvl_xp['lvl_xp']


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

    s = 0 if (int(special['stats_strength']) + int(adv_select['adv_strength'])) < 0 \
        else (int(special['stats_strength']) + int(adv_select['adv_strength']))

    p = 0 if (int(special['stats_perception']) + int(adv_select['adv_perception'])) < 0 \
        else (int(special['stats_perception']) + int(adv_select['adv_perception']))

    e = 0 if (int(special['stats_endurance']) + int(adv_select['adv_endurance'])) < 0 \
        else (int(special['stats_endurance']) + int(adv_select['adv_endurance']))

    ch = 0 if (int(special['stats_charisma']) + int(adv_select['adv_charisma'])) < 0 \
        else (int(special['stats_charisma']) + int(adv_select['adv_charisma']))

    i = 0 if (int(special['stats_intelligence']) + int(adv_select['adv_intelligence'])) < 0 \
        else (int(special['stats_intelligence']) + int(adv_select['adv_intelligence']))

    a = 0 if (int(special['stats_agility']) + int(adv_select['adv_agility'])) < 0 \
        else (int(special['stats_agility']) + int(adv_select['adv_agility']))

    lu = 0 if (int(special['stats_luck']) + int(adv_select['adv_luck'])) < 0 \
        else (int(special['stats_luck']) + int(adv_select['adv_luck']))

    adv = {
        'name': adv_select['adv_name'],
        'lvl': special['stats_lvl'],
        'strength': s,
        'perception': p,
        'endurance': e,
        'charisma': ch,
        'intelligence': i,
        'agility': a,
        'luck': lu,
        'race': adv_select['adv_race'],
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
        WHERE stats_lvl = {lvl}
    ''').fetchone()


# regarde si l'utilisateur passe au niveau sup
def db_fight_lvl_up_or_not(user_id):
    xp_lvl = db_fight_get_user_xp_lvl(user_id)
    print(xp_lvl)
    if xp_lvl is not None:
        xp, lvl = xp_lvl['xp'], xp_lvl['lvl']
        detail_lvl = db_fight_get_level_by_lvl(lvl)
        if xp in range(detail_lvl['lvl_gap_down'], detail_lvl['lvl_gap_up']):
            check = False
        else:
            check = True

    else:
        check = 2
    return check


def db_fight_lvl_up_user(user_id):
    pass
    # fight_user lvl +=1
    # retourne le nombre de point a attribuer dans le spécial
    # fight_user special += lvl_special_pts
