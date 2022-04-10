import unittest
from flask_app.backend.courses import CourseList


class TestUtils:
    course_list = CourseList()


class CourseTest(unittest.TestCase):
    def test_class_formatted_weekly_schedule_correct(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
        self.assertEqual({'8:00am-8:50am': 'MW', '3:30pm-4:45pm': 'TuTh'},
                         cmsc250.get_formatted_weekly_schedule())
        self.assertEqual({'4:30pm-5:45pm': 'MW'}, comm107.get_formatted_weekly_schedule())
