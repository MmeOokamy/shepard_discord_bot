--DROP TABLE IF EXISTS user;
--DROP TABLE IF EXISTS quotes;
--DROP TABLE IF EXISTS fight_level;
--DROP TABLE IF EXISTS fight_player;
--DROP TABLE IF EXISTS fight_adversary;
--DROP TABLE IF EXISTS fight_special;

-- USER TABLE
CREATE TABLE IF NOT EXISTS  user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    user_id INTEGER UNIQUE NOT NULL,
    score INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0
);

-- QUOTES TABLE
CREATE TABLE IF NOT EXISTS quotes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    user_name TEXT
);


-- FIGHT / BATTLE TABLES
CREATE TABLE IF NOT EXISTS fight_level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lvl INTEGER,
    name TEXT,
    pts INTEGER,
    total_xp INTEGER
);

-- INSERT INTO fight_level (id, lvl, name, pts, total_xp)
-- VALUES
-- (1, 1, 'Inoffensif', 3, 50),
-- (2, 2, 'Novice', 4, 100),
-- (3, 3, 'Compétent', 5, 300),
-- (4, 4, 'Expert', 6, 900),
-- (5, 5, 'Létal', 8, 2700);

CREATE TABLE IF NOT EXISTS fight_player (
    user_id INTEGER PRIMARY KEY UNIQUE,
    win INTEGER DEFAULT 0,
    loose INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    lvl INTEGER DEFAULT 1,
    strength INTEGER DEFAULT 1,
    perception INTEGER DEFAULT 1,
    endurance INTEGER DEFAULT 1,
    charisma INTEGER DEFAULT 1,
    intelligence INTEGER DEFAULT 1,
    agility INTEGER DEFAULT 1,
    luck INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS fight_adversary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    img TEXT,
    race TEXT,
    strength INTEGER DEFAULT 0,
    perception INTEGER DEFAULT 0,
    endurance INTEGER DEFAULT 0,
    charisma INTEGER DEFAULT 0,
    intelligence INTEGER DEFAULT 0,
    agility INTEGER DEFAULT 0,
    luck INTEGER DEFAULT 0
);

-- INSERT INTO fight_adversary (id, name, race, strength, perception, endurance, charisma, intelligence, agility, luck, img)
-- VALUES
-- (1, 'Wicket', 'Ewok', 0, 0, 0, 0, 0, 0, 0, 'wicket.png'),
-- (2, 'Fluttershy', 'Pegase', 2, 2, 2, 2, 2, 2, 2, 'flutter.png'),
-- (3, 'Grunt', 'Krogan', 2, 0, 2, 0, -1, -1, 0, 'grunt.png'),
-- (4, 'Commandant Shepard', 'Shepard', 5, 5, 5, 5, 5, 5, 5, 'shepard.png');

CREATE TABLE IF NOT EXISTS fight_special (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lvl INTEGER,
    strength INTEGER,
    perception INTEGER,
    endurance INTEGER,
    charisma INTEGER,
    intelligence INTEGER,
    agility INTEGER,
    luck INTEGER
);

-- INSERT INTO fight_special (id, lvl, strength, perception, endurance, charisma, intelligence, agility, luck)
-- VALUES  (1, 1, 2, 1, 2, 1, 1, 2, 1),
-- (2, 2, 3, 2, 3, 1, 1, 3, 2),
-- (3, 3, 3, 3, 4, 2, 1, 3, 3),
-- (4, 4, 4, 3, 6, 2, 1, 3, 3),
-- (5, 5, 5, 3, 6, 2, 1, 3, 4),
-- (6, 6, 5, 3, 6, 2, 1, 4, 4),
-- (7, 7, 5, 3, 6, 2, 2, 4, 4),
-- (8, 8, 5, 3, 6, 3, 2, 4, 4),
-- (9, 9, 6, 3, 6, 3, 2, 4, 4),
-- (10, 10, 8, 3, 6, 3, 2, 4, 4);