from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, FormField

app = Flask(__name__)

app.config["SECRET_KEY"] = "tempsecret"

class SingleFieldForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_name = list(field_dict.keys())[0]
        field_type = field_dict[field_name]
        self.field = get_field(field_name, field_type)
        self.submit = SubmitField("Submit")

class AddForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = []
        self.init_fields(field_dict)
        self.fields.append(SubmitField("Submit"))

    def init_fields(self, field_dict):
        for field in field_dict:
            if field_dict[field] == "string":
                self.fields.append(StringField(field))


class SelectSingleForm(FlaskForm):
    def __init__(self, field_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SelectMultipleForm(FlaskForm):
    pass

def get_field(field_name, field_type):
    if field_type == "string":
        return StringField(field_name)

def create_form(field_dict):
    form = FlaskForm()
    form["name"] = StringField("Name: ")
