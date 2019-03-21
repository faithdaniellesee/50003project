import os
import tempfile

import pytest
from flask import Flask, request
from app import forms


def test_sample_form_validate():
    app = Flask(__name__)
    form = forms.LoginForm()
    with app.test_request_context('/'):
        request.form = ImmutableMultiDict([('btn', 'Save')])
        form.validate()  # Prints 'Saving...'
        request.form = ImmutableMultiDict([('btn', 'Update')])
        form.validate()  # Prints 'Updating!'

        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember_me = BooleanField('Remember Me')
        submit = SubmitField('Sign In')