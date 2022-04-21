from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired()])
    submit = SubmitField('Submit')


class AddClassForm(FlaskForm):
    submit2 = SubmitField('Submit')


class AddRemoveForm(FlaskForm):
    course_query = StringField('Course Code', validators=[InputRequired()])
    section_query = StringField('Section Number', validators=[InputRequired()])
    add = SubmitField('Add')
    remove = SubmitField('Remove')


class ClearAllCoursesForm(FlaskForm):
    clear_all = SubmitField('Clear Schedule')


class SearchForCourseSectionsForm(FlaskForm):
    search_query = StringField('Course To Search', validators=[InputRequired()])
    search_for_course = SubmitField('Search')


class NextPageOnAllCoursesPageForm(FlaskForm):
    next_page = SubmitField('Next Page')


class PreviousPageOnAllCoursesPageForm(FlaskForm):
    previous_page = SubmitField('Previous Page')
