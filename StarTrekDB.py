from flask import Flask, render_template, request
from config import SECRET, TABLES
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET

@app.route("/create-table")
def create_table():
    table = request.args.get("table")
    db = connect_to_database()
    query = f"DROP TABLE IF EXISTS {table};"
    results = execute_query(db, query)
    print(results)
    query = TABLES[table]
    results = execute_query(db, query)
    print(results)
    query = f"DESCRIBE {table};"
    results = execute_query(db, query)

@app.route("/")
def home():
    return "<h1>Welcome to the site</h1>"
