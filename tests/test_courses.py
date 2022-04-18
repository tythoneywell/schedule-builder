import unittest
from flask_app.backend.courses import CourseList, Course, Section, APIGet
from tests.utils import TestUtils

test_util_instance = TestUtils()

class CourseListTest(unittest.TestCase):
    """
    Test functions in the CourseList class, which is primarily responsible for
    interacting with the API, so this also tests the API functions as supposed to
    """

    def test_get_courses_using_course_code_valid_course_code(self):
        cmsc250 = CourseList.get_course_using_course_code("CMSC250")
        self.assertEqual(cmsc250.course_code, "CMSC250")

        chem271 = CourseList.get_course_using_course_code("CHEM271")
        self.assertEqual(chem271.course_code, "CHEM271")

    def test_get_courses_using_course_code_invalid_course_code_throws_exception(self):
        try:
            CourseList.get_course_using_course_code("CMSC250hahaha")
        except Exception as e:
            self.assertEqual(str(e), "Course Code Not Found")

        try:
            CourseList.get_course_using_course_code("CC")
        except Exception as e:
            self.assertEqual(str(e), "Course Code Not Found")

    def test_get_courses_using_valid_page_number(self):
        courses = CourseList.get_courses_using_page_number(1)
        self.assertEqual(len(courses), 30)
        self.assertTrue("AASP100" in courses.keys())

        courses = CourseList.get_courses_using_page_number(10)
        self.assertEqual(len(courses), 30)

    def test_get_courses_using_invalid_page_number(self):
        courses = CourseList.get_courses_using_page_number(100000)
        self.assertEqual(len(courses), 0)


class CourseTest(unittest.TestCase):
    def test_class_formatted_weekly_schedule_correct(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        comm107 = test_util_instance.courses["COMM107"].sections["FC04"]
        self.assertEqual({'8:00am-8:50am': 'MW', '3:30pm-4:45pm': 'TuTh'},
                         cmsc250.get_formatted_weekly_schedule())
        self.assertEqual({'4:30pm-5:45pm': 'MW'}, comm107.get_formatted_weekly_schedule())
