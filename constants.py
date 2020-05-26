SECRET = "SJootneelso"

INSERT = "insert"
UPDATE = "update"

SUBMIT_TYPE = "sub_type"
UPDATE_PAGE = "update_page"

CHARACTERS       = "characters"
ACTORS           = "actors"
AFFILIATIONS     = "affiliations"
SPECIES          = "species"
LOCATIONS        = "locations"
SERIES           = "series"
CHAR_SPECIES     = "characters_species"
CHAR_AFFILS      = "characters_affiliations"
CHAR_SERIES      = "characters_series"
CHAR_SERIES_LOCS = "characters_series_locations"
CHAR_ACTORS      = "characters_actors" # Not an actual table

TABLES_LIST = [CHARACTERS, AFFILIATIONS, SPECIES, LOCATIONS, SERIES, ACTORS,
               CHAR_SPECIES, CHAR_AFFILS, CHAR_SERIES, CHAR_SERIES_LOCS]

LOCATION_TYPE_DICT = {"ship": "Space Ship", "planet": "Planet", "station": "Space Station"}

TABLES = {
    CHARACTERS: f"CREATE TABLE {CHARACTERS} ("
                 "id int(11) NOT NULL AUTO_INCREMENT,"
                 "fname varchar(255) NOT NULL,"
                 "lname varchar(255) DEFAULT NULL,"
                 "alias varchar(255) NOT NULL,"
                 "title varchar(255) DEFAULT NULL,"
                 "description text DEFAULT NULL,"
                 "biography text DEFAULT NULL,"
                 "PRIMARY KEY(id))engine=innoDB;",

    ACTORS: f"CREATE TABLE {ACTORS} ("
             "id int(11) NOT NULL AUTO_INCREMENT,"
             "fname varchar(255) NOT NULL,"
             "lname varchar(255) DEFAULT NULL,"
             "birthday date DEFAULT NULL,"
             "imdb varchar(255) DEFAULT NULL,"
             "cid INT DEFAULT NULL,"
            f"FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) "
             "ON DELETE CASCADE ON UPDATE CASCADE,"
             "PRIMARY KEY(id))engine=innoDB;",

    AFFILIATIONS: f"CREATE TABLE {AFFILIATIONS} ("
                   "id int(11) NOT NULL AUTO_INCREMENT,"
                   "name varchar(255) NOT NULL,"
                   "PRIMARY KEY(id))engine=innoDB;",

    SPECIES: f"CREATE TABLE {SPECIES} ("
              "id int(11) NOT NULL AUTO_INCREMENT,"
              "name varchar(255) NOT NULL,"
              "PRIMARY KEY (id))engine=innoDB;",

    LOCATIONS: f"CREATE TABLE {LOCATIONS} ("
                "id int(11) NOT NULL AUTO_INCREMENT,"
                "name varchar(255) NOT NULL,"
                "type varchar(255),"
                "PRIMARY KEY (id))engine=innoDB;",

    SERIES: f"CREATE TABLE {SERIES} ("
             "id int(11) NOT NULL AUTO_INCREMENT,"
             "name varchar(255) NOT NULL,"
             "start_date DATE DEFAULT NULL,"
             "end_date DATE DEFAULT NULL,"
             "PRIMARY KEY (id))engine=innoDB;",

    CHAR_SPECIES: f"CREATE TABLE {CHAR_SPECIES} ("
                   "cid int(11) NOT NULL,"
                   "sid int(11) NOT NULL,"
                  f"FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) "
                   "ON DELETE CASCADE ON UPDATE CASCADE,"
                  f"FOREIGN KEY (sid) REFERENCES {SPECIES}(id) "
                   "ON DELETE CASCADE ON UPDATE CASCADE,"
                   "PRIMARY KEY (cid, sid))engine=innoDB;",

    CHAR_AFFILS: f"CREATE TABLE {CHAR_AFFILS} ("
                  "cid int(11) NOT NULL,"
                  "aid int(11) NOT NULL,"
                 f"FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) "
                  "ON DELETE CASCADE ON UPDATE CASCADE,"
                 f"FOREIGN KEY (aid) REFERENCES {AFFILIATIONS}(id) "
                  "ON DELETE CASCADE ON UPDATE CASCADE,"
                  "PRIMARY KEY (cid, aid))engine=innoDB;",

    CHAR_SERIES: f"CREATE TABLE {CHAR_SERIES} ("
                  "id int(11) NOT NULL AUTO_INCREMENT,"
                  "cid int(11) NOT NULL,"
                  "sid int(11) NOT NULL,"
                 f"FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) "
                  "ON DELETE CASCADE ON UPDATE CASCADE,"
                 f"FOREIGN KEY (sid) REFERENCES {SERIES}(id) "
                  "ON DELETE CASCADE ON UPDATE CASCADE,"
                  "PRIMARY KEY (id))engine=innoDB;",
      
    CHAR_SERIES_LOCS: f"CREATE TABLE {CHAR_SERIES_LOCS} ("
                       "csid int(11) NOT NULL,"
                       "lid int(11) NOT NULL,"
                      f"FOREIGN KEY (csid) REFERENCES {CHAR_SERIES}(id) "
                       "ON DELETE CASCADE ON UPDATE CASCADE,"
                      f"FOREIGN KEY (lid) REFERENCES {LOCATIONS}(id) "
                       "ON DELETE CASCADE ON UPDATE CASCADE,"
                       "PRIMARY KEY (csid, lid))engine=innoDB;"
}

