from flask import Flask, render_template, request
from config import SECRET, TABLES, TABLES_LIST
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


@app.route("/add-species", methods=["GET", "POST"])
def add_species():
    form = SingleFieldForm()
    form.first_field.label = "Species Name: "
    query_res = []
    db = connect_to_database()
    columns = ["Species"]

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""

        query = "INSERT INTO species(name) VALUES (%s)"
        data = tuple([name])
        res = execute_query(db, query, data)

    if "delete_no" in request.args:
        delete_row(columns[0].lower(), db, request.args["delete_no"])

    query = "SELECT id, name FROM species"
    res = execute_query(db, query)

    for item in res:
        query_res.append(Row(item[0], item[1:]))

    return render_template("single_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add a new species to the database", target="add-species")


@app.route("/add-affiliations", methods=["GET", "POST"])
def add_affiliations():
    form = SingleFieldForm()
    form.first_field.label = "Affiliation Name: "
    query_res = []
    db = connect_to_database()
    columns = ["Affiliation"]

    if form.validate_on_submit():
        name = str(form.first_field.data)
        form.first_field.data = ""

        query = "INSERT INTO affiliations(name) VALUES (%s)"
        data = tuple([name])
        res = execute_query(db, query, data)

    if "delete_no" in request.args:
        delete_row(columns[0].lower(), db, request.args["delete_no"])

    query = "SELECT id, name FROM affiliations"
    res = execute_query(db, query)

    for item in res:
        query_res.append(Row(item[0], item[1:]))

    return render_template("single_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add a new affiliation to the database", target="add-affiliations")


@app.route("/add-series", methods=["GET", "POST"])
def add_series():
    form = SeriesForm()
    form.first_field.label = "Series Name: "
    form.second_field.label = "Series Start Date: "

    form.third_field.label = "Series End Date: "

    query_res = []
    db = connect_to_database()
    columns = ["Series", "Start Date", "End Date"]

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
        delete_row(columns[0].lower(), db, request.args["delete_no"])

    query = "SELECT id, name, start_date, end_date FROM series"
    res = execute_query(db, query)

    for item in res:
        row_id = item[0]
        item = list(item[1:])

        for i in range(1, 3):
            temp_date = str(item[i]).split("-")
            temp_date = temp_date[1:] + [temp_date[0]]
            item[i] = "-".join(temp_date)

        query_res.append(Row(row_id, item))

    return render_template("triple_field_add_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header="Add a new series to the database", target="add-series")


@app.route("/add-location", methods=["GET", "POST"])
def add_location():
    form = LocationForm()
    form.first_field.label = "Location Name: "
    form.second_field.label = "Location Type: "


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
def home():
    return "<h1>Welcome to the site</h1>"


def sanitze_input(user_input):
    pass


def delete_row(table_name, connection, row_num):
    query = f"DELETE FROM {table_name} WHERE id = {row_num}"
    res = execute_query(connection, query)


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

