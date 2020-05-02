from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class AddForm(FlaskForm):
    def __init__(self, field_names, field_types):
        self._field_names = field_names
        self._field_types = field_types