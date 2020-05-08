from flask import Flask, render_template, request
from constants import *
from db_connector.db_connector import connect_to_database, execute_query
from STForms import *

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET


@app.route("/create-all-tables")
def init_DB():
    password = request.args.get("pass")
    result = "Invalid password"
    if password == "picard":
        result = "Tables created: "
        db = connect_to_database()
        for i in range(len(TABLES_LIST)-1, -1, -1):
            if TABLES_LIST[i] in TABLES:
                # print(TABLES_LIST[i])
                query = f"DROP TABLE IF EXISTS {TABLES_LIST[i]};"
                res = execute_query(db, query)

        for table in TABLES_LIST:
            if table in TABLES:
                # print(table)
                query = TABLES[table]
                res = execute_query(db, query)
                print(res)
                if result[-2] != ":":
                    result += ", "

                result += table

    return result

@app.route("/browse-species", methods=["GET", "POST"])
def browse_species():
    db = connect_to_database()
    columns = VIEW_COLUMNS[SPEC]

    query_res = select_query(db, BASIC_SELECT_QUERIES[SPEC], SPEC)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")

@app.route("/add-species", methods=["GET", "POST"])
def add_species():
    form = SingleFieldForm()
    form.first_field.label = "Species Name: "
    query_res = []
    db = connect_to_database()
    columns = VIEW_COLUMNS[SPEC]

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""

        query = "INSERT INTO species(name) VALUES (%s)"
        data = tuple([name])
        res = execute_query(db, query, data)

    if "delete_no" in request.args:
        delete_row(SPEC, db, request.args["delete_no"])

    query_res = select_query(db, BASIC_SELECT_QUERIES[SPEC], SPEC)

    return render_template("single_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add New Species", target="add-species")

@app.route("/browse-affiliations", methods=["GET", "POST"])
def browse_affiliations():
    db = connect_to_database()
    columns = VIEW_COLUMNS[AFF]

    query_res = select_query(db, BASIC_SELECT_QUERIES[AFF], AFF)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")

@app.route("/add-affiliations", methods=["GET", "POST"])
def add_affiliation():
    form = SingleFieldForm()
    form.first_field.label = "Affiliation Name: "
    query_res = []
    db = connect_to_database()
    columns = VIEW_COLUMNS[AFF]

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""

        query = "INSERT INTO affiliations(name) VALUES (%s)"
        data = tuple([name])
        res = execute_query(db, query, data)

    if "delete_no" in request.args:
        delete_row(AFF, db, request.args["delete_no"])

    query_res = select_query(db, BASIC_SELECT_QUERIES[AFF], AFF)

    return render_template("single_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add New Affiliation", target="add-affiliations")


@app.route("/browse-series", methods=["GET", "POST"])
def browse_series():
    db = connect_to_database()
    columns = VIEW_COLUMNS[SER]

    query_res = select_query(db, BASIC_SELECT_QUERIES[SER], SER)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")

@app.route("/add-series", methods=["GET", "POST"])
def add_series():
    form = SeriesForm()
    form.second_field.label = "Series Start Date"

    form.third_field.label = "Series End Date"

    db = connect_to_database()
    columns = VIEW_COLUMNS[SER]

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
        delete_row(SER, db, request.args["delete_no"])

    query_res = select_query(db, BASIC_SELECT_QUERIES[SER], SER)
    for item in query_res:
        for i in range(1, 3):
            item.reformat_date(i)

    return render_template("add_series_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add New Series", target="add-series")


@app.route("/browse-locations", methods=["GET", "POST"])
def browse_locations():
    db = connect_to_database()
    columns = VIEW_COLUMNS[LOC]

    query_res = select_query(db, BASIC_SELECT_QUERIES[LOC], LOC)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="", target="add-species")


@app.route("/add-location", methods=["GET", "POST"])
def add_location():
    form = LocationForm()
    form.first_field.label = "Location Name"
    form.second_field.label = "Location Type"
    columns = VIEW_COLUMNS[LOC]

    db = connect_to_database()
    print(form.second_field.choices)

    query_res = select_query(db, BASIC_SELECT_QUERIES[LOC], LOC)
    return render_template("add_location_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add New Location", target="add-location")


@app.route("/browse-characters", methods=["GET", "POST"])
def browse_characters():
    db = connect_to_database()
    columns = VIEW_COLUMNS[CHAR][:]

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

    query_res = select_query(db, BASIC_SELECT_QUERIES[CHAR], CHAR)
    for item in query_res:
        # TODO add queries to set these values instead of adding a blank value to the data set
        if display_series:
            item.temp_char_buffer()
        if display_species:
            item.temp_char_buffer()

    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add New Species", target="add-species")


@app.route("/add-character", methods=["GET", "POST"])
def add_character():
    form = CharacterForm()
    query_res = []
    db = connect_to_database()
    columns = VIEW_COLUMNS[CHAR][:]
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
        delete_row(CHAR, db, request.args["delete_no"])

    query_res = select_query(db, BASIC_SELECT_QUERIES[CHAR], CHAR)
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
    columns = VIEW_COLUMNS[ACT]

    query_res = select_query(db, BASIC_SELECT_QUERIES[ACT], ACT)
    return render_template("single_table_display.html", form=False, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add New Species", target="add-species")


@app.route("/add-actor", methods=["GET", "POST"])
def add_actor():
    return render_template("AddActor.html")


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
    table = request.args.get("table")
    db = connect_to_database()
    query = f"DROP TABLE IF ExISTS {table};"
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

def sanitze_input(user_input):
    pass

def sanitize_date(date_dict: dict):
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
    data = [id_one, id_two]
    if id_three is not None:
        data += [id_three]

    data = tuple(data)

    execute_query(connection, query_template, data)


def delete_row(table_name, connection, row_num):
    query = f"DELETE FROM {table_name} WHERE id = {row_num}"
    res = execute_query(connection, query)


def select_query(connection, query, data_type):
    query_res = []
    res = execute_query(connection, query)
    for item in res:
        query_res.append(Row(item[0], list(item[1:], data_type)))

    return query_res


def load_data_page(row_item):
    print(row_item, row_item.id)
