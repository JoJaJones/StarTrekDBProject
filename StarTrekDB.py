from flask import Flask, render_template, request, redirect, url_for, session
from constants import *
from db_connector.db_connector import connect_to_database, execute_query
from STForms import *

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET

@app.route("/create-all-tables")
def init_DB():
    """
    function to delete all existing tables and create new ones. Requires a password passed to the
    url in the pass argument to process the DB reset

    :return:
    """
    password = request.args.get("pass")
    result = "Invalid password"
    if password in ("picard","kirk"):
        result = "Tables created: "
        db = connect_to_database()
        for i in range(len(TABLES_LIST)-1, -1, -1):
            if TABLES_LIST[i] in TABLES:
                query = f"DROP TABLE IF EXISTS {TABLES_LIST[i]};"
                execute_query(db, query)

        for table in TABLES_LIST:
            if table in TABLES:
                query = TABLES[table]
                res = execute_query(db, query)

                if result[-2] != ":":
                    result += ", "

                result += table

    if password == "kirk":
        for stmt in PREPOPULATE:
            db.cursor().execute(PREPOPULATE[stmt])
        db.commit()
        result += '<br>Data pre-populated in tables'

    return result

@app.route("/", methods=["GET","POST"])
def index():
    db = connect_to_database()
    header = 'Browse Characters'
    columns = VIEW_COLUMNS[CHARACTERS][:]
    submitted = False
    FnameSearchForm = SearchByFnameForm()
    LnameSearchForm = SearchByLnameForm()
    SpeciesFilterForm = FilterBySpecies()
    # Populate species list with query
    query = "SELECT id, name FROM species ORDER BY name"
    res = execute_query(db, query)
    species_list = []
    for species in res:
        species_list.append((species[0], species[1]))
    SpeciesFilterForm.species_field.choices = species_list    

    if FnameSearchForm.validate_on_submit():        
        submitted = True
        fname = str(FnameSearchForm.fname_field.data)
        query_res = select_query(db, f"SELECT id, fname, lname, alias, title FROM {CHARACTERS} WHERE fname='{fname}' ORDER BY fname", CHARACTERS)
    elif LnameSearchForm.validate_on_submit():
        submitted = True
        lname = str(LnameSearchForm.lname_field.data)
        query_res = select_query(db, f"SELECT id, fname, lname, alias, title FROM {CHARACTERS} WHERE lname='{lname}' ORDER BY fname", CHARACTERS)
    elif SpeciesFilterForm.validate_on_submit():
        submitted = True
        species = SpeciesFilterForm.species_field.data
        speciesList = ""
        for e in species:
            speciesList += str(e)
        speciesList = ','.join(speciesList)
        query = f"SELECT DISTINCT C.id, fname, lname, alias, title FROM {CHARACTERS} C \
                  JOIN characters_species CS ON CS.cid=C.id \
                  JOIN species S ON S.id=CS.sid WHERE S.id in ({speciesList}) ORDER BY fname"
        print(query)
        query_res = select_query(db, query, CHARACTERS)

    # Get basic character info for the columns defined in VIEW_COLUMNS
    if not submitted:
        query_res = select_query(db, BASIC_SELECT_QUERIES[CHARACTERS], CHARACTERS)

    # pass data necessary to generate table
    return render_template("search_table_display.html", FnameSearchForm=FnameSearchForm, LnameSearchForm=LnameSearchForm,
                            SpeciesFilterForm=SpeciesFilterForm, query_res=query_res, column_names=columns, query_has_value=(len(query_res) > 0),
                            header=header, target="/add-characters")


@app.route("/add-species", methods=["GET", "POST"])
def add_species():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = SingleFieldForm()
    form.first_field.label.text = "Species Name"

    db = connect_to_database()
    columns = VIEW_COLUMNS[SPECIES]
    header = "Add New Species"

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != SPECIES:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""

        if session[SUBMIT_TYPE] == "insert":
            query = f"INSERT INTO {SPECIES}(name) VALUES (%s)"
        else:
            query = f"UPDATE {SPECIES} SET name = %s WHERE id = {session['update_id']}"
            session[SUBMIT_TYPE] = "insert"
        data = tuple([name])
        res = execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[SPECIES], SPECIES)

        return render_template("single_field_add_form.html", form=form, query_res=query_res,
                               column_names=columns, query_has_value=(len(query_res) > 0),
                               header=header, target="add-species")

    if "delete_no" in request.args:
        delete_row(SPECIES, db, request.args["delete_no"])

    if "update_no" in request.args:
        query = f"SELECT * FROM {SPECIES} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = SPECIES
            form.first_field.data = f"{res[1]}"
            header = f"Update {res[1]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[SPECIES], SPECIES)

    return render_template("single_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-species")

