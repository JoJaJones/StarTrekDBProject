SECRET = "SJootneelso"
TABLES = {
    "characters": "CREATE TABLE characters ("
                  "id int(11) NOT NULL AUTO_INCREMENT,"
                  "fname varchar(255) NOT NULL,"
                  "lname varchar(255) DEFAULT NULL,"
                  "title varchar(255) DEFAULT NULL,"
                  "desciption text DEFAULT NULL,"
                  "biography text DEFAULT NULL,"
                  "PRIMARY KEY(id))engine=innoDB;",

    "actors": "CREATE TABLE actors ("
              "id int(11) NOT NULL AUTO_INCREMENT,"
              "fname varchar(255) NOT NULL,"
              "lname varchar(255) DEFAULT NULL,"
              "birthday date DEFAULT NULL,"
              "imdb varchar(255) DEFAULT NULL,"
              "cid INT DEFAULT NULL,"
              "FOREIGN KEY (cid) REFERENCES characters(id)"
              "ON DELETE CASCADE ON UPDATE CASCADE,"
              "PRIMARY KEY(id))engine=innoDB;",

    "affiliations": "CREATE TABLE affiliations ("
                    "id int(11) NOT NULL AUTO_INCREMENT,"
                    "name varchar(255) NOT NULL,"
                    "PRIMARY KEY(id))engine=innoDB;"
}