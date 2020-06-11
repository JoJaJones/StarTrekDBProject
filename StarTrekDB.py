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
    form = CharacterSearchForm()    

    # Populate lists with query results
    form.actors.choices = get_select_field_items(db, ACTORS)
    form.species.choices = get_select_field_items(db, SPECIES)
    form.affiliations.choices = get_select_field_items(db, AFFILIATIONS)
    form.series.choices = get_select_field_items(db, SERIES)

    if "clear" in request.args:
        form.fname.data = ''
        form.fname.data = ''
        form.actors.data = []
        form.species.data = []
        form.affiliations.data = []
        form.series.data = []
        return redirect(url_for('index'))

    if form.validate_on_submit():
        query = get_character_search_query(form)
        query_res = select_query(db, query, CHARACTERS)
    else:
        query_res = select_query(db, BASIC_SELECT_QUERIES[CHARACTERS], CHARACTERS)                

    return render_template("search_table_display.html", form=form, query_res=query_res,
                            column_names=columns, query_has_value=(len(query_res) > 0),
                            header=header, target="add-character")

@app.route("/character-display/<int:id>", methods=["GET","POST"])
def display_character(id):
    db = connect_to_database()
    # Get all info about selected character and Display it

    # character table info
    query = f"SELECT fname, lname, alias, title, description, biography FROM {CHARACTERS} WHERE id={id}"
    res_character = execute_query(db, query).fetchone()

    # species table info
    query = f"SELECT S.name FROM {CHARACTERS} C JOIN {CHAR_SPECIES} CS ON CS.cid=C.id JOIN {SPECIES} S ON S.id=CS.sid WHERE C.id={id}"
    species_list = execute_query(db, query).fetchall()

    # affiliations table info
    query = f"SELECT A.name FROM {CHARACTERS} C JOIN {CHAR_AFFILS} CA ON CA.cid=C.id JOIN {AFFILIATIONS} A ON A.id=CA.aid WHERE C.id={id}"
    affiliations_list = execute_query(db, query).fetchall()

    # series table info
    query = f"SELECT S.name FROM {CHARACTERS} C JOIN {CHAR_SERIES} CS ON CS.cid=C.id JOIN {SERIES} S ON S.id=CS.sid WHERE C.id={id}"
    series_list = execute_query(db, query).fetchall()

    # actors table info
    query = f"SELECT A.fname, A.lname FROM {CHARACTERS} C JOIN {ACTORS} A ON A.cid=C.id WHERE C.id={id}"
    actor_list = execute_query(db, query).fetchall()

    return render_template("character_display.html",res_character=res_character, species_list=species_list,
                            affiliations_list=affiliations_list, series_list=series_list, actor_list=actor_list)

