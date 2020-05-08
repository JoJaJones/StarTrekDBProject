SECRET = "SJootneelso"

CHAR = "characters"
ACT = "actors"
AFF = "affiliations"
SPEC = "species"
LOC = "locations"
SER = "series"


TABLES_LIST = [CHAR, AFF, SPEC, LOC, SER,
               ACT, "characters_species", "characters_affiliations", "characters_series",
               "characters_series_locations"]


TABLES = {
    CHAR: "CREATE TABLE characters ("
                  "id int(11) NOT NULL AUTO_INCREMENT,"
                  "fname varchar(255) NOT NULL,"
                  "lname varchar(255) DEFAULT NULL,"
                  "title varchar(255) DEFAULT NULL,"
                  "description text DEFAULT NULL,"
                  "biography text DEFAULT NULL,"
                  "PRIMARY KEY(id))engine=innoDB;",

    ACT: "CREATE TABLE actors ("
              "id int(11) NOT NULL AUTO_INCREMENT,"
              "fname varchar(255) NOT NULL,"
              "lname varchar(255) DEFAULT NULL,"
              "birthday date DEFAULT NULL,"
              "imdb varchar(255) DEFAULT NULL,"
              "cid INT DEFAULT NULL,"
              "FOREIGN KEY (cid) REFERENCES characters(id)"
              "ON DELETE CASCADE ON UPDATE CASCADE,"
              "PRIMARY KEY(id))engine=innoDB;",

    AFF: "CREATE TABLE affiliations ("
                    "id int(11) NOT NULL AUTO_INCREMENT,"
                    "name varchar(255) NOT NULL,"
                    "PRIMARY KEY(id))engine=innoDB;",

    SPEC: "CREATE TABLE species ("
               "id int(11) NOT NULL AUTO_INCREMENT,"
               "name varchar(255) NOT NULL,"
               "PRIMARY KEY (id))engine=innoDB;",

    LOC: "CREATE TABLE locations ("
                 "id int(11) NOT NULL AUTO_INCREMENT,"
                 "name varchar(255) NOT NULL,"
                 "type varchar(255),"
                 "PRIMARY KEY (id))engine=innoDB;",

    SER: "CREATE TABLE series ("
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
    SPEC: "SELECT id, name FROM species ORDER BY name",
    CHAR: "SELECT id, fname, lname, title FROM characters ORDER BY name",
    AFF: "SELECT id, fname, lname, title FROM affiliations ORDER BY name",
    ACT: "SELECT id, fname, lname, birthday, imdb FROM actors ORDER BY name",
    SER: "SELECT id, name, start_date, end_date FROM series ORDER BY name",
    LOC: "SELECT id, name, type FROM locations ORDER BY name"
}

VIEW_COLUMNS = {
    SPEC: ["Species"],
    CHAR: ["First Name", "Last Name", "Title"],
    AFF: ["Affiliation"],
    SER: ["Series", "Start Date", "End Date"],
    LOC: ["Name", "Type"]
}