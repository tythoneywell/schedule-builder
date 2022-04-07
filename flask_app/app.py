from flask import Flask, render_template, redirect, url_for
from flask_app.model import MySchedule, CourseList
from flask_app.forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key"
course_list = CourseList()  # populate the course list from the big json file


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page for the flask app that will allow users to see/make their schedule
    Also contains link to see all courses
    """

    form = SearchForm()

    if form.validate_on_submit():
        # Use form.search_query.data to access the query the user typed in
        return redirect(url_for('index'))

    schedule = MySchedule()
    cmsc250 = course_list.courses.get("CMSC250")
    comm107 = course_list.courses.get("COMM107")
    schedule.add_class(cmsc250.sections[-2])  # get the 2nd to last 250 section
    schedule.add_class(comm107.sections[-1])  # get the 1st section of comm107

    return render_template('index.html',
                           schedule=schedule,
                           form=form)


@app.route('/all_courses')
def all_courses():
    """"
    Display a list of all courses that the student could try to sign up for
    """
    return render_template('all_courses.html',
                           courses=course_list.courses)
