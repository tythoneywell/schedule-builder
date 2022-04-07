from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired()])
    submit = SubmitField('Submit')