BASIC_SELECT_QUERIES = {
    SPECIES: f"SELECT id, name FROM {SPECIES} ORDER BY name",
    CHARACTERS: f"SELECT id, fname, lname, alias, title FROM {CHARACTERS} ORDER BY fname",
    AFFILIATIONS: f"SELECT id, name FROM {AFFILIATIONS} ORDER BY name",
    ACTORS: f"SELECT id, fname, lname, birthday, imdb FROM {ACTORS} ORDER BY fname",
    SERIES: f"SELECT id, name, start_date, end_date FROM {SERIES} ORDER BY name",
    LOCATIONS: f"SELECT id, name, type FROM {LOCATIONS} ORDER BY name"
}

VIEW_COLUMNS = {
    SPECIES: ["Species"],
    CHARACTERS: ["First Name", "Last Name", "Alias", "Title"],
    AFFILIATIONS: ["Affiliation"],
    SERIES: ["Series", "Start Date", "End Date"],
    LOCATIONS: ["Name", "Type"],
    ACTORS: ["First Name", "Last Name", "Birthday", "IMDB"],
    CHAR_ACTORS: ["Character Name", "Actor Name"],
    CHAR_SPECIES: ["Character Name", "Species Name"],
    CHAR_AFFILS: ["Character Name", "Affiliation Name"],
    CHAR_SERIES: ["Character Name", "Series Name"],
    CHAR_SERIES_LOCS: ["Character/Series Name", "Location Name"]
}

SERIES_INSERT_QUERIES ={
      0: f"INSERT INTO {SERIES}(name, start_date, end_date) VALUES (%s, %s, %s)",
      1: f"INSERT INTO {SERIES}(name, start_date) VALUES (%s, %s)",
      2: f"INSERT INTO {SERIES}(name, end_date) VALUES (%s, %s)",
      3: f"INSERT INTO {SERIES}(name) VALUES (%s)"
}

SERIES_UPDATE_QUERIES ={
      0: f"UPDATE {SERIES} SET name = %s, start_date = %s, end_date = %s WHERE id = %s",
      1: f"UPDATE {SERIES} SET name = %s, start_date = %s WHERE id = %s",
      2: f"UPDATE {SERIES} SET name = %s, end_date = %s WHERE id = %s",
      3: f"UPDATE {SERIES} SET name = %s WHERE id = %s"
}

