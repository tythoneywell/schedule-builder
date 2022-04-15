from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired()])
    submit = SubmitField('Submit')


class AddClassForm(FlaskForm):
    course_code = StringField('Course Code', validators=[InputRequired()])
    section_num = StringField('Section Number', validators=[InputRequired()])
    add_course = SubmitField('Submit')


class AddRemoveForm(FlaskForm):
    course_query = StringField('Course Code', validators=[InputRequired()])
    section_query = StringField('Section Number', validators=[InputRequired()])
    add = SubmitField('Add')
    remove = SubmitField('Remove')


class ClearAllCoursesForm(FlaskForm):
    clear_all = SubmitField('Clear Schedule')

class NextPageOnAllCoursesPageForm(FlaskForm):
    next_page = SubmitField('Next Page')

class PreviousPageOnAllCoursesPageForm(FlaskForm):
    previous_page = SubmitField('Previous Page')
