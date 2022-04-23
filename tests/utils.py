from flask_app.backend.courses import CourseList, Course, Section
import os
import json


class TestUtils:
    """
    Load in some hard coded course data that doesn't depend on API to test schedule logic
    """

    def __init__(self):
        all_courses_list_raw = json.load(open(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/tests/data_for_tests.json"))
        self.courses = {}  # dictionary mapping course name (string) to a Course object
        for courses in all_courses_list_raw:
            course_id = courses["course_id"]
            course_name = courses["name"]
            course_credits = int(courses["credits"])
            sections = courses["sections"]
            section_dict = {}
            professor_to_sections = {}
            professor_to_avg_course_gpa = {}
            course_obj = Course(course_id, course_name, course_credits, section_dict, professor_to_sections,
                                professor_to_avg_course_gpa)

            # populate the sections of the specific course
            for section in sections:
                section_id = section["section_id"]
                section_number = section["number"]
                total_seats = int(section["seats"])
                open_seats = int(section["open_seats"])
                class_meetings = CourseList.make_meeting_dict(section["meetings"], section_id)
                is_synchronous = False
                for meeting in class_meetings.values():
                    if len(meeting) != 0:
                        is_synchronous = True
                professor = section["instructors"]
                section_dict[section_number] = Section(course_id, section_id, total_seats, open_seats,
                                                       class_meetings, professor, course_obj, is_synchronous)

            self.courses[course_id] = course_obj
