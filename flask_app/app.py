from flask import Flask, render_template, redirect, url_for
from flask_app.backend.schedule import MySchedule
from flask_app.backend.courses import CourseList
from flask_app.forms import SearchForm, ClearAllCoursesForm, AddRemoveForm, NextPageOnAllCoursesPageForm, \
    PreviousPageOnAllCoursesPageForm

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
            course_to_add = CourseList.get_courses_using_course_code(course_code).sections[section_number]
            # course_list.courses[course_code].sections[section_number]
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

        except Exception as e:
            add_remove_notification_text = str(e)

        finally:
            return render_template('index.html',
                                   schedule=schedule,
                                   search_form=search_form,
                                   add_remove_form=add_remove_form,
                                   add_remove_notification_text=add_remove_notification_text,
                                   clear_all_courses_form=clear_all_courses_form)

    if clear_all_courses_form.validate_on_submit():
        if schedule.total_credits == 0:
            clear_all_courses_form.clear_all.errors = ["Schedule is already empty"]
            
        schedule.remove_all_classes()
        add_remove_form.course_query.errors = []
        add_remove_form.section_query.errors = []

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


@app.route('/all_courses/<page_num>', methods=['GET', 'POST'])
def all_courses(page_num):
    """"
    Display a list of all courses that the student could try to sign up for
    The user can navigate to the next and previous pages to see more courses
    """

    if int(page_num) > 1:
        previous_page_form = PreviousPageOnAllCoursesPageForm()
    else:
        previous_page_form = None
    next_page_form = NextPageOnAllCoursesPageForm()

    # Need some way to prevent going to negative pages or too many pages

    if previous_page_form is not None and \
            previous_page_form.previous_page.data and previous_page_form.validate_on_submit():
        page_num = int(page_num) - 1
        return redirect(url_for("all_courses", page_num=page_num))

    if next_page_form.next_page.data and next_page_form.validate_on_submit():
        page_num = int(page_num) + 1
        return redirect(url_for("all_courses", page_num=page_num))

    courses = CourseList.get_courses_using_page_number(page_num)

    return render_template('all_courses.html',
                           courses=courses,
                           page_num=page_num,
                           previous_page_form=previous_page_form,
                           next_page_form=next_page_form)
