import unittest
from flask_app.backend.courses import CourseList


class TestUtils:
    course_list = CourseList()


class CourseListTest(unittest.TestCase):
    def test_get_courses_using_course_code_valid_course_code(self):
        cmsc250 = CourseList.get_courses_using_course_code("CMSC250")
        self.assertEqual(cmsc250.course_code, "CMSC250")

        chem271 = CourseList.get_courses_using_course_code("CHEM271")
        self.assertEqual(chem271.course_code, "CHEM271")

    def test_get_courses_using_course_code_invalid_course_code_throws_exception(self):
        try:
            cmsc250 = CourseList.get_courses_using_course_code("CMSC250hahaha")
        except Exception as e:
            self.assertEqual(str(e), "Course Code Not Found")

        try:
            cc = CourseList.get_courses_using_course_code("CC")
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
        cmsc250 = CourseList.get_courses_using_course_code("CMSC250").sections["0101"]
        comm107 = CourseList.get_courses_using_course_code("COMM107").sections["0201"]
        self.assertEqual({'4:00pm-4:50pm': 'MW', '2:00pm-3:15pm': 'TuTh'},
                         cmsc250.get_formatted_weekly_schedule())
        self.assertEqual({'8:00am-8:50am': 'MWF'}, comm107.get_formatted_weekly_schedule())