@app.route("/browse-affiliations", methods=["GET", "POST"])
def browse_affiliations():
    # create database connection
    db = connect_to_database()

    # set table columns using the dictionary in constants
    columns = VIEW_COLUMNS[AFFILIATIONS]

    # get results of query
    query_res = select_query(db, BASIC_SELECT_QUERIES[AFFILIATIONS], AFFILIATIONS)

    # pass data necessary to generate table
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-affiliations")

@app.route("/add-affiliations", methods=["GET", "POST"])
def add_affiliation():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = SingleFieldForm()
    form.first_field.label.text = "Affiliation Name"
    query_res = []
    db = connect_to_database()
    columns = VIEW_COLUMNS[AFFILIATIONS]
    header = "Add New Affiliation"

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != AFFILIATIONS:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""

        if session[SUBMIT_TYPE] == "insert":
            query = f"INSERT INTO {AFFILIATIONS}(name) VALUES (%s)"
        else:
            query = f"UPDATE {AFFILIATIONS} SET name = %s WHERE id = {session['update_id']}"
            session[SUBMIT_TYPE] = "insert"
        data = tuple([name])
        res = execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[AFFILIATIONS], AFFILIATIONS)

        return render_template("single_field_add_form.html", form=form, query_res=query_res,
                               column_names=columns, query_has_value=(len(query_res) > 0),
                               header=header, target="add-affiliations")

    if "delete_no" in request.args:
        delete_row(AFFILIATIONS, db, request.args["delete_no"])

    if "update_no" in request.args:
        query = f"SELECT * FROM {AFFILIATIONS} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = AFFILIATIONS
            form.first_field.data = f"{res[1]}"
            header = f"Update {res[1]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[AFFILIATIONS], AFFILIATIONS)

    return render_template("single_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-affiliations")


@app.route("/browse-series", methods=["GET", "POST"])
def browse_series():
    # create database connection
    db = connect_to_database()

    # set table columns using the dictionary in constants
    columns = VIEW_COLUMNS[SERIES]

    # get results of query
    query_res = select_query(db, BASIC_SELECT_QUERIES[SERIES], SERIES)

    # pass data necessary to generate table
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-series")

@app.route("/add-series", methods=["GET", "POST"])
def add_series():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = SeriesForm()
    form.second_field.label.text = "Series Start Date"

    form.third_field.label.text = "Series End Date"

    db = connect_to_database()
    columns = VIEW_COLUMNS[SERIES]
    header = "Add New Series"

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != SERIES:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""
        start = form.second_field.data
        end = form.third_field.data
       
        # validate the date data entered by the user and then format it for entry to DB
        start_valid = sanitize_date(start)
        start = f"{start['year']}-{start['month']}-{start['day']}"

        # validate the date data entered by the user and then format it for entry to DB
        end_valid = sanitize_date(end)
        end = f"{end['year']}-{end['month']}-{end['day']}"
        
        # Alter queries & data if fields are missing
        if start_valid and end_valid:
            case = 0
            data = (name, start, end)
        elif start_valid:
            case = 1
            data = (name, start)
        elif end_valid:
            case = 2
            data = (name, end)
        else:
            case = 3
            data = (name)    
        
        if session[SUBMIT_TYPE] == "insert":
            query = SERIES_INSERT_QUERIES[case]
        else:
            data = data + tuple([session["update_id"]])
            query = SERIES_UPDATE_QUERIES[case]            
            session[SUBMIT_TYPE] = "insert"
        res = execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[SERIES], SERIES)
        for item in query_res:
            for i in range(1, 3):
                item.reformat_date(i)

        return redirect(url_for("add_series"))

    if "delete_no" in request.args:
        delete_row(SERIES, db, request.args["delete_no"])

    if "update_no" in request.args:
        query = f"SELECT * FROM {SERIES} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = SERIES
            form.first_field.data = f"{res[1]}"
            # Dates could be empty
            if res[2]:
                form.second_field.form.year.data = res[2].year
                form.second_field.form.month.data = res[2].month
                form.second_field.form.day.data = res[2].day
            if res[3]:
                form.third_field.form.year.data = res[3].year
                form.third_field.form.month.data = res[3].month
                form.third_field.form.day.data = res[3].day
            header = f"Update {res[1]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[SERIES], SERIES)
    for item in query_res:
        for i in range(1, 3):
            item.reformat_date(i)

    return render_template("add_series_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-series")


