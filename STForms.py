from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class SingleFieldForm(FlaskForm):
    field = StringField("")
    submit = SubmitField("Submit")

class DoubleFieldForm(FlaskForm):
    pass