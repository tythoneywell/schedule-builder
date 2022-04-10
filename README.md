# UMD Schedule Builder


## Running with Docker

1. Navigate to the root directory, team-project/
2. Build the image by running the following command:

docker build -t schedule-builder .

3. Run the image by running the following command:

docker run --publish 8000:5000 --rm schedule-builder

4. Open the application in your browser at "localhost:8000"

5. To kill the docker session, navigate to Docker Desktop and kill the appropriate container.


## Running without Docker (for devs)

1. Python and pip should be installed.
2. In root directory, run:

pip3 install -r requirements.txt

This should install Flask and all required libraries.
3. Inside the flask_app directory, run:

flask run 
4. The console will tell you the address where the app is being hosted on your machine.


## Project structure

The project has two main directories, flask_app and tests. flask_app contains all components required to run the Flask application, and tests contains all tests for backend functionality. The Dockerfile and requirements.txt file in the root directory are used to set up the application when cloned.

### flask_app

model.py contains backend code, including the classes for schedules, courses, and sections.

forms.py contains WTForms forms which are used to handle user input.

app.py contains the different pages which the app can display.


Inside the templates directory are the html files to display the pages of the app.

Inside the data directory is the file that stores all course and section information, fall2020data.json.

### tests

test_schedule.py contains tests relating to the backend functionality of the MySchedule class, which represents a user's schedule.

## How to run Tests
1. Navigate to GitLab
2. CI/CD tab on left panel
3. Click blue `Run Pipeline` button at top right corner
4. Select branch (`main`) and run the pipeline. Tests will also automatically run upon any changes made to the GitLab repository. 

## Contributions
*Amar (20%)*: Created UI for adding a specific section of a class to the schedule, 
    added sections, days, and times to All Course List, Colorized Schedule based
    on sections. 20%.

*Michelle (20%)*: Set up the flask app front end to display courses in an HTML table with their time and course code. Also set up the front end for a hyperlink to see all courses and for a search bar. Implemented the CI/CD automated testing.

*Daniel (20%)*: Completed the backend, frontend, and integration of the remove all classes feature. Created the structure for having multiple Flask WTForms on one page with unique functionalities. Created the scrum log portions of the wiki and took notes during scrums. Assisted in setting up the structure of our issues, labels, and backlogs. 

*Andrew (20%)*: Created MySchedule, MeetingTime, Section, CourseList, and Course classes in backend. Parsed information from json file to create a complete CourseList and built resulting Course, Section, and MeetingTime objects from the original json for easy field access in backend. Implemented add_class and remove_class functions in MySchedule class, and also ensured that class meeting times are ordered in the schedule and include no time conflicts or duplicates.

*Tyler (20%)*: Located and imported course data to be used for Sprint 1. Added frontend and backend systems for warning the user of sections with no open seats available. Added frontend integration of adding/removing single classes. Added frontend and backend system to notify user of the result of trying to add/remove a class. Dockerized the application.
