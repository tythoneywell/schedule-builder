import requests
import os
import json


class Course(object):
    def __init__(self, course_code: str, name: str, course_credits: int, sections: list):
        self.sess = requests.Session()
        self.course_code = course_code
        self.name = name
        self.credits = course_credits
        self.sections = sections


# class which includes information of a section from a specific course
class Section(object):
    def __init__(self, course_code: str, section_id: str, total_seats: int, open_seats: int, class_meetings: list,
                 professor: str, gpa: float, course: Course):
        self.sess = requests.Session()
        self.course_code = course_code
        self.section_id = section_id
        self.total_seats = total_seats
        self.open_seats = open_seats
        self.class_meetings = class_meetings
        self.professor = professor
        self.gpa = gpa
        self.course = course


class MySchedule(object):
    def __init__(self):
        self.schedule = {"M": [],
                         "Tu": [],
                         "W": [],
                         "Th": [],
                         "F": []}
        self.total_credits = 0
        self.class_list = []

    def add_class(self, class_to_add: Section):
        if class_to_add in self.class_list:
            return

        self.total_credits += class_to_add.course.credits
        for class_meetings in class_to_add.class_meetings:
            if "M" in class_meetings["days"]:
                self.schedule["M"].append(class_to_add)
            if "Tu" in class_meetings["days"]:
                self.schedule["Tu"].append(class_to_add)
            if "W" in class_meetings["days"]:
                self.schedule["W"].append(class_to_add)
            if "Th" in class_meetings["days"]:
                self.schedule["Th"].append(class_to_add)
            if "F" in class_meetings["days"]:
                self.schedule["F"].append(class_to_add)
        self.class_list.append(class_to_add)

    def remove_class(self, class_to_remove: Section):
        class_previously_in_schedule = False
        for day, classes in self.schedule.items():
            new_day_list = []
            for one_class in classes:
                if one_class != class_to_remove:
                    new_day_list.append(one_class)
                else:
                    class_previously_in_schedule = True
            self.schedule[day] = new_day_list
        if class_previously_in_schedule:
            self.class_list.remove(class_to_remove)
            self.total_credits -= class_to_remove.course.credits

    def remove_all_classes(self):
        """
        This function will be used as a way to reset the schedule to blank (no classes) in one click.
        """
        self.schedule = {"M": [],
                         "Tu": [],
                         "W": [],
                         "Th": [],
                         "F": []}
        self.total_credits = 0
        self.class_list = []


class CourseList(object):
    def __init__(self):
        all_courses_list_raw = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/data/fall2020data.json"))
        self.courses = {}  # dictionary mapping course name (string) to a Course object
        for courses in all_courses_list_raw:
            course_id = courses["course_id"]
            course_name = courses["name"]
            course_credits = int(courses["credits"])
            sections = courses["sections"]
            section_list = []
            course_obj = Course(course_id, course_name, course_credits, section_list)

            # populate the sections of the specific course
            for section in sections:
                section_id = section["section_id"]
                total_seats = int(section["seats"])
                open_seats = int(section["open_seats"])
                class_meetings = section["meetings"]
                professor = section["instructors"]
                gpa = 3.5
                section_list.append(
                    Section(course_id, section_id, total_seats, open_seats, class_meetings, professor, gpa, course_obj))

            self.courses[course_id] = course_obj

