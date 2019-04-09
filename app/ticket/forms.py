from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class TicketForm(FlaskForm):
    ticketOptions = [(None, ''), ("Query", "Query"), ("Feedback", "Feedback"),
                     ("Suggestion", "Suggestion"), ("Others", "Others")]
    category = [(None, ''), ("Layout", "Layout"), ("Function", "Function"),
                ("Account", "Account"), ("Options", "Options")]
    options = SelectField(u'Ticket Options', choices=ticketOptions, validators=[DataRequired()])
    category = SelectField(u'Category', choices=category, validators=[DataRequired()])
    details = TextAreaField('Details', validators=[DataRequired(), Length(min=1)])
    file = FileField('File', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Submit')
