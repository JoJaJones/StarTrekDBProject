from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField,
                     IntegerField, SelectField, DateField, TextAreaField)

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"


class DateSubForm(FlaskForm):
    month = IntegerField("Month")
    day = IntegerField("Day")
    year = IntegerField("Year")

    def clear(self):
        self.month.data = ""
        self.day.data = ""
        self.year.data = ""


class SingleFieldForm(FlaskForm):
    first_field = StringField("")
    submit = SubmitField("Submit")


class Row:
    def __init__(self, id, values):
        self.id = id
        self.table_values = values
        # self.form = DeleteForm()


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")


class LocationForm(FlaskForm):
    first_field = StringField("")
    second_field = SelectField("", choices=[("station", "Space Station"),
                                            ("planet", "Planet"),
                                            ("ship", "Space Ship")])
    submit = SubmitField("Submit")


class SeriesForm(FlaskForm):
    first_field = StringField()
    second_field = FormField(DateSubForm)
    third_field = FormField(DateSubForm)
    submit = SubmitField("Submit")


class CharacterForm(FlaskForm):
    first_field = StringField()
    second_field = StringField()
    third_field = StringField()
    fourth_field = TextAreaField()
    fifth_field = TextAreaField()
    sixth_field = SelectMultipleField(choices=1)
    seventh_field = SelectMultipleField(choices=1)
    add_location = SubmitField("Add Location to Character")
    submit = SubmitField("Submit")


class AddLocationToCharacter(FlaskForm):
    first_field = SelectField(choices=1)
    second_field = SelectField(choices=1)
    submit = SubmitField("Submit")