@app.route("/add-character", methods=["GET", "POST"])
def add_character():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = CharacterForm()

    db = connect_to_database()
    columns = VIEW_COLUMNS[CHARACTERS][:]
    header = "Add New Character"

    # Get species list
    query = f"SELECT id, name FROM {SPECIES} ORDER BY name"
    res = execute_query(db, query)
    species_list = []
    for species in res:
        species_list.append((species[0], species[1]))
    form.seventh_field.choices = species_list
    display_species = len(species_list) > 0
    """ if display_species:
        columns.append("Species") """
    
    # Get affiliations list
    query = f"SELECT id, name FROM {AFFILIATIONS} ORDER BY name"
    res = execute_query(db, query)
    affiliation_list = []
    for affiliation in res:
        affiliation_list.append((affiliation[0], affiliation[1]))
    form.eighth_field.choices = affiliation_list
    display_affiliations = len(affiliation_list) > 0
    """ if display_species:
        columns.append("Affiliations") """
    
    # Get series list
    query = "SELECT id, name FROM series ORDER BY name"
    res = execute_query(db, query)
    series_list = []
    for series in res:
        series_list.append((series[0], series[1]))
    form.ninth_field.choices = series_list
    display_series = len(series_list) > 0
    """ if display_series:
        columns.append("Series") """

    if UPDATE_PAGE in session and session[UPDATE_PAGE] != CHARACTERS:
        session[SUBMIT_TYPE] = "insert"

    if form.validate_on_submit():
        first_name = form.first_field.data
        form.first_field.data = ""
        last_name = form.second_field.data
        form.second_field.data = ""
        alias = form.third_field.data
        form.third_field.data = ""
        title = form.fourth_field.data
        if len(alias) == 0:
            alias = last_name
            if len(alias) == 0:
                alias = first_name
        form.fourth_field.data = ""
        desc = form.fifth_field.data
        form.fifth_field.data = ""
        bio = form.sixth_field.data
        form.sixth_field.data = ""
        species = form.seventh_field.data
        form.seventh_field.data = []
        affiliations = form.eighth_field.data
        form.eighth_field.data = []
        series = form.ninth_field.data
        form.eighth_field.data = []


        if session[SUBMIT_TYPE] == "insert":
            query = f"INSERT INTO {CHARACTERS} (fname, lname, alias, title, description, biography) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (first_name, last_name, alias, title, desc, bio)
            execute_query(db, query, data)
            # Get the id created for the new row
            query = f"SELECT id FROM {CHARACTERS} WHERE fname = '{first_name}'"
            if last_name:
                query += f" AND lname = '{last_name}'"
            if alias:
                query += f" AND alias = '{alias}'"
            if title:
                query += f" AND title = '{title}'"
            query += ";"
            res = execute_query(db, query).fetchone()
            # Insert Char-Species Links            
            query_template = f"INSERT INTO {CHAR_SPECIES} (cid, sid) VALUES (%s, %s)"
            for spec_id in species:
                link_tables(query_template, db, res[0], spec_id)
            # Insert Char-Affiliation Links            
            query_template = f"INSERT INTO {CHAR_AFFILS} (cid, aid) VALUES (%s, %s)"
            for affil_id in affiliations:
                link_tables(query_template, db, res[0], affil_id)
            # Insert Char-Series Links            
            query_template = f"INSERT INTO {CHAR_SERIES} (cid, sid) VALUES (%s, %s)"
            for ser_id in series:
                link_tables(query_template, db, res[0], ser_id)
        else:
            # Remove all links to species, affiliation, and series because they could be changed
            # Note this will destroy the character-series-location relationships
            # should porably do this by comparing the old vs the new selections (requires a refactor)
            cid = session['update_id']
            query = f"DELETE FROM {CHAR_SPECIES} WHERE cid={cid}"
            execute_query(db, query)
            query = f"DELETE FROM {CHAR_AFFILS} WHERE cid={cid}"
            execute_query(db, query)
            query = f"DELETE FROM {CHAR_SERIES} WHERE cid={cid}"
            execute_query(db, query)
            # Now perform the updates
            query = f"UPDATE {CHARACTERS} SET fname = %s, lname = %s, alias = %s, title = %s, description = %s, biography = %s WHERE id = {cid}"
            data = (first_name, last_name, alias, title, desc, bio)
            execute_query(db, query, data)
            # Insert Char-Species Links            
            query_template = f"INSERT INTO {CHAR_SPECIES} (cid, sid) VALUES (%s, %s)"
            for spec_id in species:
                link_tables(query_template, db, cid, spec_id)
            # Insert Char-Affiliation Links            
            query_template = f"INSERT INTO {CHAR_AFFILS} (cid, aid) VALUES (%s, %s)"
            for affil_id in affiliations:
                link_tables(query_template, db, cid, affil_id)
            # Insert Char-Series Links            
            query_template = f"INSERT INTO {CHAR_SERIES} (cid, sid) VALUES (%s, %s)"
            for ser_id in series:
                link_tables(query_template, db, cid, ser_id)
            session[SUBMIT_TYPE] = "insert"

        return redirect(url_for('add_character'))

    if "delete_no" in request.args:
        delete_row(CHARACTERS, db, request.args["delete_no"])
        return redirect(url_for('add_character'))

    if "update_no" in request.args:
        cid = request.args['update_no']
        query = f"SELECT * FROM {CHARACTERS} WHERE id = {cid}"
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
            form.sixth_field.data = f"{res[6]}"
            header = f"Update {res[1]}"
        # Get species, affiliation, and series links
        query = f"SELECT S.id FROM {SPECIES} S \
                  JOIN {CHAR_SPECIES} CS ON CS.sid=S.id WHERE CS.cid={cid}"
        res = execute_query(db, query).fetchall()
        species_list = []
        for species in res:
            species_list.append(species[0])
        form.seventh_field.data = species_list
        print(f"species list = {species_list}")
        query = f"SELECT A.id FROM {AFFILIATIONS} A \
                  JOIN {CHAR_AFFILS} CA ON CA.aid=A.id WHERE CA.cid={cid}"
        res = execute_query(db, query).fetchall()
        affiliations_list = []
        for affil in res:
            affiliations_list.append(affil[0])
        form.eighth_field.data = affiliations_list
        print(f"affiliations list = {affiliations_list}")
        query = f"SELECT S.id FROM {SERIES} S \
                  JOIN {CHAR_SERIES} CS ON CS.sid=S.id WHERE CS.cid={cid}"
        res = execute_query(db, query).fetchall()
        series_list = []
        for series in res:
            series_list.append(series[0])
        form.ninth_field.data = series_list        

    query_res = select_query(db, BASIC_SELECT_QUERIES[CHARACTERS], CHARACTERS)
    """ for item in query_res:
        # TODO add queries to set these values instead of adding a blank value to the data set
        if display_series:
            item.temp_char_buffer()
        if display_species:
            item.temp_char_buffer() """

    return render_template("add_char_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, display_species=display_species, display_affiliations=display_affiliations,
                           display_series=display_series, target="add-character", allow_update=True)

