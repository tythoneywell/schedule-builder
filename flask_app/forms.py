from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    """
    Form to search for a course and then be able to add course
    """
    search_query = StringField('Query', validators=[InputRequired()])
    submit = SubmitField('Submit')


class AddClassForm(FlaskForm):
    """
    Form to add class from the search results
    """
    submit = SubmitField('Submit')


class AddSectionForm(FlaskForm):
    """
    Form to add class from the search results
    """
    submit = SubmitField('Submit')


class ViewSectionsForm(FlaskForm):
    """
    Form to view sections from the list of added or searched courses
    """
    submit = SubmitField('Submit')


class AddRemoveForm(FlaskForm):
    """
    Form to add or remove a class from the schedule
    """
    course_query = StringField('Course Code', validators=[InputRequired()])
    section_query = StringField('Section Number', validators=[InputRequired()])
    add = SubmitField('Add')
    remove = SubmitField('Remove')


class ClearAllCoursesForm(FlaskForm):
    """
    Form to clear all courses from the schedule
    """
    clear_all = SubmitField('Clear Schedule')


class SearchForCourseForm(FlaskForm):
    """
    Form to search for course and display sections
    """
    search_query = StringField('Course To Search', validators=[InputRequired()])
    search_for_course = SubmitField('Search')


class NextPageOnAllCoursesPageForm(FlaskForm):
    """
    Form to select next page on route for all pages
    """
    next_page = SubmitField('Next Page')


class PreviousPageOnAllCoursesPageForm(FlaskForm):
    """
    Form to select previous page on route for all pages
    """
    previous_page = SubmitField('Previous Page')


class SerializeScheduleForm(FlaskForm):
    """
    Form to serialize the current schedule for the user to copy, to be loaded later.
    Form also loads serialized data that was previously copied
    """
    serialize_schedule = SubmitField('Get Schedule Data')
    display_serialized_schedule = StringField('Schedule Data')
    load_schedule = SubmitField("Load Schedule Data")


