from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class SingleFieldForm(FlaskForm):
    field = StringField("")
    submit = SubmitField("Submit")


class Row:
    def __init__(self, id, values):
        self.id = id
        self.table_values = values
        self.form = DeleteForm()

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")




class DoubleFieldForm(FlaskForm):
    pass