@app.route("/add-actors", methods=["GET", "POST"])
def add_actor():
    if SUBMIT_TYPE not in session:
        session[SUBMIT_TYPE] = "insert"

    form = AddActorForm()
    form.birthday_field.label.text = "Birthday"
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
        birthday = form.birthday_field.data
        birthday_valid = sanitize_date(birthday)
        birthday = f"{birthday['year']}-{birthday['month']}-{birthday['day']}"
        imdb = str(form.imdb_field.data)
        form.imdb_field.data = ""

        if session[SUBMIT_TYPE] == "insert":
            if birthday_valid:
                query = f"INSERT INTO {ACTORS}(fname, lname, birthday, imdb) VALUES (%s, %s, %s, %s)"
                data = tuple([fname, lname, birthday, imdb])
            else:
                query = f"INSERT INTO {ACTORS}(fname, lname, imdb) VALUES (%s, %s, %s)"
                data = tuple([fname, lname, imdb])
        else:
            if birthday_valid:
                query = f"UPDATE {ACTORS} SET fname = %s, lname = %s, birthday = %s, imdb = %s WHERE id = {session['update_id']}"
                data = tuple([fname, lname, birthday, imdb])
            else:
                query = f"UPDATE {ACTORS} SET fname = %s, lname = %s, birthday = NULL, imdb = %s WHERE id = {session['update_id']}"
                data = tuple([fname, lname, imdb])
            session[SUBMIT_TYPE] = "insert"

        return redirect(url_for('add_actor'))

    if "delete_no" in request.args:
        delete_row(ACTORS, db, request.args["delete_no"])
        return redirect(url_for('add_actor'))

    if "update_no" in request.args:  # TODO
        query = f"SELECT * FROM {ACTORS} WHERE id = {request.args['update_no']}"
        res = execute_query(db, query).fetchone()
        if res is not None:
            session["update_id"] = res[0]
            session[SUBMIT_TYPE] = "update"
            session["update_page"] = ACTORS
            form.fname_field.data = res[1]
            form.lname_field.data = res[2]
           # Dates could be empty
            if res[3]:
                form.birthday_field.form.year.data = res[3].year
                form.birthday_field.form.month.data = res[3].month
                form.birthday_field.form.day.data = res[3].day
            form.imdb_field.data = res[4]
            header = f"Update {res[1]} {res[2]}"

    query_res = select_query(db, BASIC_SELECT_QUERIES[ACTORS], ACTORS)
    for item in query_res:
        if item.table_values[3] is None:
            item.table_values[3] = "#"

    return render_template("add_actor_form.html", form=form, query_res=query_res,
                           column_names=columns, query_has_value=(len(query_res) > 0),
                           header=header, target="add-actors", allow_update=True)

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
        form.second_field.data['year'] = form.second_field.data['month'] = form.second_field.data['day'] = ''
        end = form.third_field.data
        form.third_field.data['year'] = form.third_field.data['month'] = form.third_field.data['day'] = ''
       
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
            data = tuple([name])    
        
        if session[SUBMIT_TYPE] == "insert":
            query = SERIES_INSERT_QUERIES[case]
        else:
            data = data + tuple([session["update_id"]])
            query = SERIES_UPDATE_QUERIES[case]            
            session[SUBMIT_TYPE] = "insert"

        res = execute_query(db, query, data)
        return redirect(url_for("add_series"))

    if "delete_no" in request.args:
        delete_row(SERIES, db, request.args["delete_no"])
        return redirect(url_for('add_series'))

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
                           header=header, target="add-series", allow_update=True)

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
    
        return redirect(url_for('add_species'))
        

    if "delete_no" in request.args:
        delete_row(SPECIES, db, request.args["delete_no"])
        return redirect(url_for('add_species'))

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
                           header=header, target="add-species", allow_update=True)

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
        return redirect(url_for('add_location'))        

    if "delete_no" in request.args:
        delete_row(LOCATIONS, db, request.args["delete_no"])
        return redirect(url_for('add_location'))

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
                           header=header, target="add-location", allow_update=True)

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
            query = f"INSERT INTO {AFFILIATIONS} (name) VALUES (%s)"
        else:
            query = f"UPDATE {AFFILIATIONS} SET name = %s WHERE id = {session['update_id']}"
            session[SUBMIT_TYPE] = "insert"
        data = tuple([name])
        res = execute_query(db, query, data)
        return redirect(url_for('add_affiliation'))

    if "delete_no" in request.args:
        delete_row(AFFILIATIONS, db, request.args["delete_no"])
        return redirect(url_for('add_affiliation'))

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
                           header=header, target="add-affiliations", allow_update=True)

