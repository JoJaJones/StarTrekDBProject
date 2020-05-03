from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class AddForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fields = []
        self.init_fields(field_dict)

    def init_fields(self, field_dict):
        for field in field_dict:
            if field_dict[field] == "string":
                self._fields.append(StringField(field))


class SelectSingleForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SelectMultipleForm(FlaskForm):
    pass

def create_form(field_dict):
    form = FlaskForm()
    form["name"] = StringField("Name: ")
