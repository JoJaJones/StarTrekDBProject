-- format existing select queries and any non-basic ones in the flask file
-- add insert, update, and delete queries

BASIC_SELECT_QUERIES = {
    SPECIES: f"SELECT id, name FROM {SPECIES} ORDER BY name",
    CHARACTERS: f"SELECT id, fname, lname, alias, title FROM {CHARACTERS} ORDER BY fname",
    AFFILIATIONS: f"SELECT id, name FROM {AFFILIATIONS} ORDER BY name",
    ACTORS: f"SELECT id, fname, lname, birthday, imdb FROM {ACTORS} ORDER BY fname",
    SERIES: f"SELECT id, name, start_date, end_date FROM {SERIES} ORDER BY name",
    LOCATIONS: f"SELECT id, name, type FROM {LOCATIONS} ORDER BY name"
}