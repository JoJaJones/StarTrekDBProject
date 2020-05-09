SECRET = "SJootneelso"

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

TABLES_LIST = [CHARACTERS, AFFILIATIONS, SPECIES, LOCATIONS, SERIES, ACTORS,
               CHAR_SPECIES, CHAR_AFFILS, CHAR_SERIES, CHAR_SERIES_LOCS]

TABLES = {
    CHARACTERS: f"CREATE TABLE {CHARACTERS} ("
                 "id int(11) NOT NULL AUTO_INCREMENT,"
                 "fname varchar(255) NOT NULL,"
                 "lname varchar(255) DEFAULT NULL,"
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

    CHAR_SERIES: f"CREATE TABLE {CHAR_SERIES} ("
                  "cid int(11) NOT NULL,"
                  "sid int(11) NOT NULL,"
                 f"FOREIGN KEY (cid) REFERENCES {CHARACTERS}(id) "
                  "ON DELETE CASCADE ON UPDATE CASCADE,"
                 f"FOREIGN KEY (sid) REFERENCES {SERIES}(id) "
                  "ON DELETE CASCADE ON UPDATE CASCADE,"
                  "PRIMARY KEY (cid, sid))engine=innoDB;"
}

BASIC_SELECT_QUERIES = {
    SPECIES: f"SELECT id, name FROM {SPECIES} ORDER BY name",
    CHARACTERS: f"SELECT id, fname, lname, title FROM {CHARACTERS} ORDER BY fname",
    AFFILIATIONS: f"SELECT id, name FROM {AFFILIATIONS} ORDER BY name",
    ACTORS: f"SELECT id, fname, lname, birthday, imdb FROM {ACTORS} ORDER BY fname",
    SERIES: f"SELECT id, name, start_date, end_date FROM {SERIES} ORDER BY name",
    LOCATIONS: f"SELECT id, name, type FROM {LOCATIONS} ORDER BY name"
}

VIEW_COLUMNS = {
    SPECIES: ["Species"],
    CHARACTERS: ["First Name", "Last Name", "Title"],
    AFFILIATIONS: ["Affiliation"],
    SERIES: ["Series", "Start Date", "End Date"],
    LOCATIONS: ["Name", "Type"],
    ACTORS: ["First Name", "Last Name", "Birthday", "IMDB"]
}

PREPOPULATE = {
    '1': "INSERT INTO characters"
         "(fname,lname,title,description,biography)"
         "VALUES"
         "('James','Kirk','Commanding Officer','Captain','James Tiberius Kirk was born in Riverside, Iowa, on March 22, 2233');",

    '2': "INSERT INTO characters"
         "(fname,lname,title,description)"
         "VALUES"
         "('Hirakaru','Sulu','Captain','Commanding Officer');",

    '3': "INSERT INTO characters"
         "(fname,lname,title)"
         "VALUES"
         "('Nyota','Uhura','Commander');",

    '4': "INSERT INTO characters"
         "(fname,title)"
         "VALUES"
         "('Spock','Ambassador');",

    '5': "INSERT INTO actors"
         "(fname,lname,birthday,imdb,cid)"
         "VALUES"
         "('William','Shatner','1931-03-22','https://www.imdb.com/name/nm0000638/',(SELECT id from characters WHERE lname='Kirk')),"
         "('George','Takei','1937-04-20','https://www.imdb.com/name/nm0001786/',(SELECT id from characters WHERE lname='Sulu'));",

    '6': "INSERT INTO actors"
         "(fname,lname,birthday)"
         "VALUES"
         "('LeVar','Burton','1957-02-16'),"
         "('Patrick','Stewart','1940-07-13');"
}