@app.route("/connect-actor-char", methods=["GET", "POST"])
def link_actor_char():
    header = "Select a Character and Actor to Link"
    columns = VIEW_COLUMNS[CHAR_ACTORS]
    db = connect_to_database()
    form = LinkForm()
    form.entity1.label = "Characters"
    form.entity2.label = "Actors"
    form.entity1.choices = get_select_field_items(db, CHARACTERS)
    form.entity2.choices = get_select_field_items(db, ACTORS)

    if form.validate_on_submit():
        query = f"UPDATE {ACTORS} SET cid={form.entity1.data} WHERE id={form.entity2.data}"
        execute_query(db, query)
        return redirect(url_for('link_actor_char'))

    if "delete_no" in request.args:
        query = f"UPDATE {ACTORS} SET cid=NULL WHERE id={request.args['delete_no']}"
        execute_query(db, query)
        return redirect(url_for('link_actor_char'))
    
    query = f"SELECT A.id, CONCAT_WS(' ', C.fname, IFNULL(C.lname,'')), CONCAT_WS(' ', A.fname, IFNULL(A.lname,'')) FROM {CHARACTERS} C \
              JOIN {ACTORS} A ON A.cid=C.id ORDER BY C.fname"
    query_res = select_query(db, query, ACTORS)

    return render_template("dual_field_link_form.html", header=header, form=form,
                            query_res=query_res, column_names=columns, query_has_value=(len(query_res) > 0),
                            target='connect-actor-char', allow_update=False)


