-- missing: char_aff, char_ser_loc

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
FOREIGN KEY (cid) REFERENCES characters(id)
ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY(id))engine=innoDB;

CREATE TABLE affiliations (
id int(11) NOT NULL AUTO_INCREMENT,
name varchar(255) NOT NULL,
PRIMARY KEY(id))engine=innoDB;

CREATE TABLE species (
id int(11) NOT NULL AUTO_INCREMENT,
name varchar(255) NOT NULL,
PRIMARY KEY (id))engine=innoDB;

CREATE TABLE locations (
id int(11) NOT NULL AUTO_INCREMENT,
name varchar(255) NOT NULL,
type varchar(255),
PRIMARY KEY (id))engine=innoDB;

CREATE TABLE series (
id int(11) NOT NULL AUTO_INCREMENT,
name varchar(255) NOT NULL,
start_date DATE DEFAULT NULL,
end_date DATE DEFAULT NULL,
PRIMARY KEY (id))engine=innoDB;          

CREATE TABLE characters_species (
cid int(11) NOT NULL,
sid int(11) NOT NULL,
FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) 
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (sid) REFERENCES {SPECIES}(id) 
ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (cid, sid))engine=innoDB;

CREATE TABLE characters_series (
cid int(11) NOT NULL,
sid int(11) NOT NULL,
FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) 
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (sid) REFERENCES {SERIES}(id) 
ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (cid, sid))engine=innoDB;

