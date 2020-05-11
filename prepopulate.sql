-- characters data
INSERT INTO characters
(fname,lname,title,description,biography)
VALUES
('James','Kirk','Commanding Officer','Chief of Starfleet Operations','James Tiberius Kirk was born in Riverside, Iowa, on March 22, 2233');
INSERT INTO characters
(fname,lname,title,description)
VALUES
('Hirakaru','Sulu','Captain','USS Enterprise helmsman');
INSERT INTO characters
(fname,lname,title)
VALUES
('Nyota','Uhura','Lieutenant Commander');
INSERT INTO characters
(fname,title)
VALUES
('Spock','Ambassador');

-- actors data
INSERT INTO actors
(fname,lname,birthday,imdb,cid)
VALUES
('William','Shatner','1931-03-22','https://www.imdb.com/name/nm0000638/',(SELECT id from characters WHERE lname='Kirk')),
('George','Takei','1937-04-20','https://www.imdb.com/name/nm0001786/',(SELECT id from characters WHERE lname='Sulu'));
INSERT INTO actors
(fname,lname,birthday)
VALUES
('LeVar','Burton','1957-02-16'),
('Patrick','Stewart','1940-07-13');

-- affiliations data
INSERT INTO affiliations
(name)
VALUES
('Starfleet'),
('Borg'),
('Ferengi'),
('Klingon'),
('Romulan');

-- species data
INSERT INTO species
(name)
VALUES
('Borg'),
('Breen'),
('Human'),
('Vulcan'),
('Hirogen');

-- locations data
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
INSERT INTO characters_species
(cid,sid)
VALUES
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from species WHERE name='Human')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from species WHERE name='Vulcan')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from species WHERE name='Human')),
((SELECT id from characters WHERE lname='Sulu'),(SELECT id from species WHERE name='Human')),
((SELECT id from characters WHERE lname='Uhura'),(SELECT id from species WHERE name='Human'));

-- character_series data
INSERT INTO characters_series
(cid,sid)
VALUES
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from series WHERE name='The Original Series')),
((SELECT id from characters WHERE lname='Kirk'),(SELECT id from series WHERE name='The Next Generation')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from series WHERE name='The Original Series')),
((SELECT id from characters WHERE fname='Spock'),(SELECT id from series WHERE name='The Next Generation')),
((SELECT id from characters WHERE lname='Sulu'),(SELECT id from series WHERE name='The Original Series')),
((SELECT id from characters WHERE lname='Uhura'),(SELECT id from series WHERE name='The Original Series'));

