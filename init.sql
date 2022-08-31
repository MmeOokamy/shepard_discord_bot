--DROP TABLE IF EXISTS user;
--DROP TABLE IF EXISTS quotes;
--DROP TABLE IF EXISTS fight_user;
--DROP TABLE IF EXISTS fight_level;
--DROP TABLE IF EXISTS fight_adversary;
--DROP TABLE IF EXISTS fight_special;

CREATE TABLE IF NOT EXISTS  user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    user_id INTEGER UNIQUE NOT NULL,
    score INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0
);


CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    user_name TEXT
);

CREATE TABLE IF NOT EXISTS fight_level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lvl_nb INTEGER,
    lvl_name TEXT,
    lvl_xp INTEGER,
    lvl_xp_for_up INTEGER,
    lvl_gap_down INTEGER,
    lvl_gap_up INTEGER
);


CREATE TABLE IF NOT EXISTS fight_user (
    user_id INTEGER PRIMARY KEY UNIQUE,
    fight_win INTEGER DEFAULT 0,
    fight_loose INTEGER DEFAULT 0,
    fight_xp INTEGER DEFAULT 0,
    fight_lvl INTEGER DEFAULT 1,
    fight_strength INTEGER DEFAULT 1,
    fight_perception INTEGER DEFAULT 1,
    fight_endurance INTEGER DEFAULT 1,
    fight_charisma INTEGER DEFAULT 1,
    fight_intelligence INTEGER DEFAULT 1,
    fight_agility INTEGER DEFAULT 1,
    fight_luck INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS fight_adversary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adv_name TEXT,
    adv_race TEXT,
    adv_lvl TEXT,
    adv_strength INTEGER DEFAULT 0,
    adv_perception INTEGER DEFAULT 0,
    adv_endurance INTEGER DEFAULT 0,
    adv_charisma INTEGER DEFAULT 0,
    adv_intelligence INTEGER DEFAULT 0,
    adv_agility INTEGER DEFAULT 0,
    adv_luck INTEGER DEFAULT 0
);



CREATE TABLE IF NOT EXISTS fight_special (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stats_lvl INTEGER,
    stats_strength INTEGER,
    stats_perception INTEGER,
    stats_endurance INTEGER,
    stats_charisma INTEGER,
    stats_intelligence INTEGER,
    stats_agility INTEGER,
    stats_luck INTEGER
);


--INSERT INTO fight_level (lvl_nb, lvl_name, lvl_xp, lvl_xp_for_up, lvl_gap_down, lvl_gap_up)
--VALUES
--(1, 'Inoffensif', 3, 50, 0,50),
--(2, 'Novice', 3, 100, 50,150),
--(3, 'Compétent', 3, 300, 150,450),
--(4, 'Expert', 3, 900, 450,1350),
--(5, 'Létal', 3, 2700, 1350,4050);
--
--INSERT INTO fight_adversary (adv_name, adv_race, adv_lvl, adv_strength, adv_perception, adv_endurance, adv_charisma, adv_intelligence, adv_agility, adv_luck)
--VALUES
--('Wicket', 'Ewok','0,1,2', 0, 0, 0, 0, 0, 0, 0),
--('Fluttershy', 'Pegase','0,1,2', 2, 2, 2, 2, 2, 2, 2),
--('Grunt', 'Krogan','1,2,3', 2, 0, 2, 0, -1, -1, 0),
--('Commandant Shepard', 'Shepard','9,10', 5, 5, 5, 5, 5, 5, 5);
--
-- INSERT INTO fight_special (stats_lvl,stats_strength,stats_perception,stats_endurance,stats_charisma,stats_intelligence,stats_agility,stats_luck)
-- VALUES  (1, 2, 1, 2, 1, 1, 2, 1),
-- (2, 3, 2, 3, 1, 1, 3, 2),
-- (3, 3, 3, 4, 2, 1, 3, 3),
-- (4, 4, 3, 6, 2, 1, 3, 3),
-- (5, 5, 3, 6, 2, 1, 3, 4),
-- (6, 5, 3, 6, 2, 1, 4, 4),
-- (7, 5, 3, 6, 2, 2, 4, 4),
-- (8, 5, 3, 6, 3, 2, 4, 4),
-- (9, 6, 3, 6, 3, 2, 4, 4),
-- (10, 8, 3, 6, 3, 2, 4, 4);