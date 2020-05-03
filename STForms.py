from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class AddForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SelectSingleForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)