from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User
from wtforms_test import FormTestCase


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Regexp('^\w+$'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Regexp('^\w+$'), DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LanguageForm(FlaskForm):

    text = TextAreaField("Text")
    language = SelectField('Languages', choices=[('en', 'English'),
                                                 ('fr', 'French'),
                                                 ('de', 'German')])
    submit = SubmitField("Submit")


class GetLanguage(FlaskForm):

    text2 = TextAreaField("Text")
    submit2 = SubmitField("Submit")


class TestLoginForm(FormTestCase):
    form_class = LoginForm

    def test_age_is_required(self):
        res = client.get(url_for('auth.register'))
        assert res.status_code == 200
        res = client.post(url_for('auth.register'),
                          data={'fname': 'test', 'lname': 'user', 'email': 'test@user.org', 'password': '12'})
