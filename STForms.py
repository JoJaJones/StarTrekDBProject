from flask import Flask, render_template
from flask_wtf import FlaskForm
from constants import CHARACTERS, SPECIES, SERIES, LOCATIONS, AFFILIATIONS, ACTORS
from wtforms import (widgets, validators, StringField, SubmitField, RadioField, SelectMultipleField, FormField,
                     IntegerField, SelectField, DateField, TextAreaField, Form)

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"


class DateSubForm(Form):
    month = IntegerField("MM", validators=[validators.Optional(), validators.NumberRange(1, 12)])
    day = IntegerField("DD", validators=[validators.Optional(), validators.number_range(1, 31)])
    year = IntegerField("YYYY", validators=[validators.Optional(),
                                              validators.number_range(1966,
                                                                      message="Year must be 1966 or later")])

    def clear(self):
        self.month.data = None
        self.day.data = None
        self.year.data = None


class Display:
    pass


class SingleFieldForm(FlaskForm):
    first_field = StringField("", validators=[validators.DataRequired()])
    submit = SubmitField("Submit")


class Row:
    def __init__(self, id, values, data_type):
        self.id = id
        self.data_type = data_type
        self.table_values = values
        self.name = None
        self.set_name()

    def set_name(self):
        if self.data_type == CHARACTERS and self.table_values[1] and len(self.table_values[1]) > 0:
            self.name = self.table_values[1]
        else:
            self.name = self.table_values[0]

    def reformat_date(self, idx: int):
        temp_date = str(self.table_values[idx]).split("-")
        temp_date = temp_date[1:] + [temp_date[0]]
        self.table_values[idx] = "-".join(temp_date)

    def temp_char_buffer(self):
        self.table_values += [""]


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")


class TestForm(FlaskForm):
    select_field = SelectField("", coerce=int)


class LocationForm(FlaskForm):
    first_field = StringField("")
    second_field = SelectField("", choices=[("station", "Space Station"),
                                            ("planet", "Planet"),
                                            ("ship", "Space Ship")])
    submit = SubmitField("Submit")


class SeriesForm(FlaskForm):
    first_field = StringField("Series Name", validators=[validators.DataRequired()])
    second_field = FormField(DateSubForm)
    third_field = FormField(DateSubForm)
    submit = SubmitField("Submit")


class CharacterForm(FlaskForm):
    first_field = StringField("First Name")
    second_field = StringField("Last Name", validators=[validators.Optional()])
    third_field = StringField("Title", validators=[validators.Optional()])
    fourth_field = TextAreaField("Description", validators=[validators.Optional()])
    fifth_field = TextAreaField("Biography", validators=[validators.Optional()])
    sixth_field = SelectMultipleField("Species", coerce=int, validators=[validators.Optional()])
    seventh_field = SelectMultipleField("Series", coerce=int, validators=[validators.Optional()])
    # add_location = SubmitField("Add Location to Character")
    submit = SubmitField("Submit")


class AddLocationToCharacter(FlaskForm):
    first_field = SelectField(coerce=int)
    second_field = SelectField(coerce=int)
    submit = SubmitField("Submit")


class AddActorForm(FlaskForm):
    fname_field    = StringField("First name", validators=[validators.Required()])
    lname_field    = StringField("Last name", validators=[validators.Optional()])
    birthday_field = StringField(label="Birthday", id='datepick', validators=[validators.Optional()])
    imdb_field     = StringField("IMDB link", validators=[validators.Optional()])
    submit         = SubmitField("Submit")

class SearchByFnameForm(FlaskForm):
    fname_field    = StringField("First name", validators=[validators.Required()])
    submit         = SubmitField("Search")

class SearchByLnameForm(FlaskForm):
    lname_field    = StringField("Last name", validators=[validators.Required()])
    submit         = SubmitField("Search")

class FilterBySpecies(FlaskForm):
    species_field = SelectMultipleField("Species", coerce=int, validators=[validators.Optional()])
    submit        = SubmitField("Search")

class FilterBySeries(FlaskForm):
    series_field = SelectMultipleField("Species", coerce=int, validators=[validators.Optional()])
    submit       = SubmitField("Search")


