import unittest
from flask_app.model import MySchedule, CourseList


class TestUtils:
    course_list = CourseList()


class ScheduleTest(unittest.TestCase):

    def test_schedule_is_empty(self):
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_removing_class_not_in_schedule_doesnt_change_credits(self):
        class_to_try_to_remove = TestUtils.course_list.courses["CMSC250"].sections[0]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.remove_class(class_to_try_to_remove)
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_add_class_and_credits_and_schedule_correct(self):
        class_to_add = TestUtils.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.add_class(class_to_add)
        self.assertEqual(schedule.total_credits, 4)
        for day, day_list in schedule.schedule.items():
            if day != "F":
                self.assertEqual(len(day_list), 1)
            else:
                self.assertEqual(len(day_list), 0)

    def test_add_duplicate_class_and_credits_and_schedule_correct(self):
        class_to_add = TestUtils.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.add_class(class_to_add)
        schedule.add_class(class_to_add)  # duplicate add, won't go through
        self.assertEqual(schedule.total_credits, 4)
        for day, day_list in schedule.schedule.items():
            if day != "F":
                self.assertEqual(len(day_list), 1)
            else:
                self.assertEqual(len(day_list), 0)

    def test_add_class_then_remove_class_correct_credits_and_schedule(self):
        class_to_add = TestUtils.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.add_class(class_to_add)
        self.assertEqual(schedule.total_credits, 4)
        schedule.remove_class(class_to_add)
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_add_two_classes_correct_credits_and_schedule(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
        comm107 = TestUtils.course_list.courses["COMM107"].sections[-1]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.add_class(cmsc250)
        self.assertEqual(schedule.total_credits, 4)
        schedule.add_class(comm107)
        self.assertEqual(schedule.total_credits, 7)
        for day, day_list in schedule.schedule.items():
            if day == "F":
                self.assertEqual(len(day_list), 0)
            elif day == "M" or day == "W":
                self.assertEqual(len(day_list), 2)
            else:
                self.assertEqual(len(day_list), 1)


class ScheduleWarningTest(unittest.TestCase):
    def test_add_class_no_open_seats_makes_warning(self):
        # List comprehension syntax is really *chef's kiss*
        # This is definitely the simplest way to get a list of all filled sections, it's just hideous.
        full_sections = [section for sections in
                         [course.sections for course in TestUtils.course_list.courses.values()]
                         for section in sections if section.open_seats == 0]
        full_section = full_sections[0]

        schedule = MySchedule()
        self.assertEqual(schedule.warnings_list, [])
        schedule.add_class(full_section)
        self.assertIn("section full", [warning.warning_type for warning in schedule.warnings_list])

    def test_add_multiple_classes_no_open_seats_makes_warnings(self):
        full_sections = [section for sections in
                         [course.sections for course in TestUtils.course_list.courses.values()]
                         for section in sections if section.open_seats == 0]

        schedule = MySchedule()
        self.assertEqual(schedule.warnings_list, [])
        schedule.add_class(full_sections[0])
        self.assertIn("section full", [warning.warning_type for warning in schedule.warnings_list])
        schedule.add_class(full_sections[1])
        self.assertEqual(
            len([warning.warning_type for warning in schedule.warnings_list
                 if warning.warning_type == "section full"]),
            2)

    def test_remove_class_no_open_seats_removes_warnings(self):
        full_sections = [section for sections in
                         [course.sections for course in TestUtils.course_list.courses.values()]
                         for section in sections if section.open_seats == 0]
        full_section = full_sections[0]

        schedule = MySchedule()
        schedule.add_class(full_section)
        schedule.remove_class(full_section)
        self.assertNotIn("section full", [warning.warning_type for warning in schedule.warnings_list])

    def test_remove_multiple_classes_no_open_seats_removes_warnings(self):
        full_sections = [section for sections in
                         [course.sections for course in TestUtils.course_list.courses.values()]
                         for section in sections if section.open_seats == 0]

        schedule = MySchedule()
        self.assertEqual(schedule.warnings_list, [])
        schedule.add_class(full_sections[0])
        schedule.add_class(full_sections[1])
        schedule.remove_class(full_sections[0])
        self.assertEqual(
            len([warning.warning_type for warning in schedule.warnings_list
                 if warning.warning_type == "section full"]),
            1)
        schedule.remove_class(full_sections[1])
        self.assertNotIn("section full", [warning.warning_type for warning in schedule.warnings_list])

