from flask import Flask, render_template, redirect, url_for
from flask_app.model import MySchedule, CourseList
from flask_app.forms import SearchForm, ClearAllCoursesForm, AddRemoveForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key"
course_list = CourseList()  # populate the course list from the big json file

schedule = MySchedule()
color_index = 0
colors = ["red", "blue", "green", "yellow", "orange", "pink"]


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page for the flask app that will allow users to see/make their schedule
    Also contains link to see all courses
    """

    global schedule
    global color_index
    global colors

    search_form = SearchForm()
    add_remove_form = AddRemoveForm()
    add_remove_notification_text = ""
    clear_all_courses_form = ClearAllCoursesForm()

    if add_remove_form.validate_on_submit():
        course_code = add_remove_form.course_query.data.upper()
        section_number = add_remove_form.section_query.data
        add_remove_notification_text = ""

        try:
            course_to_add = course_list.courses[course_code].sections[section_number]
            course_to_add.set_color(colors[color_index])

            if add_remove_form.add.data:
                add_remove_notification_text = schedule.add_class(course_to_add)
                color_index += 1
                if color_index >= len(colors):
                    color_index = 0

            if add_remove_form.remove.data:
                add_remove_notification_text = schedule.remove_class(course_to_add)
                color_index -= 1
                if color_index < 0:
                    color_index = len(colors) - 1

        except KeyError:
            add_remove_notification_text = "No section named " + \
                                           course_code + "-" + section_number + " found."

        finally:
            return render_template('index.html',
                                   schedule=schedule,
                                   search_form=search_form,
                                   add_remove_form=add_remove_form,
                                   add_remove_notification_text=add_remove_notification_text,
                                   clear_all_courses_form=clear_all_courses_form)

    if clear_all_courses_form.validate_on_submit():
        schedule.remove_all_classes()

        return render_template('index.html',
                               schedule=schedule,
                               search_form=search_form,
                               add_remove_form=add_remove_form,
                               add_remove_notification_text=add_remove_notification_text,
                               clear_all_courses_form=clear_all_courses_form)

    return render_template('index.html',
                           schedule=schedule,
                           search_form=search_form,
                           add_remove_form=add_remove_form,
                           add_remove_notification_text=add_remove_notification_text,
                           clear_all_courses_form=clear_all_courses_form)


@app.route('/all_courses')
def all_courses():
    """"
    Display a list of all courses that the student could try to sign up for
    """
    return render_template('all_courses.html',
                           courses=course_list.courses)