@app.route("/browse-locations", methods=["GET", "POST"])
def browse_locations():
    # create database connection
    db = connect_to_database()

    # set table columns using the dictionary in constants
    columns = VIEW_COLUMNS[LOCATIONS]

    # get results of query
    query_res = select_query(db, BASIC_SELECT_QUERIES[LOCATIONS], LOCATIONS)

    # pass data necessary to generate table
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-location")


@app.route("/add-location", methods=["GET", "POST"])
def add_location():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = LocationForm()
    form.first_field.label = "Location Name"
    form.second_field.label = "Location Type"
    columns = VIEW_COLUMNS[LOCATIONS]
    header = "Add New Location"

    db = connect_to_database()

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != LOCATIONS:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""
        type = form.second_field.data
        form.second_field.data = None

        if session[SUBMIT_TYPE] == "insert":
            query = f"INSERT INTO {LOCATIONS}(name, type) VALUES (%s, %s)"
        else:
            query = f"UPDATE {LOCATIONS} SET name = %s, type = %s WHERE id = {session['update_id']}"
            session[SUBMIT_TYPE] = "insert"

        data = (name, type)
        res = execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[LOCATIONS], LOCATIONS)
        for item in query_res:
            item.table_values[1] = LOCATION_TYPE_DICT[item.table_values[1]]

        return render_template("add_location_form.html", form=form, query_res=query_res,
                               column_names=columns, query_has_value=(len(query_res) > 0),
                               header=header, target="add-location")

    if "delete_no" in request.args:
        delete_row(LOCATIONS, db, request.args["delete_no"])

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {LOCATIONS} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = LOCATIONS
            form.first_field.data = f"{res[1]}"
            form.second_field.data = f"{res[2]}"
            header = f"Update {res[1]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[LOCATIONS], LOCATIONS)
    for item in query_res:
        item.table_values[1] = LOCATION_TYPE_DICT[item.table_values[1]]

    return render_template("add_location_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-location")


@app.route("/browse-characters", methods=["GET", "POST"])
def browse_characters():
    # create database connection
    db = connect_to_database()

    # set table columns using the dictionary in constants
    columns = VIEW_COLUMNS[CHARACTERS][:]


    # determine if species has data that might need to be displayed
    query = "SELECT id, name FROM species ORDER BY name"
    res = execute_query(db, query)
    species_list = []
    for species in res:
        species_list.append((species[0], species[1]))
    display_species = len(species_list) > 0
    if display_species:
        columns.append("Species")

    # determine if series has data that might need to be displayed
    query = "SELECT id, name FROM series ORDER BY name"
    res = execute_query(db, query)
    series_list = []
    for series in res:
        series_list.append((series[0], series[1]))
    display_series = len(series_list) > 0
    if display_series:
        columns.append("Series")

    # get results of query
    query_res = select_query(db, BASIC_SELECT_QUERIES[CHARACTERS], CHARACTERS)
    for item in query_res:  # append blank spaces to characters if species and series exist
        # TODO add queries to set these values instead of adding a blank value to the data set
        if display_series:
            item.temp_char_buffer()
        if display_species:
            item.temp_char_buffer()

    # pass data necessary to generate table
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-characters")


