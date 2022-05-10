# UMD Schedule Builder
The purpose of this repository is to create a UMD schedule builder. Students can use this application to create a 
schedule, view available professors and professor rating information, view all courses with corresponding GPA 
information, see the total number of credits in their schedule, and import/export their schedule to easily save or
continue where they left off!

### Schedule Builder - Home Page
Below is a screenshot of the web application's home page. On the header, there are links to 
"See All Courses" and to "See All Professors" which route the user to separate endpoints within
the site. The schedule is currently empty because the user has not added any sections to their course.
Below the schedule are several interactive elements for the user to help build their schedule. The first section includes
an area for the user to add/remove a specific section to/from their schedule. If the user is not certain which section they
want to add, they are free to search for a course and view all available sections from the query provided (e.g. searching
for "CMSC13" will return all courses starting with "CMSC13" for the user to choose from.) If the user wishes to restart
their schedule, they can easily wipe the schedule clean by clicking "Clear Schedule." Lastly, the user
can easily import/export their schedule. By clicking "Get Schedule Data", the user can copy a string which represents the
serialized schedule. If the user already has this serialized schedule string and wishes to reload their schedule later,
they can paste this string in the textbox and click "Load Schedule Data."

![Schedule Homescreen](/screenshots/schedule_homescreen.png?raw=true)
### Schedule Builder - Add a section to schedule
Below is a screenshot of the "Add a section to schedule" portion of the schedule builder. This form includes two
text boxes which allow the user to enter a course code (e.g. CMSC435) followed by a section number (e.g. 0101). The user
is then prompted to add or remove this section from their schedule by two buttons immediately preceding the input textboxes.
If the section cannot be added or remove from their schedule, an appropriate warning/reason will be displayed.

![Add section to schedule](/screenshots/add_section_to_schedule.png?raw=true)
### Schedule Builder - Search for a course
Below is a screenshot of the "Search for a course" portion of the schedule builder. This form allows the user to enter a
search query for a course. As an example, after searching for "CMSC131", a scrollable section is rendered
with all the courses beginning with "CMSC131". The screenshot below shows that CMSC131H, CMSC131, and CMSC131A are all 
valid courses from the given query. The user can now add the course to their schedule, or can view all 
available sections for a given course and can then add a specific section to their schedule.

![Search for a course](/screenshots/search_for_course.png?raw=true)
### Schedule Builder - View sections of a course
Below is a screenshot of the same form after the user selected to "View CMSC131 sections". A different scrollable
section is rendered to the right of the search query results. This portion is sorted by professor. Under each professor,
average PlanetTerp rating information and average GPA information for that course taught by that professor
is also displayed. Each section of the course includes information about the number of seats available and the meeting 
times of that specific section. The user can browse the available sections and if a section fits their criteria, they
can easily add a specific section to their schedule with a click of a button.

![View sections of a course](/screenshots/view_sections_after_searching_for_course.png?raw=true)
### Schedule Builder - View the Schedule After Adding a Section
Below is a screenshot of the home page after the user added CMSC131-0101. In this example, the user clicked the button
under the "Search for a course" portion to "Add CMSC131-0101", but they also could have added CMSC131-0101 through the
"Add a section to schedule" form. Notice that the schedule displays the meeting times of CMSC131-0101, and the average
schedule GPA, total credits, and courses in the current schedule were updated appropriately as well.

![Add specific course section to schedule](/screenshots/schedule_after_adding_section.png?raw=true)
### Schedule Builder - Get Schedule Data
Below are two screenshots of the home page after the user added CHEM135-3125, CMSC131-0101, and INAG110-0501. The user
then selected to "Get Schedule Data" (as shown in the second screenshot) and a string was displayed for the user to copy.
If the user wishes to come back to the schedule builder at a later time and continue progress, they can paste the same
string into the text box and click "Load Schedule Data" to continue with their schedule as they left it.

![View Schedule with Multiple Classes](/screenshots/multiple_classes_in_schedule.png?raw=true)
![Get Schedule Data](/screenshots/export_schedule.png?raw=true)
### See All Courses
Below is a screenshot of the "See All Courses" tab of the web application. This can be accessed by clicking the
shortcut on the banner at the top of the screen. This endpoint loads all the courses for the current academic term in
alphabetical order and lists the following information: number of credits, average GPA of course, available sections,
and the meeting times and seats available for each section.

![See All Courses](/screenshots/see_all_courses.png?raw=true)
### See All Professors
Below is a screenshot of the "See All Professors" tab of the web application. This can be accessed by clicking the
shortcut on the banner at the top of the screen. This endpoint loads all the professors. Beneath each professor
is their average PlanetTerp rating and a link to visit the professor's page which includes review information.

The second screenshot shows an example of a Professor's page (in this case, Auguste Gezalyan.) The Professor review page
shows the average rating, the type (e.g. lecturer, TA, etc.), a link to the PlanetTerp review page, courses they are
teaching in the current academic year, and finally a list of reviews by real students taken from PlanetTerp!

![See All Professors](/screenshots/see_all_professors.png?raw=true)
![Visit Professor Page](/screenshots/professor_review.png?raw=true)

