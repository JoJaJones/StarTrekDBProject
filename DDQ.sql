-- Drop junction tables first
DROP TABLE IF EXISTS characters_series_locations;
DROP TABLE IF EXISTS characters_series;
DROP TABLE IF EXISTS characters_affiliations;
DROP TABLE IF EXISTS characters_species;
DROP TABLE IF EXISTS actors;

	
-- DROP TABLE IF EXISTS characters;
CREATE TABLE characters (
	id int(11) NOT NULL AUTO_INCREMENT,
	fname varchar(255) NOT NULL,
	lname varchar(255) DEFAULT NULL,
	alias varchar(255) NOT NULL,
	title varchar(255) DEFAULT NULL,
	description text DEFAULT NULL,
	biography text DEFAULT NULL,
	PRIMARY KEY(id))engine=innoDB;
	
CREATE TABLE actors (
	id int(11) NOT NULL AUTO_INCREMENT,
	fname varchar(255) NOT NULL,
	lname varchar(255) DEFAULT NULL,
	birthday date DEFAULT NULL,
	imdb varchar(255) DEFAULT NULL,
	cid INT DEFAULT NULL,
	FOREIGN KEY (cid) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(id))engine=innoDB;

-- DROP TABLE IF EXISTS affiliations;
CREATE TABLE affiliations (
	id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	PRIMARY KEY(id))engine=innoDB;

-- DROP TABLE IF EXISTS species;
CREATE TABLE species (
	id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	PRIMARY KEY (id))engine=innoDB;

-- DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
	id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	type varchar(255),
	PRIMARY KEY (id))engine=innoDB;

-- DROP TABLE IF EXISTS series;
CREATE TABLE series (
	id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	start_date DATE DEFAULT NULL,
	end_date DATE DEFAULT NULL,
	PRIMARY KEY (id))engine=innoDB;

