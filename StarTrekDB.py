from flask import Flask, render_template, request, redirect, url_for, session
from constants import *
from db_connector.db_connector import connect_to_database, execute_query
from STForms import *

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET


@app.route("/create-all-tables")
def init_DB():
    password = request.args.get("pass")
    result = "Invalid password"
    if password in ("picard","kirk"):
        result = "Tables created: "
        db = connect_to_database()
        for i in range(len(TABLES_LIST)-1, -1, -1):
            if TABLES_LIST[i] in TABLES:
                # print(TABLES_LIST[i])
                query = f"DROP TABLE IF EXISTS {TABLES_LIST[i]};"
                execute_query(db, query)

        for table in TABLES_LIST:
            if table in TABLES:
                # print(table)
                query = TABLES[table]
                res = execute_query(db, query)
                print(res)
                if result[-2] != ":":
                    result += ", "

                result += table

    if password == "kirk":
        for stmt in PREPOPULATE:
            db.cursor().execute(PREPOPULATE[stmt])
        db.commit()
        result += '<br>Data pre-populated in tables'

    return result

@app.route("/browse-species", methods=["GET", "POST"])
def browse_species():
    db = connect_to_database()
    columns = VIEW_COLUMNS[SPECIES]

    query_res = select_query(db, BASIC_SELECT_QUERIES[SPECIES], SPECIES)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")

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
    db = connect_to_database()
    columns = VIEW_COLUMNS[AFFILIATIONS]

    query_res = select_query(db, BASIC_SELECT_QUERIES[AFFILIATIONS], AFFILIATIONS)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")

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
    db = connect_to_database()
    columns = VIEW_COLUMNS[SERIES]

    query_res = select_query(db, BASIC_SELECT_QUERIES[SERIES], SERIES)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")

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
        form.second_field.data.clear()
        end = form.third_field.data
        form.third_field.data.clear()

        sanitize_date(start)
        start = f"{start['year']}-{start['month']}-{start['day']}"

        sanitize_date(end)
        end = f"{end['year']}-{end['month']}-{end['day']}"

        if session[SUBMIT_TYPE] == "insert":
            query = f"INSERT INTO {SERIES}(name, start_date, end_date) VALUES (%s, %s, %s)"
        else:
            query = f"UPDATE {SERIES} SET name = %s, start_date = %s, end_date = %s WHERE id = {session['update_id']}"
            session[SUBMIT_TYPE] = "insert"
        data = tuple([name])
        res = execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[SERIES], SERIES)
        for item in query_res:
            for i in range(1, 3):
                item.reformat_date(i)

        return render_template("add_series_form.html", form=form, query_res=query_res,
                               column_names=columns, query_has_value=(len(query_res) > 0),
                               header=header, target="add-series")

    if "delete_no" in request.args:
        delete_row(SERIES, db, request.args["delete_no"])

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {SERIES} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        print(res)
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = SERIES
            form.first_field.data = f"{res[1]}"
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
    db = connect_to_database()
    columns = VIEW_COLUMNS[LOCATIONS]

    query_res = select_query(db, BASIC_SELECT_QUERIES[LOCATIONS], LOCATIONS)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")


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
    print(form.second_field.choices)

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != LOCATIONS:
        session[SUBMIT_TYPE] = "insert"

    # TODO *********************************************************************
    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""
        start = form.second_field.data
        form.second_field.data.clear()
        end = form.third_field.data
        form.third_field.data.clear()

        sanitize_date(start)
        start = f"{start['year']}-{start['month']}-{start['day']}"

        sanitize_date(end)
        end = f"{end['year']}-{end['month']}-{end['day']}"

        query = "INSERT INTO series(name, start_date, end_date) VALUES (%s, %s, %s)"
        data = (name, start, end)
        res = execute_query(db, query, data)

    if "delete_no" in request.args:
        delete_row(SERIES, db, request.args["delete_no"])

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {LOCATIONS} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = LOCATIONS
            form.first_field.data = f"{res[1]}"
            header = f"Update {res[1]}"
    # TODO *********************************************************************

    query_res = select_query(db, BASIC_SELECT_QUERIES[LOCATIONS], LOCATIONS)
    return render_template("add_location_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-location")


