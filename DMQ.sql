-- These queries are used to populate the 6 main display tables for browsing and on display when adding new entities
SELECT id, name FROM species ORDER BY name;
SELECT id, name FROM affiliations ORDER BY name;
SELECT id, name, type FROM locations ORDER BY name;
SELECT id, name, start_date, end_date FROM series ORDER BY name;
SELECT id, fname, lname, birthday, imdb FROM actors ORDER BY fname;
SELECT C.id, fname, lname, title, SP.name AS Species, S.name AS Series FROM characters C
	JOIN characters_series CS ON CS.cid=C.id
	JOIN series S ON S.id=CS.sid
	JOIN characters_species CSP ON CSP.cid=C.id
	JOIN species SP ON SP.id=CSP.sid ORDER BY fname, lname;

-- get all Species id's and names to populate the Species dropdown on add-character page
SELECT id, name FROM species ORDER BY name;

-- get all Series id's and names to populate the Series dropdown on add-character page
SELECT id, name FROM series ORDER BY name;

-- To connect an actor to a character we need to get all actors who arent currently linked and all characters.
SELECT id, fname, lname, alias FROM characters ORDER BY fname;
SELECT id, fname, lname FROM actors WHERE cid is NULL ORDER BY fname;

-- To connect a character to a species we need to get all characters and all species available
SELECT id, fname, lname, alias FROM characters ORDER BY fname;
SELECT id, name FROM species ORDER BY name;

-- To connect a character to an affilitation we need to get all characters and all affiliations available
SELECT id, fname, lname, alias FROM characters ORDER BY fname;
SELECT id, name FROM affiliations ORDER BY name;

-- To connect a character to an series we need to get all characters and all series available
SELECT id, fname, lname, alias FROM characters ORDER BY fname;
SELECT id, name FROM series ORDER BY name;

-- To connect a character_series combo to a loaction we need to get all character_series and all locations available
SELECT CS.id, CONCAT(fname,' ',IFNULL(lname,'')) AS "Character", name AS Series FROM characters C
	JOIN characters_series CS ON CS.cid=C.id
	JOIN series S ON S.id=CS.sid ORDER BY fname;
SELECT id, name, type FROM locations ORDER BY name;


-- Search Character queries
-- Search by first name
SELECT id, fname, lname, alias FROM characters WHERE fname=(:fnameInput);
-- Search by last name
SELECT id, fname, lname, alias FROM characters WHERE lname=(:lnameInput);
-- Search by series on-air date
SELECT id, fname, lname, alias FROM characters C
	JOIN characters_series CS ON CS.cid=C.id
	JOIN series S ON S.id=CS.sid
	WHERE S.start_date<=(:airdateInput) AND S.end_date>=(:airdateInput)
	ORDER BY fname;
-- Search using filters (would need to alter query depending on if None was selcted)
SELECT C.id, C.fname, C.lname, C.title FROM characters C
	JOIN characters_species CSP ON CSP.cid=C.id
	JOIN species SP ON SP.id=CSP.sid
	JOIN characters_series CS ON CS.cid=C.id
	JOIN series S ON S.id=CS.sid
	JOIN characters_series_locations CSL ON CSL.csid=CS.id
	JOIN locations L ON L.id=CSL.lid
	JOIN actors A ON A.cid=C.id
	WHERE SP.id in (:listOfSelectedSpecies)
		AND S.id in (:listOfSelectedSeries)
		AND L.id in (:listOfSelectedLocations)
		AND A.id in (:listOfSelectedActors)
	ORDER BY C.fname;


-- add a new actor (change query based on inputs given)
INSERT INTO actors (fname, lname, birthday date, imdb, cid) VALUES (:fnameInput, :lnameInput, :birthdayInput, :imdbInput, :cidInput);

-- add new series (change query based on inputs given)
INSERT INTO series (name,start_date,end_date) VALUES (:nameInput, :startDateInput, :endDateInput);

-- add a new location
INSERT INTO locations (name,type) VALUES (:nameInput, :typeFromPulldown);

-- add a new species, affiliation
INSERT INTO {tablename} (name) VALUES (:nameInput);

-- associate a character with a series (M-to-M relationship addition)
INSERT INTO characters (cid, sid) VALUES (:character_id_from_dropdown_Input, :series_id_from_dropdown_Input);

-- update a character's data based on submission of the Update Character form 
UPDATE characters SET fname = :fnameInput, lname= :lnameInput, alias= :aliasInput, title= :titleInput, 
	description= :descriptionText, biography= :bioText WHERE id= :character_ID_from_the_update_form;
	
-- Updates on species, affiliations, actors, locations, series
UPDATE species SET name=:newName WHERE id=:selectedSpecies;
UPDATE locations SET name=:newName, type=:newType  WHERE id=:selectedLocation;
UPDATE affiliations SET name=:newName  WHERE id=:selectedAffiliation;
UPDATE series SET name=:newName, start_date=:newStartDate, end_date= :newEndDate  WHERE id=:selectedSeries;
UPDATE actors SET fname=:newFname, lname=:newFname, birthday=:newDate, imdb= :newIMDBLink, cid=:newCharIDfromList WHERE id=:selectedActor;


-- All deletes follow the same pattern from the button which activates the delete action
DELETE FROM {table_name} WHERE id = {row_num};

-- Unlink an actor to a character
UPDATE actors SET cid=NULL WHERE id=:selectedActorCharacterPair;

-- Remove Species, Affiliation, or Series link to character
DELETE FROM characters_series WHERE id=:csidFromSelectedCharacterSeries;
DELETE FROM characters_species WHERE cid=:cidFromSelectedCharacterSpecies AND sid=:sidFromSelected CharacterSpecies;
DELETE FROM characters_affiliations WHERE cid=:cidFromSelectedCharacterAffiliation AND aid=:sidFromSelected CharacterAffiliation;

-- Remove location link to character_series combo
DELETE FROM characters_series_locations WHERE csid=:csidFromSelectedCharacterSeries AND sid=:sidFromSelected CharacterSeries;
