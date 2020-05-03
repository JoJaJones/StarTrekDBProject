from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class SingleFieldForm(FlaskForm):
    field = StringField("")
    submit = SubmitField("Submit")

class DeleteForm(FlaskForm):

    submit = SubmitField("Delete")

    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.data = []



class DoubleFieldForm(FlaskForm):
    pass