BEGIN TRANSACTION;
DROP TABLE IF EXISTS "user";
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"user"	TEXT,
	"user_id"	INTEGER NOT NULL UNIQUE,
	"score"	INTEGER DEFAULT 0,
	"xp"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "quotes";
CREATE TABLE IF NOT EXISTS "quotes" (
	"id"	INTEGER,
	"quote"	TEXT,
	"user_name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "fight_level";
CREATE TABLE IF NOT EXISTS "fight_level" (
	"id"	INTEGER,
	"lvl"	INTEGER,
	"name"	TEXT,
	"pts"	INTEGER,
	"total_xp"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "fight_player";
CREATE TABLE IF NOT EXISTS "fight_player" (
	"user_id"	INTEGER UNIQUE,
	"win"	INTEGER DEFAULT 0,
	"loose"	INTEGER DEFAULT 0,
	"xp"	INTEGER DEFAULT 0,
	"lvl"	INTEGER DEFAULT 1,
	"strength"	INTEGER DEFAULT 1,
	"perception"	INTEGER DEFAULT 1,
	"endurance"	INTEGER DEFAULT 1,
	"charisma"	INTEGER DEFAULT 1,
	"intelligence"	INTEGER DEFAULT 1,
	"agility"	INTEGER DEFAULT 1,
	"luck"	INTEGER DEFAULT 1,
	PRIMARY KEY("user_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("user_id")
);
DROP TABLE IF EXISTS "fight_adversary";
CREATE TABLE IF NOT EXISTS "fight_adversary" (
	"id"	INTEGER,
	"name"	TEXT,
	"img"	TEXT,
	"race"	TEXT,
	"strength"	INTEGER DEFAULT 0,
	"perception"	INTEGER DEFAULT 0,
	"endurance"	INTEGER DEFAULT 0,
	"charisma"	INTEGER DEFAULT 0,
	"intelligence"	INTEGER DEFAULT 0,
	"agility"	INTEGER DEFAULT 0,
	"luck"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "fight_special";
CREATE TABLE IF NOT EXISTS "fight_special" (
	"id"	INTEGER,
	"lvl"	INTEGER,
	"strength"	INTEGER,
	"perception"	INTEGER,
	"endurance"	INTEGER,
	"charisma"	INTEGER,
	"intelligence"	INTEGER,
	"agility"	INTEGER,
	"luck"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "user" VALUES (1,'Ookamy',283935710858313730,0,0);
INSERT INTO "user" VALUES (2,'Emmanuelle Ggt',686552959382847504,0,0);
INSERT INTO "fight_level" VALUES (1,1,'Inoffensif',3,50);
INSERT INTO "fight_level" VALUES (2,2,'Novice',4,100);
INSERT INTO "fight_level" VALUES (3,3,'Compétent',5,300);
INSERT INTO "fight_level" VALUES (4,4,'Expert',6,900);
INSERT INTO "fight_level" VALUES (5,5,'Létal',8,2700);
INSERT INTO "fight_player" VALUES (283935710858313730,0,0,0,1,1,1,1,1,1,1,1);
INSERT INTO "fight_player" VALUES (686552959382847504,0,0,0,1,1,1,1,1,1,1,1);
INSERT INTO "fight_adversary" VALUES (1,'Wicket','wicket.png','Ewok',0,0,0,0,0,0,0);
INSERT INTO "fight_adversary" VALUES (2,'Fluttershy','flutter.png','Pegase',2,2,2,2,2,2,2);
INSERT INTO "fight_adversary" VALUES (3,'Grunt','grunt.png','Krogan',2,0,2,0,-1,-1,0);
INSERT INTO "fight_adversary" VALUES (4,'Commandant Shepard','shepard.png','Shepard',5,5,5,5,5,5,5);
INSERT INTO "fight_special" VALUES (1,1,2,1,2,1,1,2,1);
INSERT INTO "fight_special" VALUES (2,2,3,2,3,1,1,3,2);
INSERT INTO "fight_special" VALUES (3,3,3,3,4,2,1,3,3);
INSERT INTO "fight_special" VALUES (4,4,4,3,6,2,1,3,3);
INSERT INTO "fight_special" VALUES (5,5,5,3,6,2,1,3,4);
INSERT INTO "fight_special" VALUES (6,6,5,3,6,2,1,4,4);
INSERT INTO "fight_special" VALUES (7,7,5,3,6,2,2,4,4);
INSERT INTO "fight_special" VALUES (8,8,5,3,6,3,2,4,4);
INSERT INTO "fight_special" VALUES (9,9,6,3,6,3,2,4,4);
INSERT INTO "fight_special" VALUES (10,10,8,3,6,3,2,4,4);
COMMIT;
