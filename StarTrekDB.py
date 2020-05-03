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
                query = f"DROP TABLE IF EXISTS {TABLES_LIST[i]};"
                res = execute_query(db, query)

        for table in TABLES_LIST:
            if table in TABLES:
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
    form.field.label = "Species Name: "
    query_res = False
    db = connect_to_database()
    columns = ["Species"]

    if form.validate_on_submit():
        species = str(form.field.data)
        form.field.data = ""

        query = "INSERT INTO species(name) VALUES (%s)"
        res = execute_query(db, query, tuple([species]))

    if "delete_no" in request.args:
        query = f"DELETE FROM species WHERE id = {request.args['delete_no']}"
        res = execute_query(db, query)

    query = "SELECT id, name FROM species"
    res = execute_query(db, query)

    query_res = []
    for item in res:
        query_res.append(Row(item[0], item[1:]))

    return render_template("single_field_add_form.html", form=form, query_res=query_res, column_names=columns)

@app.route("/add-affiliations", methods=["GET", "POST"])
def add_affiliations():
    form = SingleFieldForm()
    form.field.label = "Affiliation Name: "
    query_res = False
    db = connect_to_database()
    columns = ["Affiliation"]

    if form.validate_on_submit():
        species = str(form.field.data)
        form.field.data = ""

        query = "INSERT INTO affiliations(name) VALUES (%s)"
        res = execute_query(db, query, tuple([species]))

    if "delete_no" in request.args:
        query = f"DELETE FROM affiliations WHERE id = {request.args['delete_no']}"
        res = execute_query(db, query)

    query = "SELECT id, name FROM affiliations"
    res = execute_query(db, query)

    query_res = []
    for item in res:
        query_res.append(Row(item[0], item[1:]))

    return render_template("single_field_add_form.html", form=form, query_res=query_res, column_names=columns)



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
