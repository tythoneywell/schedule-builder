# team project

(Temporary) Instructions to run Flask app

- Python and pip should be installed.
- In root directory, run:
pip3 install -r requirements.txt
This should install Flask and all required libraries.
- Inside the flask_app directory, run:
flask run 
- The console will tell you the address where the app is being hosted on your machine.


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

*Tyler (20%)*:
