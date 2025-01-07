CREATE TABLE IF NOT EXISTS `notes` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`user_id`	INTEGER,
	`title`	TEXT,
	`content`	TEXT,
	`priority`	INTEGER DEFAULT 3,
	`date`	TEXT
);
CREATE TABLE IF NOT EXISTS `users` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT,
	`password`	TEXT
);