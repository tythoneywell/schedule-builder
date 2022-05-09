from flask import Flask, render_template, request
from flask_app.backend.schedule import MySchedule
from flask_app.backend.courses import CourseList, APIGet, Professor
from flask_app.forms import SearchForm, ClearAllCoursesForm, AddRemoveForm, SearchForCourseForm, AddClassForm, \
    ViewSectionsForm, SerializeScheduleForm, GenEdSearchForm

course_list = CourseList()
schedule = MySchedule()
courses_to_display = []
expanded_course_to_display = None


def create_app():
    """
    Creates the actual flask app
    """
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = "super secret key"

    @app.route('/', methods=['GET', 'POST'])
    def index():
        """
        Home page for the flask app that will allow users to see/make their schedule
        Also contains link to see all courses
        """

        global schedule
        global courses_to_display
        global expanded_course_to_display

        search_form = SearchForm()
        add_remove_form = AddRemoveForm()
        add_remove_notification_text = ""
        clear_all_courses_form = ClearAllCoursesForm()
        search_for_course_form = SearchForCourseForm()
        add_class_form = AddClassForm()
        view_sections_form = ViewSectionsForm()
        serialize_schedule_form = SerializeScheduleForm()
        serialized_schedule = None
        gen_ed_search_form = GenEdSearchForm()
        all_gen_ends = ["SCIS", "DVCC", "DVUP", "DSHS",
                        "DSHU", "DSNS", "DSNL", "DSSP",
                        "FSAW", "FSAR", "FSMA", "FSOC", "FSPW"]

        if search_for_course_form.search_for_course.data and \
                search_for_course_form.validate_on_submit():
            partial_course_code = search_for_course_form.search_query.data.upper()

            try:
                courses_to_display = APIGet.get_course_heads_by_query(partial_course_code)

                courses_to_display.sort(reverse=True,
                                        key=lambda this_course: (this_course.avg_gpa is not None, this_course.avg_gpa))
            except ConnectionError as e:
                add_remove_notification_text = str(e)

        if (add_remove_form.add.data or add_remove_form.remove.data) and add_remove_form.validate_on_submit():
            course_code = add_remove_form.course_query.data.upper()
            section_number = add_remove_form.section_query.data
            add_remove_notification_text = ""

            try:
                course_list_to_add = CourseList.get_course_using_course_code(course_code)
                if course_list_to_add.sections == {}:
                    raise ConnectionError("This course has no sections, please "
                                          "contact department for information to register for this course.")
                course_to_add = course_list_to_add.sections[section_number]

                if add_remove_form.add.data:
                    add_remove_notification_text = schedule.add_section(course_to_add)

                if add_remove_form.remove.data:
                    add_remove_notification_text = schedule.remove_section(course_to_add)

            except ConnectionError as e:
                add_remove_notification_text = str(e)

        if gen_ed_search_form.validate_on_submit():
            list_of_gen_eds_selected = request.form.getlist("gened")
            if len(list_of_gen_eds_selected) > 0:
                courses_to_display = APIGet.get_course_list_by_gen_ed(
                    gen_ed_search_form.department_id.data, list_of_gen_eds_selected[0])

        if clear_all_courses_form.clear_all.data and clear_all_courses_form.validate_on_submit():
            if schedule.total_credits == 0:
                clear_all_courses_form.clear_all.errors = ["Schedule is already empty"]

            schedule.remove_all_classes()
            add_remove_form.course_query.errors = []
            add_remove_form.section_query.errors = []

        if serialize_schedule_form.serialize_schedule.data and serialize_schedule_form.validate_on_submit():
            serialized_schedule = schedule.get_serialized_schedule()

        if serialize_schedule_form.load_schedule.data and serialize_schedule_form.validate_on_submit():
            schedule.load_serialized_schedule(serialize_schedule_form.display_serialized_schedule.data)

        # KEEP THIS IF STATEMENT LAST PLEASE!!!!
        # Changed to be a slightly different horrible hack
        if "add_course" in request.form:
            try:
                button_response = request.form['add_course']
                course_code = button_response.split(" ")[1]
                if expanded_course_to_display.course_code == course_code:
                    add_remove_notification_text = schedule.add_course(expanded_course_to_display)
                else:
                    course_to_add = CourseList.get_course_using_course_code(course_code)
                    add_remove_notification_text = schedule.add_course(course_to_add)

            except ConnectionError as e:
                add_remove_notification_text = str(e)

        if "add_section" in request.form:
            try:
                button_response = request.form['add_section']
                section_id = button_response.split(" ")[1]
                course_code = section_id.split("-")[0]
                section_number = section_id.split("-")[1]

                course_in_schedule = course_code in [course.course_code for course in schedule.courses_list]
                if course_in_schedule:
                    add_remove_notification_text = schedule.add_registered_course_section_by_id(section_id)
                else:
                    section_to_add = CourseList.get_course_using_course_code(course_code).sections[section_number]
                    add_remove_notification_text = schedule.add_section(section_to_add)

            except ConnectionError as e:
                add_remove_notification_text = str(e)

        if "view_course" in request.form:
            try:
                button_response = request.form['view_course']
                course_code = button_response.split(" ")[1]

                course_in_schedule = [course for course in schedule.courses_list
                                      if course.course_code == course_code]
                if course_in_schedule:
                    expanded_course_to_display = course_in_schedule[0]
                else:
                    expanded_course_to_display = CourseList.get_course_using_course_code(course_code)

            except ConnectionError as e:
                add_remove_notification_text = str(e)

        return render_template('index.html',
                               schedule=schedule,
                               search_form=search_form,
                               courses_to_display=courses_to_display,
                               add_remove_form=add_remove_form,
                               add_remove_notification_text=add_remove_notification_text,
                               clear_all_courses_form=clear_all_courses_form,
                               search_for_course_form=search_for_course_form,
                               add_class_form=add_class_form,
                               view_sections_form=view_sections_form,
                               expanded_course_to_display=expanded_course_to_display,
                               serialize_schedule_form=serialize_schedule_form,
                               serialized_schedule=serialized_schedule,
                               gen_ed_search_form=gen_ed_search_form,
                               all_gen_ends=all_gen_ends)

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

        professor = APIGet.get_professor_by_name(name, get_reviews="true")
        plantterp_link = "https://planetterp.com/professor/" + slug
        return render_template("professor_detail.html",
                               professor=professor,
                               plantterp_link=plantterp_link)

    @app.route('/tutorial', methods=['GET'])
    def tutorial():
        """"
        Tutorial page explaining how to use the schedule builder 
        """
        return render_template("tutorial.html")
        
    return app