-- DROP TABLE IF EXISTS characters_species;
CREATE TABLE characters_species (
	cid int(11) NOT NULL,
	sid int(11) NOT NULL,
	FOREIGN KEY (cid) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (sid) REFERENCES species(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (cid, sid))engine=innoDB;

-- DROP TABLE IF EXISTS characters_affiliations;
CREATE TABLE characters_affiliations (
	cid int(11) NOT NULL,
	aid int(11) NOT NULL,
	FOREIGN KEY (cid) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (aid) REFERENCES affiliations(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (cid, aid))engine=innoDB;

-- DROP TABLE IF EXISTS characters_series;
CREATE TABLE characters_series (
	id int(11) NOT NULL AUTO_INCREMENT,
	cid int(11) NOT NULL,
	sid int(11) NOT NULL,
	FOREIGN KEY (cid) REFERENCES characters(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (sid) REFERENCES series(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (id))engine=innoDB;

-- DROP TABLE IF EXISTS characters_series_locations;
CREATE TABLE characters_series_locations (
	csid int(11) NOT NULL,
	lid int(11) NOT NULL,
	FOREIGN KEY (csid) REFERENCES characters_series(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (lid) REFERENCES locations(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (csid, lid))engine=innoDB;



-- Insert Data

-- characters data
-- (fname, lname, alias, title, description, biography)
INSERT INTO characters
(fname,lname,alias,title,description,biography)
VALUES
('James','Kirk','Captain Kirk','Commanding Officer','Chief of Starfleet Operations','James Tiberius Kirk was born in Riverside, Iowa, on March 22, 2233');
INSERT INTO characters
(fname,lname,alias,title,description)
VALUES
('Hirakaru','Sulu','Captain Sulu','Captain','USS Enterprise helmsman');
INSERT INTO characters
(fname,lname,alias,title)
VALUES
('Nyota','Uhura','Uhura','Lieutenant Commander');
INSERT INTO characters
(fname,alias,title)
VALUES
('Spock','Spock','Ambassador'),
('Borg Queen','Borg Queen','Queen'),
('Worf','Worf','Lieutenant');

-- actors data
-- (fname, lname, birthday, imdb, cid)
INSERT INTO actors
(fname,lname,birthday,imdb,cid)
VALUES
('William','Shatner','1931-03-22','https://www.imdb.com/name/nm0000638/',(SELECT id from characters WHERE lname='Kirk')),
('George','Takei','1937-04-20','https://www.imdb.com/name/nm0001786/',(SELECT id from characters WHERE lname='Sulu')),
('Leonard', 'Nimoy', '1931-03-26', 'https://www.imdb.com/name/nm0000559/', (SELECT id FROM characters WHERE alias='Spock'));
INSERT INTO actors
(fname,lname,birthday)
VALUES
('Michael','Dorn','1952-12-09'),
('LeVar','Burton','1957-02-16'),
('Patrick','Stewart','1940-07-13');

-- affiliations data
-- (name)
INSERT INTO affiliations
(name)
VALUES
('Starfleet'),
('Borg'),
('Ferengi'),
('Klingon'),
('Romulan');

-- species data
-- (name)
INSERT INTO species
(name)
VALUES
('Borg'),
('Breen'),
('Human'),
('Klingon'),
('Vulcan'),
('Hirogen');

-- locations data
-- (name, type)
INSERT INTO locations
(name,type)
VALUES
('Omicron Kappa II','planet'),
('Boreth','planet'),
('Earth','planet'),
('USS Enterprise','ship'),
('Borg Cube','ship'),
('USS Voyager','ship'),
('Deep Space 9','station');

-- series data
-- (name, start_date, end_date)
INSERT INTO series
(name,start_date,end_date)
VALUES
('The Original Series','1966-09-08','1968-09-20'),
('The Next Generation','1987-09-28','1993-09-20'),
('Voyager','1995-01-16','2000-10-04');
INSERT INTO series
(name,start_date)
VALUES
('Discovery','2017-09-24');

-- character_species data
-- (cid, sid)
INSERT INTO characters_species
(cid,sid)
VALUES
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from species WHERE name='Human')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from species WHERE name='Vulcan')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from species WHERE name='Human')),
((SELECT id from characters WHERE lname='Sulu'),(SELECT id from species WHERE name='Human')),
((SELECT id from characters WHERE fname='Worf'),(SELECT id from species WHERE name='Klingon')),
((SELECT id from characters WHERE fname='Borg Queen'),(SELECT id from species WHERE name='Borg')),
((SELECT id from characters WHERE lname='Uhura'),(SELECT id from species WHERE name='Human'));

-- characters_affiliations data
-- (cid, aid)
INSERT INTO characters_affiliations
(cid,aid)
VALUES
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from affiliations WHERE name='Starfleet')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from affiliations WHERE name='Starfleet')),
((SELECT id from characters WHERE lname='Sulu'),(SELECT id from affiliations WHERE name='Starfleet')),
((SELECT id from characters WHERE fname='Worf'),(SELECT id from affiliations WHERE name='Klingon')),
((SELECT id from characters WHERE fname='Borg Queen'),(SELECT id from affiliations WHERE name='Borg')),
((SELECT id from characters WHERE lname='Uhura'),(SELECT id from affiliations WHERE name='Starfleet'));

-- character_series data
-- (cid, sid)
INSERT INTO characters_series
(cid,sid)
VALUES
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from series WHERE name='The Original Series')),
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from series WHERE name='The Next Generation')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from series WHERE name='The Original Series')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from series WHERE name='The Next Generation')),
((SELECT id from characters WHERE lname='Sulu'),(SELECT id from series WHERE name='The Original Series')),
((SELECT id from characters WHERE lname='Uhura'),(SELECT id from series WHERE name='The Original Series'));

-- characters_series_locations data
-- (csid, lid)
INSERT INTO characters_series_locations
(csid,lid)
VALUES
((SELECT id from characters_series WHERE cid=(SELECT id from characters WHERE lname='Kirk') AND sid=(SELECT id from series WHERE name='The Original Series')),(SELECT id from locations WHERE name='USS Enterprise')),
((SELECT id from characters_series WHERE cid=(SELECT id from characters WHERE lname='Sulu') AND sid=(SELECT id from series WHERE name='The Original Series')),(SELECT id from locations WHERE name='USS Enterprise'));