## Accessing the app via the cloud
[https://cmsc435.herokuapp.com/]

## Running with Docker  

1. Navigate to the root directory, team-project/
2. Build the image by running the following command:

`docker build -t schedule-builder .`

3. Run the image by running the following command:

`docker run --publish 8000:5000 --rm schedule-builder`

4. Open the application in your browser at `localhost:8000`

5. To kill the docker session, navigate to Docker Desktop and kill the appropriate container.


## Running without Docker (for devs)

1. Python and pip should be installed.
2. In root directory, run:

`pip3 install -r requirements.txt`

This should install Flask and all required libraries.
3. Inside the root directory, run:

`flask run`

4. The console will tell you the address where the app is being hosted on your machine.


## Project structure

The project has two main directories, flask_app and tests. flask_app contains all components required to run the Flask application, and tests contains all tests for backend functionality. The Dockerfile and requirements.txt file in the root directory are used to set up the application when cloned.

### flask_app

* `backend/courses.py` contains backend code for courses and sections.

* `backend/schedule.py` contains backend code for the schedule.

* `forms.py` contains WTForms forms which are used to handle user input.

* `app.py` contains the different pages which the app can display.


Inside the templates directory are the html files to display the pages of the app.

Inside the static directory are the screenshots used for the tutorial page.



### tests

* `test_schedule.py` contains tests relating to the backend functionality of the MySchedule class, which represents a user's schedule.
* `test_courses.py` contains tests for the API to check that the code is properly getting course information
* `test_app.py` contains tests for the front end flask UI
* `utils.py` contains utility code for the tests to use
* `data_for_tests.json` contains course information that allows manual construction of Course objects for testing

### screenshots
* Contains screenshots of the web app. These images are used in the README

### docs
* Contains all sphinx documentation and the files necessary to automatically generate documentation

### Other

* `requirements.txt` contains the package dependencies to be installed
* `Dockerfile` contains the code needed to run the Docker image
* `Procfile` contains the command to help with cloud deployment 
* `run.py` contains code needed to find the flask app to launch it 
* `.flaskenv` contains environment variables needed for the flask app

## How to run Tests
1. Navigate to GitLab
2. CI/CD tab on left panel
3. Click blue `Run Pipeline` button at top right corner
4. Select branch (`main`) and run the pipeline. Tests will also automatically run upon any changes made to the GitLab repository. 

## Contributions (Sprint 3)
*Amar (20%)*: I modified the partial course search results to sort by the Average GPA of the class, descending. I also changed the sorting of sections to be based on the professor rating on planetterp, highest to lowest. 

*Michelle (20%)*: I created a flask route for all professors and then a route for every professor. Each professor has a page with information such as reviews for that professors, the courses they teach, rating, etc. I added front end testing for flask routes. I deployed the app to the cloud. 

*Daniel (20%)*: I added the tutorial page which will give the user an overview of how to build a schedule and use the different tools. I also added the sphinx documentation and cleaned up certain comments to make them comply with the sphinx required format.

*Andrew (20%)*: I added the ability for users to serialize/deserialize their schedules. This is a method of saving their schedules without using user accounts or cookies. I also added the repo badges and added detailed app instructions/screenshots to the README.

*Tyler (20%)*: Changed the process of adding courses to the schedule by separating the addition into adding courses and sections separate from one another. Improved speed of the application by reducing API calls whenever possible. Added the ability to search for courses based on general education credits. Made it possible for multiple users to use the application at the same time while deployed.

## Contributions (Sprint 2)
*Amar (20%)*: Created Professor Object, retrieved average professor rating from API and listed it in search results, added Average GPA in Course List as well. Added subsequent tests for basic Professor API results. 

*Michelle (20%)*: Hooked up the schedule with the umd.io API to obtain course information from. Revised the tests to reflect this new code. Added front end flask tests. Added number of credits to the schedule. 


*Daniel (20%)*: Added a list of all courses that the user currently has on their schedule. Also added a readout of the total credits of the current schedule. Fixed some warnings that were popping up unintentionally and added appropriate warnings for a few other cases. 

*Andrew (20%)*: Added drop down menu for users to search for a course name (e.g. cmsc435) and then a list is populated sorted by professor with all of the sections of that course. This includes information such as gpa, open seats, etc. There is also an add button next to the section for the user to click once to add that section to their schedule. Added backend support for getting grade information by professor and calculated gpa per course per professor (different from the average course gpa.) Added tests for all new functions. 

*Tyler (20%)*: Integrated planetterp API. Combined API implementations with umd.io API. Implemented API testing.

## Contributions (Sprint 1)
*Amar (20%)*: Created UI for adding a specific section of a class to the schedule, added sections, days, and times to All Course List, Colorized Schedule based on sections. 20%.

*Michelle (20%)*: Set up the flask app front end to display courses in an HTML table with their time and course code. Also set up the front end for a hyperlink to see all courses and for a search bar. Implemented the CI/CD automated testing.

*Daniel (20%)*: Completed the backend, frontend, and integration of the remove all classes feature. Created the structure for having multiple Flask WTForms on one page with unique functionalities. Created the scrum log portions of the wiki and took notes during scrums. Assisted in setting up the structure of our issues, labels, and backlogs. 

*Andrew (20%)*: Created MySchedule, MeetingTime, Section, CourseList, and Course classes in backend. Parsed information from json file to create a complete CourseList and built resulting Course, Section, and MeetingTime objects from the original json for easy field access in backend. Implemented add_class and remove_class functions in MySchedule class, and also ensured that class meeting times are ordered in the schedule and include no time conflicts or duplicates.

*Tyler (20%)*: Located and imported course data to be used for Sprint 1. Added frontend and backend systems for warning the user of sections with no open seats available. Added frontend integration of adding/removing single classes. Added frontend and backend system to notify user of the result of trying to add/remove a class. Dockerized the application.