@app.route("/add-character", methods=["GET", "POST"])
def add_character():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = CharacterForm()

    db = connect_to_database()
    columns = VIEW_COLUMNS[CHARACTERS][:]
    header = "Add New Character"

    query = "SELECT id, name FROM species ORDER BY name"
    res = execute_query(db, query)
    species_list = []
    for species in res:
        species_list.append((species[0], species[1]))
    form.sixth_field.choices = species_list
    display_species = len(species_list) > 0
    if display_species:
        columns.append("Species")

    query = "SELECT id, name FROM series ORDER BY name"
    res = execute_query(db, query)
    series_list = []
    for series in res:
        series_list.append((series[0], series[1]))
    form.seventh_field.choices = series_list
    display_series = len(series_list) > 0
    if display_series:
        columns.append("Series")

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != CHARACTERS:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        first_name = form.first_field.data
        form.first_field.data = ""
        last_name = form.second_field.data
        form.second_field.data = ""
        title = form.third_field.data
        form.third_field.data = ""
        desc = form.fourth_field.data
        form.fourth_field.data = ""
        bio = form.fifth_field.data
        form.fifth_field.data = ""

        query = "INSERT INTO characters(fname, lname, title, description, biography) VALUES (%s, %s, %s, %s, %s)"
        data = (first_name, last_name, title, desc, bio)
        res = execute_query(db, query, data)

        query = f"SELECT id, fname, lname, title FROM characters " \
                f"WHERE fname = '{first_name}'"
        if last_name:
            query += f" AND lname = '{last_name}'"
        if title:
            query += f" AND title = '{title}'"
        query += ";"

        res = execute_query(db, query).fetchone()

        species = form.sixth_field.data
        form.sixth_field.data = []
        query_template = "INSERT INTO characters_species(cid, sid) VALUES (%s, %s)"
        for spec_id in species:
            link_tables(query_template, db, res[0], spec_id)

        series = form.seventh_field.data
        form.seventh_field.data = []
        query_template = "INSERT INTO characters_series(cid, sid) VALUES (%s, %s)"
        for ser_id in series:
            link_tables(query_template, db, res[0], ser_id)

    if "delete_no" in request.args:
        delete_row(CHARACTERS, db, request.args["delete_no"])

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {CHARACTERS} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = CHARACTERS
            form.first_field.data = f"{res[1]}"
            form.second_field.data = f"{res[2]}"
            form.third_field.data = f"{res[3]}"
            form.fourth_field.data = f"{res[4]}"
            form.fifth_field.data = f"{res[5]}"
            header = f"Update {res[1]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[CHARACTERS], CHARACTERS)
    for item in query_res:
        # TODO add queries to set these values instead of adding a blank value to the data set
        if display_series:
            item.temp_char_buffer()
        if display_species:
            item.temp_char_buffer()

    return render_template("add_char_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, display_species=display_species,
                           display_series=display_series, target="add-character")



@app.route("/browse-actors", methods=["GET", "POST"])
def browse_actors():
    # create database connection
    db = connect_to_database()

    # set table columns using the dictionary in constants
    columns = VIEW_COLUMNS[ACTORS]

    # get results of query
    query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)

    # pass data necessary to generate table
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-actors")

@app.route("/add-actors", methods=["GET", "POST"])
def add_actor():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = AddActorForm()
    db = connect_to_database()
    columns = VIEW_COLUMNS[ACTORS]
    header = "Add New Actor"

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != ACTORS:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        fname = str(form.fname_field.data)
        form.fname_field.data = ""
        lname = str(form.lname_field.data)
        form.lname_field.data = ""
        birthday = str(form.birthday_field.data).replace('/','-')
        form.birthday_field.data = ""
        imdb = str(form.imdb_field.data)
        form.imdb_field.data = ""

        if session[SUBMIT_TYPE] == "insert":
            query = f"INSERT INTO {ACTORS}(fname, lname, birthday, imdb) VALUES (%s, %s)"
        else:
            query = f"UPDATE {ACTORS} SET fname = %s, lname = %s, birthday = %s, imdb = %s WHERE id = {session['update_id']}"
            session[SUBMIT_TYPE] = "insert"

        print(birthday)
        data = tuple([fname,lname,birthday,imdb])
        execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)

        return render_template("add_actor_form.html", form=form, query_res=query_res,
                               column_names=columns, query_has_value=(len(query_res) > 0),
                               header=header, target="add-actors")

    if "delete_no" in request.args:
        delete_row(ACTORS, db, request.args["delete_no"])

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {ACTORS} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = ACTORS
            form.fname_field.data = res[1]
            form.lname_field.data = res[2]
            print(res[3])
            form.birthday_field.data = res[3]
            form.imdb_field.data = res[4]
            header = f"Update {res[1]} {res[2]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)

    return render_template("add_actor_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-actors")