PREPOPULATE = {
      1: f"INSERT INTO {CHARACTERS}"
          "(fname,lname,title,description,biography)"
          "VALUES"
          "('James','Kirk','Commanding Officer','Chief of Starfleet Operations','James Tiberius Kirk was born in Riverside, Iowa, on March 22, 2233');",

      2: f"INSERT INTO {CHARACTERS}"
          "(fname,lname,title,description)"
           "VALUES"
         "('Hirakaru','Sulu','Captain','USS Enterprise helmsman');",

      3: f"INSERT INTO {CHARACTERS}"
          "(fname,lname,title)"
          "VALUES"
          "('Nyota','Uhura','Lieutenant Commander');",

      4: f"INSERT INTO {CHARACTERS}"
          "(fname,title)"
          "VALUES"
          "('Spock','Ambassador');",

      5: f"INSERT INTO {ACTORS}"
          "(fname,lname,birthday,imdb,cid)"
          "VALUES"
          "('William','Shatner','1931-03-22','https://www.imdb.com/name/nm0000638/',(SELECT id from characters WHERE lname='Kirk')),"
          "('George','Takei','1937-04-20','https://www.imdb.com/name/nm0001786/',(SELECT id from characters WHERE lname='Sulu'));",

      6: f"INSERT INTO {ACTORS}"
          "(fname,lname,birthday)"
          "VALUES"
          "('LeVar','Burton','1957-02-16'),"
          "('Patrick','Stewart','1940-07-13');",

      7: f"INSERT INTO {AFFILIATIONS}"
          "(name)"
          "VALUES"
          "('Starfleet'),"
          "('Borg'),"
          "('Ferengi'),"
          "('Klingon'),"
          "('Romulan');",

      8: f"INSERT INTO {SPECIES}"
          "(name)"
          "VALUES"
          "('Borg'),"
          "('Breen'),"
          "('Human'),"
          "('Vulcan'),"
          "('Hirogen');",

      9: f"INSERT INTO {LOCATIONS}"
          "(name,type)"
          "VALUES"
          "('Omicron Kappa II','planet'),"
          "('Boreth','planet'),"
          "('Earth','planet'),"
          "('USS Enterprise','ship'),"
          "('Borg Cube','ship'),"
          "('USS Voyager','ship'),"
          "('Deep Space 9','station');",

      10: f"INSERT INTO {SERIES}"
           "(name,start_date,end_date)"
           "VALUES"
           "('The Original Series','1966-09-08','1968-09-20'),"
           "('The Next Generation','1987-09-28','1993-09-20'),"
           "('Voyager','1995-01-16','2000-10-04');",

      11: f"INSERT INTO {SERIES}"
           "(name,start_date)"
           "VALUES"
           "('Discovery','2017-09-24');",

      12: f"INSERT INTO {CHAR_SPECIES}"
           "(cid,sid)"
           "VALUES"
           "((SELECT id from characters WHERE lname='Kirk'),(SELECT id from species WHERE name='Human')),"
           "((SELECT id from characters WHERE fname='Spock'),(SELECT id from species WHERE name='Vulcan')),"
           "((SELECT id from characters WHERE fname='Spock'),(SELECT id from species WHERE name='Human')),"
           "((SELECT id from characters WHERE lname='Sulu'),(SELECT id from species WHERE name='Human')),"
           "((SELECT id from characters WHERE lname='Uhura'),(SELECT id from species WHERE name='Human'));",

      13: f"INSERT INTO {CHAR_SERIES}"
           "(cid,sid)"
           "VALUES"
           "((SELECT id from characters WHERE lname='Kirk'),(SELECT id from series WHERE name='The Original Series')),"
           "((SELECT id from characters WHERE lname='Kirk'),(SELECT id from series WHERE name='The Next Generation')),"
           "((SELECT id from characters WHERE fname='Spock'),(SELECT id from series WHERE name='The Original Series')),"
           "((SELECT id from characters WHERE fname='Spock'),(SELECT id from series WHERE name='The Next Generation')),"
           "((SELECT id from characters WHERE lname='Sulu'),(SELECT id from series WHERE name='The Original Series')),"
           "((SELECT id from characters WHERE lname='Uhura'),(SELECT id from series WHERE name='The Original Series'));"

}


