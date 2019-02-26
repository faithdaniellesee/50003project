from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField


class LanguageForm(Form):

    text = TextAreaField("Text")
    language = SelectField('Languages', choices=[('en', 'English'),
                                                 ('fr', 'French'),
                                                 ('de', 'German')])
    submit = SubmitField("Send")
