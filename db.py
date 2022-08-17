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


def db_create_user(user_id, user):
    user_obj = c.execute(f"SELECT 1 FROM user WHERE user_id = '{user_id}'")
    response = 0
    if user_obj.fetchone() is None:
        c.execute(f'''
            INSERT INTO user (user_id, user)
            VALUES ('{user_id}', '{user}');
        ''')
        c.execute(f'''
             INSERT INTO fight (user_id)
             VALUES ('{user_id}');
         ''')
        db.commit()
        response = 1
    return response


def db_fight_add_score(user_id, win_or_loose):
    fight_obj = c.execute(f"SELECT * FROM fight WHERE user_id = '{user_id}'")
    fight = fight_obj.fetchone()
    fight_win = int(fight['fight_win'])
    fight_loose = int(fight['fight_loose'])
    if int(win_or_loose) == 1:
        # print('gagné')
        fight_win += 1
    elif int(win_or_loose) == 0:
        # print('perdu')
        fight_loose += 1

    c.execute(f'''
        UPDATE fight
        SET fight_win = {fight_win},
            fight_loose = {fight_loose}
        WHERE
            user_id = {user_id}
        LIMIT 1

    ''')
    db.commit()


def db_fight_user_stats(user_id):
    return c.execute(f"SELECT * FROM fight WHERE user_id = '{user_id}'").fetchone()


def db_user_stats(user_id):
    return c.execute(f'''
        SELECT u.user, u.user_id, u.score, u.xp, f.fight_win, f.fight_loose
        FROM user u
        JOIN fight f on f.user_id = u.user_id
        WHERE u.user_id = {user_id}
    ''').fetchone()



