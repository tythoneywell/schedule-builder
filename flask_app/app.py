from flask import Flask, render_template, request
from flask_app.backend.schedule import MySchedule
from flask_app.backend.courses import CourseList, APIGet
from flask_app.forms import SearchForm, ClearAllCoursesForm, AddRemoveForm, NextPageOnAllCoursesPageForm, \
    PreviousPageOnAllCoursesPageForm, SearchForCourseSectionsForm, AddClassForm, SerializeScheduleForm

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "super secret key"

course_list = CourseList()
schedule = MySchedule()
color_index = 0
colors = ["red", "blue", "green", "purple", "orange", "magenta"]


class GetApp:
    """"
    Returns instance of the flask app
    Mainly used so that other files (i.e. tests) can access the Flask object
    """

    @staticmethod
    def get_app():
        global app
        return app


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
    search_for_sections_of_course_form = SearchForCourseSectionsForm()
    add_class_form = AddClassForm()
    serialize_schedule_form = SerializeScheduleForm()

    if search_for_sections_of_course_form.search_for_course.data and \
            search_for_sections_of_course_form.validate_on_submit():
        courses_to_display = []
        partial_course_code = search_for_sections_of_course_form.search_query.data.upper()

        try:
            courses_to_display = [CourseList.get_course_using_course_code(course_head.course_code) for course_head in
                                  APIGet.get_course_heads_by_query(partial_course_code)]

        except Exception as e:
            add_remove_notification_text = str(e)

        finally:
            return render_template('index.html',
                                   courses_to_display=courses_to_display,
                                   schedule=schedule,
                                   search_form=search_form,
                                   add_remove_form=add_remove_form,
                                   add_remove_notification_text=add_remove_notification_text,
                                   clear_all_courses_form=clear_all_courses_form,
                                   search_for_sections_of_course_form=search_for_sections_of_course_form,
                                   add_class_form=add_class_form,
                                   serialize_schedule_form=serialize_schedule_form)

    if (add_remove_form.add.data or add_remove_form.remove.data) and add_remove_form.validate_on_submit():
        course_code = add_remove_form.course_query.data.upper()
        section_number = add_remove_form.section_query.data
        add_remove_notification_text = ""

        try:
            course_list_to_add = CourseList.get_course_using_course_code(course_code)
            if course_list_to_add.sections == {}:
                raise Exception("This course has no sections, please "
                                "contact department for information to register for this course.")
            course_to_add = course_list_to_add.sections[section_number]
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
                                   clear_all_courses_form=clear_all_courses_form,
                                   search_for_sections_of_course_form=search_for_sections_of_course_form,
                                   add_class_form=add_class_form,
                                   serialize_schedule_form=serialize_schedule_form)

    if clear_all_courses_form.clear_all.data and clear_all_courses_form.validate_on_submit():
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
                               clear_all_courses_form=clear_all_courses_form,
                               search_for_sections_of_course_form=search_for_sections_of_course_form,
                               add_class_form=add_class_form,
                               serialize_schedule_form=serialize_schedule_form)
    if serialize_schedule_form.serialize_schedule.data and serialize_schedule_form.validate_on_submit():
        serialized_schedule = schedule.get_serialized_schedule()
        return render_template('index.html',
                               schedule=schedule,
                               search_form=search_form,
                               add_remove_form=add_remove_form,
                               add_remove_notification_text=add_remove_notification_text,
                               clear_all_courses_form=clear_all_courses_form,
                               search_for_sections_of_course_form=search_for_sections_of_course_form,
                               add_class_form=add_class_form,
                               serialize_schedule_form=serialize_schedule_form,
                               serialized_schedule=serialized_schedule)

    if serialize_schedule_form.load_schedule.data and serialize_schedule_form.validate_on_submit():
        schedule.load_serialized_schedule(serialize_schedule_form.display_serialized_schedule.data)
        return render_template('index.html',
                               schedule=schedule,
                               search_form=search_form,
                               add_remove_form=add_remove_form,
                               add_remove_notification_text=add_remove_notification_text,
                               clear_all_courses_form=clear_all_courses_form,
                               search_for_sections_of_course_form=search_for_sections_of_course_form,
                               add_class_form=add_class_form,
                               serialize_schedule_form=serialize_schedule_form)

    # KEEP THIS IF STATEMENT LAST PLEASE!!!!
    if add_class_form.validate_on_submit():
        try:
            button_response = request.form['course'].split(" ")[1].split("-")
            course = button_response[0]
            section = button_response[1]
            course_to_add = CourseList.get_course_using_course_code(course).sections[section]
            course_to_add.set_color(colors[color_index])

            schedule.add_class(course_to_add)
            color_index += 1
            if color_index >= len(colors):
                color_index = 0

        except Exception as e:
            add_remove_notification_text = str(e)

        finally:
            return render_template('index.html',
                                   schedule=schedule,
                                   search_form=search_form,
                                   add_remove_form=add_remove_form,
                                   add_remove_notification_text=add_remove_notification_text,
                                   clear_all_courses_form=clear_all_courses_form,
                                   search_for_sections_of_course_form=search_for_sections_of_course_form,
                                   add_class_form=add_class_form,
                                   serialize_schedule_form=serialize_schedule_form)

    return render_template('index.html',
                           schedule=schedule,
                           search_form=search_form,
                           add_remove_form=add_remove_form,
                           add_remove_notification_text=add_remove_notification_text,
                           clear_all_courses_form=clear_all_courses_form,
                           search_for_sections_of_course_form=search_for_sections_of_course_form,
                           add_class_form=add_class_form,
                           serialize_schedule_form=serialize_schedule_form)


@app.route('/all_courses/<page_num>', methods=['GET', 'POST'])
def all_courses(page_num: int):
    """"
    Display a list of all courses that the student could try to sign up for
    The user can navigate to the next and previous pages to see more courses
    Args:
            page_num: int
                The page number of all courses to load
    """

    courses = CourseList.get_courses_using_page_number(page_num)

    prev_page_num = None if page_num == 1 else int(page_num) - 1
    next_page_num = int(page_num) + 1

    return render_template('all_courses.html',
                           courses=courses,
                           page_num=page_num,
                           prev_page_num=prev_page_num,
                           next_page_num=next_page_num)


@app.route('/all_professors/<page_num>', methods=['GET', 'POST'])
def all_professors(page_num: int):
    """"
    Display a list of all professors that the student could try to take
    Each professor is a hyerlink to their specific page 
    Args:
        page_num: int
            The page number of all courses to load
    """

    professor_names, professor_slugs, professor_ratings = Professor.get_all_professors(page_num)

    prev_page_num = None if page_num == 1 else int(page_num) - 1
    next_page_num = int(page_num) + 1

    return render_template('all_professors.html',
                           professor_names_slugs=zip(professor_names, professor_slugs, professor_ratings),
                           page_num=page_num,
                           prev_page_num=prev_page_num,
                           next_page_num=next_page_num)


@app.route('/professor/<name>/<slug>', methods=['GET', 'POST'])
def professor_detail(name: str, slug):
    """"
    Display a page for a specific professor using their slug
    Args:
        name: string
            Professor name to get professor with
        slug: string
            Professor slug to create a unique link to their page 
    """

    professor = APIGet.get_professor_by_name(name)
    plantterp_link = "https://planetterp.com/professor/" + slug
    return render_template("professor_detail.html",
                           professor=professor,
                           plantterp_link=plantterp_link)
