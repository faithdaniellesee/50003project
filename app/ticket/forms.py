from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class TicketForm(FlaskForm):
    ticketOptions = [(None, ''), ("Query", "Query"), ("Feedback", "Feedback"),
                     ("Suggestion", "Suggestion"), ("Others", "Others")]
    options = SelectField(u'Ticket Options', choices=ticketOptions, validators=[DataRequired()])
    title = StringField(u'Full Name', validators=[DataRequired(), Length(max=100)])
    details = TextAreaField('Details', validators=[DataRequired(), Length(min=1)])
    file = FileField('File', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Submit')

