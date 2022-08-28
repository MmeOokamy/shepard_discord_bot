--DROP TABLE IF EXISTS user;
--DROP TABLE IF EXISTS quotes;

--DROP TABLE IF EXISTS enemie;
--DROP TABLE IF EXISTS level;
--DROP TABLE IF EXISTS fight_stats;
--DROP TABLE IF EXISTS fight_special;

CREATE TABLE IF NOT EXISTS  user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    user_id INTEGER NOT NULL UNIQUE,
    score INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0
);


CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    user_name TEXT,
    since DATETIME
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


--INSERT INTO level
--VALUES (1, 1, 'Inoffensif', 50, '0, 50'),
--(2, 2, 'Novice', 100, '50, 150'),
--(3, 3, 'Compétent', 300, '150, 450'),
--(4, 4, 'Expert', 900, '450, 1350'),
--(5, 5, 'Létal', 2700, '1350,4050');



CREATE TABLE IF NOT EXISTS fight_stats (
    user_id INTEGER PRIMARY KEY UNIQUE,
    fight_win INTEGER DEFAULT 0,
    fight_loose INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS fight_special (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stats_name TEXT,
    stats_strenght INTEGER,
    stats_perception INTEGER,
    stats_endurance INTEGER,
    stats_charisma INTEGER,
    stats_intelligence INTEGER,
    stats_agility INTEGER,
    stats_luck INTEGER
);

-- INSERT INTO fight_special
-- VALUES  (1, '50', 2, 1, 2, 1, 1, 2, 1);
-- (2, '100', 3, 2, 3, 1, 1, 3, 2);
-- (3, '300', 3, 3, 4, 2, 1, 3, 3);
-- (4, '900', 4, 3, 6, 2, 1, 3, 3);
-- (5, '2700', 5, 3, 6, 2, 1, 3, 4);
-- (6, '4500', 5, 3, 6, 2, 1, 4, 4);
-- (7, '6300', 5, 3, 6, 2, 2, 4, 4);
-- (8, '8100', 5, 3, 6, 3, 2, 4, 4);
-- (9, '9900', 6, 3, 6, 3, 2, 4, 4);
-- (10, '11700', 8, 3, 6, 3, 2, 4, 4);