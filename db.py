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


def db_user_exist(user_id):
    return False if c.execute(f"SELECT 1 FROM user WHERE user_id = '{user_id}'").fetchone() is None else True


def db_user_exist_return_id(user_id):
    user = c.execute(f"SELECT user_id FROM user WHERE user_id = '{user_id}'").fetchone()
    if user is not None:
        return user['id']


def db_user_create(user_id, user_name):
    c.execute(f'''
        INSERT INTO user (user_id, user)
        VALUES ('{user_id}', '{user_name}');
    ''')
    c.execute(f'''
         INSERT INTO fight_player (user_id)
         VALUES ('{user_id}');
     ''')
    db.commit()


###########################
# ###   BOT COMMAND   ### #
###########################
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


###########################
# ###   BOT  BATTLE   ### #
###########################

###################
#  users/players  #
###################
def db_fight_podium():
    return c.execute(f'''
                     SELECT u.user as user, fp.win AS partie_gagne, fp.xp as exp, fp.lvl as niveau, 
                     fp.strength + fs.strength AS force, fp.perception + fs.perception AS perception, 
                     fp.endurance + fs.endurance AS endurance, fp.charisma + fs.charisma AS charisme, 
                     fp.intelligence + fs.intelligence AS intelligence, fp.agility + fs.agility AS agility, 
                     fp.luck + fs.luck as luck 
                     FROM user u
                     JOIN fight_player fp ON u.user_id = fp.user_id
                     JOIN fight_special fs ON fp.lvl = fs.lvl
                     ORDER BY fp.win DESC, fp.xp DESC, fp.lvl DESC;
                     ''').fetchall()


def db_fight_user_detail(player_id):
    return c.execute(f'''
                     SELECT u.user as user, fp.win AS partie_gagne, fp.xp as xp, fp.lvl as niveau, 
                     fp.strength + fs.strength AS strength, fp.perception + fs.perception AS perception, 
                     fp.endurance + fs.endurance AS endurance, fp.charisma + fs.charisma AS charisma, 
                     fp.intelligence + fs.intelligence AS intelligence, fp.agility + fs.agility AS agility, 
                     fp.luck + fs.luck as luck 
                     FROM user u
                     JOIN fight_player fp ON u.user_id = fp.user_id
                     JOIN fight_special fs ON fp.lvl = fs.lvl
                     WHERE u.user_id = {int(player_id)};
                     ''').fetchone()


###################
#   user/player   #
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


# retourne toutes les infos + special
def db_fight_user_get_all_info(user_id):
    return c.execute(f'''
            SELECT u.user AS name,
                fu.strength AS strength, fu.perception AS perception,
                fu.endurance AS endurance, fu.charisma AS charisma,
                fu.intelligence AS intelligence, fu.agility AS agility,
                fu.luck AS luck, fu.lvl AS lvl, fu.xp AS xp
            FROM user u
            JOIN fight_player fu ON u.user_id = fu.user_id
            JOIN fight_level fl ON fp.lvl = fl.lvl
            WHERE u.user_id = {user_id}
        ''').fetchone()


