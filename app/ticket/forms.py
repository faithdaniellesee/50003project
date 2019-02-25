from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class TicketForm(FlaskForm):
    content = TextAreaField('Enter your request here.', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')
