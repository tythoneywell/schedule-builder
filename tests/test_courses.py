import unittest
from flask_app.backend.courses import CourseList, APIGet, RequestProxy
from tests.utils import TestUtils

test_util_instance = TestUtils()


class CourseListTest(unittest.TestCase):
    """
    Test functions in the CourseList class, which is primarily responsible for
    interacting with the API, so this also tests the API functions as supposed to
    """
    def setUp(self):
        RequestProxy.test_mode = True

    def tearDown(self):
        RequestProxy.test_mode = False

    def test_get_courses_using_course_code_valid_course_code(self):
        RequestProxy.bad_request = False
        cmsc250 = CourseList.get_course_using_course_code("CMSC250")
        self.assertEqual(cmsc250.course_code, "MATH140")  # Using API emulator

        chem271 = CourseList.get_course_using_course_code("CHEM271")
        self.assertEqual(chem271.course_code, "MATH140")

    def test_get_courses_using_course_code_invalid_course_code_throws_exception(self):
        RequestProxy.bad_request = True
        try:
            CourseList.get_course_using_course_code("CMSC250hahaha")
        except Exception as e:
            self.assertEqual(str(e), "Course Code Not Found")

        try:
            CourseList.get_course_using_course_code("CC")
        except Exception as e:
            self.assertEqual(str(e), "Course Code Not Found")

    def test_get_courses_using_valid_page_number(self):
        RequestProxy.bad_request = False
        courses = CourseList.get_courses_using_page_number(1)
        self.assertEqual(len(courses), 1)  # Using API emulator

        courses = CourseList.get_courses_using_page_number(10)
        self.assertEqual(len(courses), 1)

    def test_get_courses_using_invalid_page_number(self):
        RequestProxy.bad_request = True
        courses = CourseList.get_courses_using_page_number(100000)
        self.assertEqual(len(courses), 0)


class CourseTest(unittest.TestCase):
    """
    Test functions in the classes related to Courses (e.g. Section, Course, MeetingTime, etc.). It does not test
    the API calls
    """

    def test_class_formatted_weekly_schedule_correct(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        comm107 = test_util_instance.courses["COMM107"].sections["FC04"]
        self.assertEqual({'8:00am-8:50am': 'MW', '3:30pm-4:45pm': 'TuTh'},
                         cmsc250.get_formatted_weekly_schedule())
        self.assertEqual({'4:30pm-5:45pm': 'MW'}, comm107.get_formatted_weekly_schedule())

    def test_meeting_time_not_equal_to_non_meeting_time_object(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        meeting_times_dict = cmsc250.class_meetings
        self.assertNotEqual(meeting_times_dict["M"][0], "meeting time string")

    def test_meeting_times_are_equal_according_to_eq_function(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        meeting_times_dict = cmsc250.class_meetings
        self.assertEqual(meeting_times_dict["M"][0], meeting_times_dict["M"][0])

    def test_meeting_times_are_not_equal_according_to_eq_function(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        comm107 = test_util_instance.courses["COMM107"].sections["FC04"]
        meeting_times_cmsc250_dict = cmsc250.class_meetings
        meeting_times_comm107_dict = comm107.class_meetings
        self.assertNotEqual(meeting_times_cmsc250_dict["M"][0], meeting_times_comm107_dict["M"][0])

    def test_hashes_of_different_meetings_times_are_different_too(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        comm107 = test_util_instance.courses["COMM107"].sections["FC04"]
        meeting_times_cmsc250_dict = cmsc250.class_meetings
        meeting_times_comm107_dict = comm107.class_meetings
        self.assertNotEqual(hash(meeting_times_cmsc250_dict["M"][0]), hash(meeting_times_comm107_dict["M"][0]))

    def test_hashes_of_same_meetings_times_are_same(self):
        cmsc250 = test_util_instance.courses["CMSC250"].sections["0307"]
        meeting_times_cmsc250_dict = cmsc250.class_meetings
        self.assertEqual(hash(meeting_times_cmsc250_dict["M"][0]), hash(meeting_times_cmsc250_dict["M"][0]))

    def test_course_correct_professor_rating_static_method(self):
        professor_json = APIGet.get_professor_by_name("Erin Callahan")
        self.assertEqual(5.0, professor_json.average_rating)


class APIGetAndParseTest(unittest.TestCase):
    """
    Test functions in the APIGet and APIParse classes, which consist of several static helper methods to call
    the Planetterp and umdio APIs, and parse the returned data into objects
    """

    def test_get_course_heads_make_sure_all_courses_we_expect_are_present(self):
        cmsc_courses = APIGet.get_course_heads_by_query("CMSC")
        self.assertEqual(len(cmsc_courses), 30)  # 30 CMSC courses offered this semester

    def test_professor_object_returned_valid_name(self):
        professor_json = APIGet.get_professor_by_name("Clyde Kruskal")
        self.assertEqual('Clyde Kruskal', professor_json.name)

    def test_professor_object_returned_valid_rating(self):
        professor_json = APIGet.get_professor_by_name("Erin Callahan")
        self.assertEqual(5.0, professor_json.average_rating)

    def test_professor_object_returned_valid_courselist(self):
        professor_json = APIGet.get_professor_by_name("David Mount")
        self.assertEqual(set(professor_json.course_list), {'CMSC388D', 'CMSC420', 'CMSC425',
                                                           'CMSC427', 'CMSC451', 'CMSC754', 'CMSC798'})

    def test_professor_object_returned_valid_instructor_type(self):
        professor_json = APIGet.get_professor_by_name("Justin Wyss-Gallifent")
        self.assertEqual('professor', professor_json.instructor_type)
