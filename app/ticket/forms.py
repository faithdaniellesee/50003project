from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired


def validate_select(form, field):
    if field.data == "":
        raise ValidationError("Please select a field")

class TicketForm(FlaskForm):
    ticketOptions = [("", ' '), ("Query", "Query"), ("Feedback", "Feedback"),
                     ("Suggestion", "Suggestion"), ("Others", "Others")]
    options = SelectField(u'Ticket Options', choices=ticketOptions, validators=[validate_select, DataRequired()])
    title = StringField(u'Full Name', validators=[DataRequired(), Length(max=100)])
    details = TextAreaField('Details', validators=[DataRequired(), Length(min=1)])
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ViewForm(FlaskForm):
    replytext = TextAreaField('Reply', validators=[DataRequired(), Length(min=1)])
    reply = SubmitField('Reply')

class ResolveForm(FlaskForm):
    resolve = SubmitField('Resolve')
    send = SubmitField('Send')
    msgContent = TextAreaField('msgContent')

class BackForm(FlaskForm):
    back = SubmitField('Back')

