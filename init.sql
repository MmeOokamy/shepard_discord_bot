--DROP TABLE IF EXISTS user;
--DROP TABLE IF EXISTS fight;
--DROP TABLE IF EXISTS enemie;
--DROP TABLE IF EXISTS level;
--DROP TABLE IF EXISTS quotes;

CREATE TABLE IF NOT EXISTS  user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    user_id INTEGER NOT NULL UNIQUE,
    score INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fight (
    user_id INTEGER PRIMARY KEY UNIQUE,
    fight_win INTEGER DEFAULT 0,
    fight_loose INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS enemie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enemie_name TEXT,
    enemie_lvl INTEGER,
    enemie_strenght INTEGER,
    enemie_perception INTEGER,
    enemie_endurance INTEGER,
    enemie_charisma INTEGER,
    enemie_intelligence INTEGER,
    enemie_agility INTEGER,
    enemie_luck INTEGER
);


CREATE TABLE IF NOT EXISTS level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lvl_nb INTEGER,
    lvl_name TEXT,
    lvl_xp INTEGER,
    lvl_gap TEXT
);


CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    user_name TEXT,
    since DATETIME
);


--INSERT INTO level
--VALUES (1, 1, 'Inoffensif', 50, '0, 50'),
--(2, 2, 'Novice', 100, '50, 150'),
--(3, 3, 'Compétent', 300, '150, 450'),
--(4, 4, 'Expert', 900, '450, 1350'),
--(5, 5, 'Létal', 2700, '1350,4050');

--INSERT INTO enemie
--VALUES (1, 'Grunt',1,1,1,1,1,1,1,1);