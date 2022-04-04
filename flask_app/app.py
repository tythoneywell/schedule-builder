from flask import Flask, render_template, redirect, url_for
from model import MyClass
from forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key"


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

    # Example of how to render index.html
    courses = [MyClass("CMSC131", "9AM - 10AM", "Nelson", 3.8, ), MyClass("CMSC132", "2 PM - 3 PM", "Yoon", 3.5)]
    monday_classes = [MyClass("CMSC131", "9AM - 10AM", "Nelson", 3.8, )]
    friday_classes = [MyClass("CMSC132", "2 PM - 3 PM", "Yoon", 3.5)]

    return render_template('index.html',
                           courses=courses,
                           monday_classes=monday_classes,
                           friday_classes=friday_classes,
                           form=form)


@app.route('/all_courses')
def all_courses():
    """"
    Display a list of all courses that the student could try to sign up for
    """

    # Example of how to render the all_courses.html
    courses = [MyClass("CMSC131", "9AM - 10AM", "Nelson", 3.8), MyClass("CMSC132", "2 PM - 3 PM", "Yoon", 3.5)]
    return render_template('all_courses.html',
                           courses=courses)