@app.route("/connect-char-spec", methods=["GET", "POST"])
def link_char_species():
    header = "Select a Character and Species to Link"
    columns = VIEW_COLUMNS[CHAR_SPECIES]
    db = connect_to_database()
    form = LinkForm()
    form.entity1.label = "Characters"
    form.entity2.label = "Species"
    form.entity1.choices = get_select_field_items(db, CHARACTERS)
    form.entity2.choices = get_select_field_items(db, SPECIES)

    if form.validate_on_submit():
        # Check to see if relationship already exists
        cid = form.entity1.data
        sid = form.entity2.data
        query = f"SELECT * FROM {CHAR_SPECIES} WHERE cid={cid} AND sid={sid}"
        res = execute_query(db, query).fetchone()
        if not res:            
            query = f"INSERT INTO {CHAR_SPECIES} (cid,sid) VALUES ({cid},{sid})"
            execute_query(db, query)
        return redirect(url_for('link_char_species'))

    if "delete_no" in request.args:
        cidsid = request.args['delete_no'].split('-')
        query = f"DELETE FROM {CHAR_SPECIES} WHERE cid={cidsid[0]} AND sid={cidsid[1]}"
        execute_query(db, query)
        return redirect(url_for('link_char_species'))
    
    query = f"SELECT CONCAT_WS('-',CS.cid,CS.sid), CONCAT_WS(' ', C.fname, IFNULL(C.lname,'')), S.name FROM {CHAR_SPECIES} CS \
              JOIN {CHARACTERS} C ON C.id=CS.cid \
              JOIN {SPECIES} S ON S.id=CS.sid ORDER BY C.fname"
    query_res = select_query(db, query, CHAR_SPECIES)

    return render_template("dual_field_link_form.html", header=header, form=form,
                            query_res=query_res, column_names=columns, query_has_value=(len(query_res) > 0),
                            target='connect-char-spec', allow_update=False)


@app.route("/connect-char-aff", methods=["GET", "POST"])
def link_char_aff():
    header = "Select a Character and Affiliation to Link"
    columns = VIEW_COLUMNS[CHAR_AFFILS]
    db = connect_to_database()
    form = LinkForm()
    form.entity1.label = "Characters"
    form.entity2.label = "Affiliations"
    form.entity1.choices = get_select_field_items(db, CHARACTERS)
    form.entity2.choices = get_select_field_items(db, AFFILIATIONS)

    if form.validate_on_submit():
        # Check to see if relationship already exists
        cid = form.entity1.data
        aid = form.entity2.data
        query = f"SELECT * FROM {CHAR_AFFILS} WHERE cid={cid} AND aid={aid}"
        res = execute_query(db, query).fetchone()
        if not res:
            query = f"INSERT INTO {CHAR_AFFILS} (cid,aid) VALUES ({cid},{aid})"
            execute_query(db, query)
        return redirect(url_for('link_char_aff'))

    if "delete_no" in request.args:
        cidaid = request.args['delete_no'].split('-')
        query = f"DELETE FROM {CHAR_AFFILS} WHERE cid={cidaid[0]} AND aid={cidaid[1]}"
        execute_query(db, query)
        return redirect(url_for('link_char_aff'))
    
    query = f"SELECT CONCAT_WS('-',CA.cid,CA.aid), CONCAT_WS(' ', C.fname, IFNULL(C.lname,'')), A.name FROM {CHAR_AFFILS} CA \
              JOIN {CHARACTERS} C ON C.id=CA.cid \
              JOIN {AFFILIATIONS} A ON A.id=CA.aid ORDER BY C.fname"
    query_res = select_query(db, query, CHAR_AFFILS)

    return render_template("dual_field_link_form.html", header=header, form=form,
                            query_res=query_res, column_names=columns, query_has_value=(len(query_res) > 0),
                            target='connect-char-aff', allow_update=False)


