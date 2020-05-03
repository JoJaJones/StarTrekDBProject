from flask import Flask, render_template, request
from config import SECRET, TABLES
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET

@app.route("/create-all-tables")
def init_DB():
    password = request.args.get("pass")
    results = "Invalid password"
    if password == "picard":
        results = "Tables created: "
        db = connect_to_database()
        for table in TABLES:
            query = f"DROP TABLE IF ExISTS {table};"
            results = execute_query(db, query)
            query = TABLES[table]
            results = execute_query(db, query)
            if results[-2] != ":":
                results += ", "

            results += table

    return results



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