@app.route("/browse-characters", methods=["GET", "POST"])
def browse_characters():
    db = connect_to_database()
    columns = VIEW_COLUMNS[CHARACTERS][:]
    header = "Add New Species"

    query = "SELECT id, name FROM species ORDER BY name"
    res = execute_query(db, query)
    species_list = []
    for species in res:
        species_list.append((species[0], species[1]))
    display_species = len(species_list) > 0
    if display_species:
        columns.append("Species")

    query = "SELECT id, name FROM series ORDER BY name"
    res = execute_query(db, query)
    series_list = []
    for series in res:
        series_list.append((series[0], series[1]))
    display_series = len(series_list) > 0
    if display_series:
        columns.append("Series")

    query_res = select_query(db, BASIC_SELECT_QUERIES[CHARACTERS], CHARACTERS)
    for item in query_res:
        # TODO add queries to set these values instead of adding a blank value to the data set
        if display_series:
            item.temp_char_buffer()
        if display_species:
            item.temp_char_buffer()

    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-species")


@app.route("/add-character", methods=["GET", "POST"])
def add_character():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = CharacterForm()
    query_res = []
    db = connect_to_database()
    columns = VIEW_COLUMNS[CHARACTERS][:]
    print(form.first_field.label.text)

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
                           header="Add New Character", display_species=display_species,
                           display_series=display_series, target="add-character")



@app.route("/browse-actors", methods=["GET", "POST"])
def browse_actors():
    db = connect_to_database()
    columns = VIEW_COLUMNS[ACTORS]

    query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)
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

    if "update_no" in request.args:
        id = request.args['update_no']
        query = f"SELECT fname,lname,birthday,imdb FROM {ACTORS} WHERE id={id}"
        res = execute_query(db, query).fetchall()
        res = res[0]
        form.fname_field.data = res[0]
        form.lname_field.data = res[1]
        form.birthday_field.data = str(res[2]).replace('-','/')
        form.imdb_field.data = res[3]

        return render_template("AddActor.html", form=form, query_res=None,
                           column_names=columns, query_has_value=False,
                           header="Edit New Actor", updating=True, id=id)

    if form.validate_on_submit():
        fname = str(form.fname_field.data)
        form.fname_field.data = ""
        lname = str(form.lname_field.data)
        form.lname_field.data = ""
        birthday = str(form.birthday_field.data).replace('/','-')
        form.birthday_field.data = ""
        imdb = str(form.imdb_field.data)
        form.imdb_field.data = ""


        query = f"INSERT INTO {ACTORS} (fname,lname,birthday,imdb) VALUES (%s, %s, %s, %s)"
        data = tuple([fname,lname,birthday,imdb])
        execute_query(db, query, data)

        query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)

        return render_template("AddActor.html", form=form, query_res=query_res,
                               column_names=columns, query_has_value=(len(query_res) > 0),
                               header=header, target="add-actors", updating=False)

    if "delete_no" in request.args:
        delete_row(ACTORS, db, request.args["delete_no"])

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {SPECIES} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        session["update_id"] = res[0]
        session[SUBMIT_TYPE] = "update"
        session["update_page"] = SPECIES
        form.first_field.data = f"{res[1]}"
        header = f"Update {res[1]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)

    return render_template("AddActor.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-actors", updating=False)

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
    return render_template("LinkActorChar.html")


@app.route("/connect-char-spec", methods=["GET", "POST"])
def link_char_species():
    return render_template("LinkCharSpecies.html")


@app.route("/connect-char-aff", methods=["GET", "POST"])
def link_char_aff():
    return render_template("LinkCharAff.html")


@app.route("/connect-char-series", methods=["GET", "POST"])
def link_char_series():
    return render_template("LinkCharSeries.html")


@app.route("/connect-location", methods=["GET", "POST"])
def link_to_location():
    return render_template("LinkCharSeriesLocation.html")


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


@app.route("/")
def index():
    return render_template("landing_page.html")


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
        print((item[0], list(item[1:]), data_type))
        query_res.append(Row(item[0], list(item[1:]), data_type))

    return query_res

# TODO implement
def load_data_page(row_item):
    print(row_item, row_item.id)


if __name__=="__main__":
    app.run(debug=True)
