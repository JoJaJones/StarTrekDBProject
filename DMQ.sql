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
SELECT id, fname, lname, alias FROM characters WHERE fname=(:fname_input);
-- Search by last name
SELECT id, fname, lname, alias FROM characters WHERE lname=(:lname_input);

SELECT id, fname, lname, alias FROM characters WHERE :user_input IN lname or :user_input IN lname
-- Search by series on-air date
SELECT id, fname, lname, alias FROM characters C
	JOIN characters_series CS ON CS.cid=C.id
	JOIN series S ON S.id=CS.sid
	WHERE S.start_date<=(:airdate_input) AND S.end_date>=(:airdate_input)
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
	WHERE SP.id in (:list_of_selected_species)
		AND S.id in (:list_of_selected_series)
		AND L.id in (:list_of_selected_locations)
		AND A.id in (:list_of_selected_actors)
	GROUP BY C.fname, C.lname;

--Search Series
SELECT name, start_date, end_date FROM series WHERE :user_input IN name

--Search Species
SELECT name FROM species WHERE :user_input IN name

--Search Locations
SELECT name, type From locations WHERE :user_input IN name

--Search Actors
SELECT fname, lname, birthday, imdb, cid FROM actors WHERE :user_input IN lname OR :user_input IN fname

--Search Affiliations
SELECT name FROM affiliations WHERE :user_input IN name

-- add a new actor (change query based on inputs given)
INSERT INTO actors (fname, lname, birthday date, imdb, cid) VALUES (:fname_input, :lname_input, :birthday_input, :imdb_input, :cid_input);

-- add new series (change query based on inputs given)
INSERT INTO series (name,start_date,end_date) VALUES (:name_input, :start_date_input, :end_date_input);

-- add a new location
INSERT INTO locations (name,type) VALUES (:name_input, :type_from_pulldown);

-- add a new species, affiliation
INSERT INTO {tablename} (name) VALUES (:name_input);

-- associate a character with a series (M-to-M relationship addition)
INSERT INTO characters (cid, sid) VALUES (:character_id_from_dropdown_input, :series_id_from_dropdown_input);

-- update a character's data based on submission of the Update Character form 
UPDATE characters SET fname = :fname_input, lname= :lname_input, alias= :alias_input, title= :title_input, 
	description= :description_text, biography= :bio_text WHERE id= :character_ID_from_the_update_form;
	
-- Updates on species, affiliations, actors, locations, series
UPDATE species SET name=:new_name WHERE id=:selected_species;
UPDATE locations SET name=:new_name, type=:new_type  WHERE id=:selected_location;
UPDATE affiliations SET name=:new_name  WHERE id=:selected_affiliation;
UPDATE series SET name=:new_name, start_date=:newStartDate, end_date= :new_end_date  WHERE id=:selected_series;
UPDATE actors SET fname=:new_fname, lname=:new_lname, birthday=:new_date, imdb= :new_IMDB_link, cid=:new_char_ID_from_list WHERE id=:selected_actor;


-- All deletes follow the same pattern from the button which activates the delete action
DELETE FROM {table_name} WHERE id = {row_num};

-- Unlink an actor to a character
UPDATE actors SET cid=NULL WHERE id=:selected_actor_character_pair;

-- Remove Species, Affiliation, or Series link to character
DELETE FROM characters_series WHERE id=:csid_from_selected_character_series;
DELETE FROM characters_species WHERE cid=:cidFromSelectedCharacterSpecies AND sid=:sid_from_selected_character_species;
DELETE FROM characters_affiliations WHERE cid=:cidFromSelectedCharacterAffiliation AND aid=:sid_from_selected_character_affiliation;

-- Remove location link to character_series combo
DELETE FROM characters_series_locations WHERE csid=:csid_from_selected_character_series AND sid=:sid_from_selected_character_series;