@app.route("/connect-char-series", methods=["GET", "POST"])
def link_char_series():
    header = "Select a Character and Series to Link"
    columns = VIEW_COLUMNS[CHAR_SERIES]
    db = connect_to_database()
    form = LinkForm()
    form.entity1.label = "Characters"
    form.entity2.label = "Series"
    form.entity1.choices = get_select_field_items(db, CHARACTERS)
    form.entity2.choices = get_select_field_items(db, SERIES)

    if form.validate_on_submit():
        # Check to see if relationship already exists
        cid = form.entity1.data
        sid = form.entity2.data
        query = f"SELECT * FROM {CHAR_SERIES} WHERE cid={cid} AND sid={sid}"
        res = execute_query(db, query).fetchone()
        if not res:            
            query = f"INSERT INTO {CHAR_SERIES} (cid,sid) VALUES ({cid},{sid})"
            execute_query(db, query)
        return redirect(url_for('link_char_series'))

    if "delete_no" in request.args:
        query = f"DELETE FROM {CHAR_SERIES} WHERE id={request.args['delete_no']}"
        execute_query(db, query)
        return redirect(url_for('link_char_series'))
    
    query = f"SELECT CS.id, CONCAT_WS(' ', C.fname, IFNULL(C.lname,'')), S.name FROM {CHAR_SERIES} CS " \
            f"JOIN {CHARACTERS} C ON C.id=CS.cid "\
            f"JOIN {SERIES} S ON S.id=CS.sid ORDER BY C.fname"
    query_res = select_query(db, query, CHAR_SPECIES)

    return render_template("dual_field_link_form.html", header=header, form=form,
                            query_res=query_res, column_names=columns, query_has_value=(len(query_res) > 0),
                            target='connect-char-series', allow_update=False)

@app.route("/connect-csl", methods=["GET", "POST"])
def link_char_series_loc():
    header = "Select a relationship between character, series and location"
    columns = VIEW_COLUMNS[CHAR_SERIES_LOCS]
    db = connect_to_database()

    form = CSLLinkForm()
    form.entity1.choices = get_select_field_items(db, CHARACTERS)
    form.entity2.choices = get_select_field_items(db, SERIES)
    form.entity3.choices = [[-1, "None"]] + get_select_field_items(db, LOCATIONS)

    query_res = []
    query = "SELECT CS.id, L.id, C.fname, C.alias, C.lname, S.name, L.name FROM characters C INNER JOIN characters_series CS ON C.id = CS.cid INNER JOIN series S ON S.id = CS.sid LEFT JOIN characters_series_locations CSL ON CSL.csid = CS.id LEFT JOIN locations L ON L.id = CSL.lid;"
    query_res = select_query(db, query, "CSL")

    return render_template("link_csl.html", header=header, form=form, colum_names=columns,
                           query_has_value=(len(query_res) > 0), target='connect-csl', allow_update=False)

@app.route("/connect-location", methods=["GET", "POST"])
def link_to_location():
    header = "Select a Character-Series and Location to Link"
    columns = VIEW_COLUMNS[CHARSERIES_LOCS]
    db = connect_to_database()
    form = LinkForm()
    form.entity1.label = "Characters/Series"
    form.entity2.label = "Locations"
    form.entity1.choices = get_select_field_items(db, CHAR_SERIES)
    form.entity2.choices = get_select_field_items(db, LOCATIONS)

    if form.validate_on_submit():
        # Check to see if relationship already exists
        csid = form.entity1.data
        lid = form.entity2.data
        query = f"SELECT * FROM {CHAR_SERIES_LOCS} WHERE csid={csid} AND lid={lid}"
        res = execute_query(db, query).fetchone()
        if not res:            
            query = f"INSERT INTO {CHAR_SERIES_LOCS} (csid,lid) VALUES ({csid},{lid})"
            execute_query(db, query)
        return redirect(url_for('link_to_location'))

    if "delete_no" in request.args:
        csidlid = request.args['delete_no'].split('-')
        query = f"DELETE FROM {CHAR_SERIES_LOCS} WHERE csid={csidlid[0]} AND lid={csidlid[1]}"
        execute_query(db, query)
        return redirect(url_for('link_to_location'))
    
    query = f"SELECT CONCAT_WS('-',CSL.csid,CSL.lid), CONCAT_WS(' / ', CONCAT_WS(' ', C.fname, IFNULL(C.lname,'')), S.name), L.name FROM {CHAR_SERIES_LOCS} CSL \
              JOIN {LOCATIONS} L ON L.id=CSL.lid \
              JOIN {CHAR_SERIES} CS ON CS.id=CSL.csid \
              JOIN {CHARACTERS} C ON C.id=CS.cid \
              JOIN {SERIES} S ON S.id=CS.sid ORDER BY C.fname"
    query_res = select_query(db, query, CHAR_SPECIES)

    return render_template("dual_field_link_form.html", header=header, form=form,
                            query_res=query_res, column_names=columns, query_has_value=(len(query_res) > 0),
                            target='connect-location', allow_update=False)


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
        if data_type != "CSL":
            query_res.append(Row(item[0], list(item[1:]), data_type))
        else:
            query_res.append(Row(f"{item[0]} {item[1]}", list(item[2:]), data_type))
            print(f"{item[0]} {item[1]}")

    return query_res