###################
#      STATS      #
###################
# retourne le lvl et l'xp total obtenir avec le jeu fight
# ('xp':0, 'lvl':1)
def db_fight_get_user_xp_lvl(user_id):
    return c.execute(f'''
        SELECT xp, lvl, win
        FROM fight_player
        WHERE user_id = {user_id}
    ''').fetchone()


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
        SELECT pts
        FROM fight_level
        WHERE lvl = {lvl}
    ''').fetchone()
    return lvl_xp['pts']


###################
#   Adversaires   #
###################
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


###################
#  S.P.E.C.I.A.L  #
###################

def db_fight_get_special():
    """ Donne les informations de la table fight_special
    Returns:
        List: id, lvl, strength, perception, endurance,
                  charisma, intelligence, agility, luck
    """    
    return c.execute('''
        SELECT * FROM fight_special
    ''').fetchall()


def db_fight_get_special_by_lvl(lvl):
    """ donne le detail du special en fonction du lvl

    Args:
        lvl (int): niveau 

    Returns:
        Dict: id, lvl, strength, perception, endurance,
                  charisma, intelligence, agility, luck
    """
    return c.execute(f'''
        SELECT * FROM fight_special
        WHERE lvl = {lvl}
    ''').fetchone()


def db_fight_get_special_by_user(user_id):
    """ donne le special d'un membre

    Args:
        user_id (int): discord member.id 

    Returns:
        Dict: strength, perception, endurance, charisma, 
                intelligence, agility, luck,
                lvl
    """
    return c.execute(f'''
        SELECT fs.strength AS strength, fs.perception AS perception,
                fs.endurance AS endurance, fs.charisma AS charisma,
                fs.intelligence AS intelligence, fs.agility AS agility,
                fs.luck AS luck, fp.lvl AS lvl
        FROM fight_special fs
        JOIN fight_player fp on fp.lvl = fs.lvl
        WHERE fp.user_id = {user_id}
    ''').fetchone()



def db_fight_special_add_pts(user_id, strength=0, perception=0, endurance=0, charisma=0, intelligence=0, agility=0, luck=0):
    """ Fonction pour mettre à jour le SPECIAL du joueur

    Args:
        user_id (int): discord member.id
        strength (int, optional): strength - force. Defaults to 0.
        perception (int, optional): perception. Defaults to 0.
        endurance (int, optional): endurance. Defaults to 0.
        charisma (int, optional): charisma. Defaults to 0.
        intelligence (int, optional): intelligence. Defaults to 0.
        agility (int, optional): agility. Defaults to 0.
        luck (int, optional): luck - chance. Defaults to 0.
    """
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


def db_fight_get_special_total(user_id, adv_id=0):
    """ Donne le special du member ou de l'adversaire 
        par rapport au niveau du member

    Args:
        user_id (int): discord member.id
        adv_id (int, optional): id de l'adversaire. Defaults to 0.

    Returns:
        Dict: name, lvl, strength, perception, endurance,
              charisma, intelligence, agility, luck
    """
    special = db_fight_get_special_by_user(user_id)
    if adv_id == 0:
        player = db_fight_get_user_special(user_id)
        # {'name': 'Ookamy', 'strength': 1, 'perception': 1, 'endurance': 1, 'charisma': 1, 'intelligence': 1,
        # 'agility': 1, 'luck': 1, 'lvl': 1, 'xp': 9}
    else:
        player = db_fight_get_adversary_by_id(adv_id)
        # {'id': 4, 'name': 'Commandant Shepard', 'img': 'shepard.png', 'race': 'Shepard', 'strength': 5,
        # 'perception': 5, 'endurance': 5, 'charisma': 5, 'intelligence': 5, 'agility': 5, 'luck': 5}
    s = 0 if (int(special['strength']) + int(player['strength'])) < 0 \
        else (int(special['strength']) + int(player['strength']))

    p = 0 if (int(special['perception']) + int(player['perception'])) < 0 \
        else (int(special['perception']) + int(player['perception']))

    e = 0 if (int(special['endurance']) + int(player['endurance'])) < 0 \
        else (int(special['endurance']) + int(player['endurance']))

    ch = 0 if (int(special['charisma']) + int(player['charisma'])) < 0 \
        else (int(special['charisma']) + int(player['charisma']))

    i = 0 if (int(special['intelligence']) + int(player['intelligence'])) < 0 \
        else (int(special['intelligence']) + int(player['intelligence']))

    a = 0 if (int(special['agility']) + int(player['agility'])) < 0 \
        else (int(special['agility']) + int(player['agility']))

    lu = 0 if (int(special['luck']) + int(player['luck'])) < 0 \
        else (int(special['luck']) + int(player['luck']))

    special = {
        'name': player['name'],
        'lvl': special['lvl'],
        'strength': s,
        'perception': p,
        'endurance': e,
        'charisma': ch,
        'intelligence': i,
        'agility': a,
        'luck': lu
    }
    return special



def db_fight_get_user_special_for_create_fighter(user_id):
    """ Donne les informations calculer pour la création de l'objet Fighter

    Args:
        user_id (int): discord member.id

    Returns:
        Dict: destinée à la création de l'obj Fighter
    """
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


# retourne l'adversaire avec son special calculé
# pour la creation de l'objet Fighter
def db_fight_get_adversary_by_id_for_create(adv_id, user_id):
    adv_select = db_fight_get_adversary_by_id(adv_id)
    user_lvl = db_fight_get_user_xp_lvl(user_id)
    special = db_fight_get_special_by_lvl(user_lvl['lvl'])
    pts = db_fight_level_get_xp_if_win(user_lvl['lvl'])

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
        'pts': pts
    }
    # print(f"db_fight_get_adversary_by_id_for_create  :{adv}")
    return adv


###################
#      SCORES     #
###################
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
