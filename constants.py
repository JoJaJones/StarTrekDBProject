SECRET = "SJootneelso"

CHARACTERS = "characters"
ACTORS = "actors"
AFFILIATIONS = "affiliations"
SPECIES = "species"
LOCATIONS = "locations"
SERIES = "series"


TABLES_LIST = [CHARACTERS, AFFILIATIONS, SPECIES, LOCATIONS, SERIES,
               ACTORS, "characters_species", "characters_affiliations", "characters_series",
               "characters_series_locations"]


TABLES = {
    CHARACTERS: "CREATE TABLE characters ("
                  "id int(11) NOT NULL AUTO_INCREMENT,"
                  "fname varchar(255) NOT NULL,"
                  "lname varchar(255) DEFAULT NULL,"
                  "title varchar(255) DEFAULT NULL,"
                  "description text DEFAULT NULL,"
                  "biography text DEFAULT NULL,"
                  "PRIMARY KEY(id))engine=innoDB;",

    ACTORS: "CREATE TABLE actors ("
              "id int(11) NOT NULL AUTO_INCREMENT,"
              "fname varchar(255) NOT NULL,"
              "lname varchar(255) DEFAULT NULL,"
              "birthday date DEFAULT NULL,"
              "imdb varchar(255) DEFAULT NULL,"
              "cid INT DEFAULT NULL,"
              "FOREIGN KEY (cid) REFERENCES characters(id)"
              "ON DELETE CASCADE ON UPDATE CASCADE,"
              "PRIMARY KEY(id))engine=innoDB;",

    AFFILIATIONS: "CREATE TABLE affiliations ("
                    "id int(11) NOT NULL AUTO_INCREMENT,"
                    "name varchar(255) NOT NULL,"
                    "PRIMARY KEY(id))engine=innoDB;",

    SPECIES: "CREATE TABLE species ("
               "id int(11) NOT NULL AUTO_INCREMENT,"
               "name varchar(255) NOT NULL,"
               "PRIMARY KEY (id))engine=innoDB;",

    LOCATIONS: "CREATE TABLE locations ("
                 "id int(11) NOT NULL AUTO_INCREMENT,"
                 "name varchar(255) NOT NULL,"
                 "type varchar(255),"
                 "PRIMARY KEY (id))engine=innoDB;",

    SERIES: "CREATE TABLE series ("
              "id int(11) NOT NULL AUTO_INCREMENT,"
              "name varchar(255) NOT NULL,"
              "start_date DATE DEFAULT NULL,"
              "end_date DATE DEFAULT NULL,"
              "PRIMARY KEY (id))engine=innoDB;",

    "characters_species": "CREATE TABLE characters_species ("
                          "cid int(11) NOT NULL,"
                          "sid int(11) NOT NULL,"
                          "FOREIGN KEY (cid) REFERENCES characters(id)"
                          "ON DELETE CASCADE ON UPDATE CASCADE,"
                          "FOREIGN KEY (sid) REFERENCES species(id)"
                          "ON DELETE CASCADE ON UPDATE CASCADE,"
                          "PRIMARY KEY (cid, sid))engine=innoDB;",

    "characters_series": "CREATE TABLE characters_series ("
                         "cid int(11) NOT NULL,"
                         "sid int(11) NOT NULL,"
                         "FOREIGN KEY (cid) REFERENCES characters(id)"
                         "ON DELETE CASCADE ON UPDATE CASCADE,"
                         "FOREIGN KEY (sid) REFERENCES series(id)"
                         "ON DELETE CASCADE ON UPDATE CASCADE,"
                         "PRIMARY KEY (cid, sid))engine=innoDB;"
}

BASIC_SELECT_QUERIES = {
    SPECIES: "SELECT id, name FROM species ORDER BY name",
    CHARACTERS: "SELECT id, fname, lname, title FROM characters ORDER BY fname",
    AFFILIATIONS: "SELECT id, name FROM affiliations ORDER BY name",
    ACTORS: "SELECT id, fname, lname, birthday, imdb FROM actors ORDER BY fname",
    SERIES: "SELECT id, name, start_date, end_date FROM series ORDER BY name",
    LOCATIONS: "SELECT id, name, type FROM locations ORDER BY name"
}

VIEW_COLUMNS = {
    SPECIES: ["Species"],
    CHARACTERS: ["First Name", "Last Name", "Title"],
    AFFILIATIONS: ["Affiliation"],
    SERIES: ["Series", "Start Date", "End Date"],
    LOCATIONS: ["Name", "Type"],
    ACTORS: ["First Name", "Last Name", "Birthday", "IMDB"]
}