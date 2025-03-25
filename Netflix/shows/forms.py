from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

from flask_login import current_user
from Netflix.models import Users

class AddShow(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    release_date = StringField('Release Date', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    submit = SubmitField('Add')

class DeleteShow(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Delete')

class SearchShows(FlaskForm):
    title = StringField('Title')
    genre = StringField('Genre')
    submit = SubmitField('Search')