def get_select_field_items(db, table, attributes = None):
    query = ""

    if attributes is None:
        if table == CHARACTERS:
            attributes = ["id", "fname", "alias", "lname"]
        elif table == ACTORS:
            attributes = ["id", "fname", "lname"]
        elif table == CHAR_SERIES:
            query = f"SELECT CS.id, CONCAT_WS(' / ', CONCAT_WS(' ', C.fname, IFNULL(C.lname,'')), S.name) " \
                    f"FROM {table} CS JOIN {CHARACTERS} C ON C.id=CS.cid " \
                    f"JOIN {SERIES} S ON S.id=CS.sid ORDER BY C.fname"
        else:
            attributes = ["id", "name"]
    elif attributes[0] != "id":
        attributes = ["id"] + attributes


    if len(query) == 0:
        order_by = attributes[1]
        attributes = (", ").join(attributes)
        query = f"SELECT {attributes} FROM {table} ORDER BY {order_by}"
    res = execute_query(db, query)

    result_list = []
    for item in res:
        id = item[0]
        item_data = item[1:]
        data_str = ""
        for val in item_data:
            if len(val) > 0 and val not in data_str:
                data_str += " " + val
        result_list.append((id, data_str))
    return result_list


def get_character_search_query(form):
    # form assumes fields fname, lname, actors, species, affiliations, and series
    whereString = ''
    query = f"SELECT DISTINCT C.id, C.fname, C.lname, C.alias, C.title FROM {CHARACTERS} C"

    fname = str(form.fname.data)
    if fname:
        if whereString:
            whereString += f" AND C.fname='{fname}'"
        else:
            whereString += f" WHERE C.fname='{fname}'"

    lname = str(form.lname.data)
    if lname:
        if whereString:
            whereString += f" AND C.lname='{lname}'"
        else:
            whereString += f" WHERE C.lname='{lname}'"

    actorList = ''
    for e in form.actors.data:
        actorList += str(e)
    if actorList:
        query += f" JOIN {ACTORS} A ON A.cid=C.id"
        if whereString:
            whereString += f" AND A.id in ({','.join(actorList)})"
        else:
            whereString += f" WHERE A.id in ({','.join(actorList)})"

    speciesList = ''
    for e in form.species.data:
        speciesList += str(e)
    if speciesList:
        query += f" JOIN {CHAR_SPECIES} CS ON CS.cid=C.id JOIN {SPECIES} S ON S.id=CS.sid"
        if whereString:
            whereString += f" AND S.id in ({','.join(speciesList)})"
        else:
            whereString += f" WHERE S.id in ({','.join(speciesList)})"

    affiliationsList = ''
    for e in form.affiliations.data:
        affiliationsList += str(e)
    if affiliationsList:
        query += f" JOIN {CHAR_AFFILS} CA ON CA.cid=C.id JOIN {AFFILIATIONS} AFF ON AFF.id=CA.aid"
        if whereString:
            whereString += f" AND AFF.id in ({','.join(affiliationsList)})"
        else:
            whereString += f" WHERE AFF.id in ({','.join(affiliationsList)})"

    seriesList = ''
    for e in form.series.data:
        seriesList += str(e)
    if seriesList:
        query += f" JOIN {CHAR_SERIES} CSR ON CSR.cid=C.id JOIN {SERIES} SR ON SR.id=CSR.sid"
        if whereString:
            whereString += f" AND SR.id in ({','.join(seriesList)})"
        else:
            whereString += f" WHERE SR.id in ({','.join(seriesList)})"   

    query += f"{whereString} ORDER BY fname"

    return query
    
# TODO implement
def load_data_page(row_item):
    print(row_item, row_item.id)


if __name__=="__main__":
    app.run(debug=True)