@app.route("/edit-actors", methods=["GET", "POST"])
def edit_actor():
    db = connect_to_database()
    form = AddActorForm()
    id = request.args['id']
    fname = str(form.fname_field.data)
    lname = str(form.lname_field.data)
    birthday = str(form.birthday_field.data).replace('/','-')
    imdb = str(form.imdb_field.data)
    query = f"UPDATE {ACTORS} SET fname=(%s),lname=(%s),birthday=(%s),imdb=(%s) WHERE id={id}"
    data = tuple([fname,lname,birthday,imdb])
    execute_query(db, query, data)   

    return redirect(url_for('add_actor'))


@app.route("/connect-actor-char", methods=["GET", "POST"])
def link_actor_char():
    return render_template("link_relationships.html", header="Enter a Character and Actor to link", form=True,
                           field_one_text="Character Name", field_two_text="Actor Name")


@app.route("/connect-char-spec", methods=["GET", "POST"])
def link_char_species():
    return render_template("link_relationships.html", header="Enter a Character and Species to link", form=True,
                           field_one_text="Character Name", field_two_text="Species Name")


@app.route("/connect-char-aff", methods=["GET", "POST"])
def link_char_aff():
    return render_template("link_relationships.html", header="Enter a Character and Affiliation to link", form=True,
                           field_one_text="Character Name", field_two_text="Affiliation Name")


@app.route("/connect-char-series", methods=["GET", "POST"])
def link_char_series():
    return render_template("link_relationships.html", header="Enter a Character and Series to link", form=True,
                           field_one_text="Character Name", field_two_text="Series Name")


@app.route("/connect-location", methods=["GET", "POST"])
def link_to_location():
    return render_template("link_three.html", header="Enter a Character/Series combination to link to a Location", form=True,
                           field_one_text="Character Name", field_two_text="Series Name", field_three_text="Location Name")


@app.route("/create-table")
def create_table():
    """
    Function to create the table specified in the url table argument

    :return:
    """

    table = request.args.get("table")
    db = connect_to_database()
    query = f"DROP TABLE IF EXISTS {table};"
    results = execute_query(db, query)
    query = TABLES[table]
    results = execute_query(db, query)
    return f"{table} table created"



@app.route("/char-search")
def search_char():
    return render_template("SearchChar.html")


# TODO implement function to prevent SQL injections as needed
def sanitze_input(user_input):
    pass


def sanitize_date(date_dict: dict):
    """
    Function to take the date values entered by the user and check their validity. If valid it returns True,
    otherwise it sets the values to None and returns False

    :param date_dict:
    :return:
    """
    month = date_dict["month"]
    day = date_dict["day"]
    year = date_dict["year"]
    date = [month, day, year]

    date_is_valid = not any([component is None for component in date])
    if date_is_valid:
        date_is_valid &= not (month == 2 and day > 29)
        date_is_valid &= not (month in [4, 6, 9, 11] and day > 30)
        is_leap_year = (year % 4) == 0
        is_leap_year &= ((year % 100) != 0 or (year % 400) == 0)
        date_is_valid &= not (month == 2 and day == 29 and not is_leap_year)

    if not date_is_valid:
        date_dict["month"] = date_dict["day"] = date_dict["year"] = None
        return False

    return True


def link_tables(query_template, connection, id_one, id_two, id_three=None):
    """
    Function to create the connections in M:M relationships in the database
    takes a string in the format:
    INSERT INTO table_name(id_one_attribute_name, id_two_attribute_name) VALUES (%s, %s)
    for the query and interpolates the data and calls the appropriate query


    :param query_template:
    :param connection:
    :param id_one:
    :param id_two:
    :param id_three:
    :return:
    """
    data = [id_one, id_two]
    if id_three is not None:
        data += [id_three]

    data = tuple(data)

    execute_query(connection, query_template, data)


def delete_row(table_name, connection, row_num):
    """
    Function to delete the selected row from the table

    :param table_name:
    :param connection:
    :param row_num:
    :return:
    """
    query = f"DELETE FROM {table_name} WHERE id = {row_num}"
    res = execute_query(connection, query)


def select_query(connection, query, data_type):
    """
    Function to perform the select query passed to it and return a list of row objects
    representing the results of the query

    :param connection:
    :param query:
    :param data_type:
    :return:
    """

    # perform passed query
    query_res = []
    res = execute_query(connection, query)

    # prepare and format the results
    for item in res:
        query_res.append(Row(item[0], list(item[1:]), data_type))

    return query_res

# TODO implement
def load_data_page(row_item):
    print(row_item, row_item.id)


if __name__=="__main__":
    app.run(debug=True)
