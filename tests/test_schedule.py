import unittest
from flask_app.schedule import MySchedule
from flask_app.courses import CourseList


class TestUtils:
    course_list = CourseList()


class ScheduleTest(unittest.TestCase):
    """
    Tests for the add_class and remove_class functions of MySchedule.
    """

    def test_schedule_is_empty(self):
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_removing_class_not_in_schedule_doesnt_change_credits(self):
        class_to_try_to_remove = TestUtils.course_list.courses["CMSC250"].sections["0101"]  # getting section 0101
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.remove_class(class_to_try_to_remove)
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_add_class_and_credits_and_schedule_correct(self):
        class_to_add = TestUtils.course_list.courses["CMSC250"].sections["0307"]
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
        class_to_add = TestUtils.course_list.courses["CMSC250"].sections["0307"]
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
        class_to_add = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.add_class(class_to_add)
        self.assertEqual(schedule.total_credits, 4)
        schedule.remove_class(class_to_add)
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_add_two_classes_correct_credits_and_schedule(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
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

    def test_add_two_classes_make_sure_ordered_by_time(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
        schedule = MySchedule()
        schedule.add_class(cmsc250)
        schedule.add_class(comm107)
        self.assertEqual(schedule.schedule["M"][0].section_id, "CMSC250-0307")
        self.assertEqual(schedule.schedule["M"][1].section_id, "COMM107-FC04")
        self.assertEqual(schedule.total_credits, 7)

    def test_try_to_add_overlapping_classes_only_first_gets_added(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0306"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
        schedule = MySchedule()
        schedule.add_class(comm107)
        self.assertEqual(schedule.total_credits, 3)
        schedule.add_class(cmsc250)  # can't add this class
        self.assertEqual(schedule.total_credits, 3)
        self.assertEqual(schedule.schedule["M"][0].section_id, "COMM107-FC04")

    def test_remove_all_classes_on_empty_schedule(self):
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.remove_all_classes()
        self.assertEqual(schedule.total_credits, 0)
        for day, classes in schedule.schedule.items():
            self.assertEqual(len(classes), 0)

    def test_remove_all_classes_on_schedule_with_classes_in_it(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
        schedule = MySchedule()
        schedule.add_class(comm107)
        schedule.add_class(cmsc250)
        self.assertEqual(schedule.total_credits, 7)
        schedule.remove_all_classes()
        self.assertEqual(schedule.total_credits, 0)
        for day, classes in schedule.schedule.items():
            self.assertEqual(len(classes), 0)

    def test_class_overlap_same_class(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        cmsc250_2 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        schedule = MySchedule()
        schedule.add_class(cmsc250)
        self.assertFalse(schedule.no_class_overlap(cmsc250_2))

    def test_class_overlap_different_class_time_conflict(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0306"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
        schedule = MySchedule()
        schedule.add_class(cmsc250)
        self.assertFalse(schedule.no_class_overlap(comm107))

    def test_class_with_no_time_conflict(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        comm107 = TestUtils.course_list.courses["COMM107"].sections["FC04"]
        schedule = MySchedule()
        schedule.add_class(cmsc250)
        self.assertTrue(schedule.no_class_overlap(comm107))
        schedule.remove_all_classes()
        schedule.add_class(comm107)
        self.assertTrue(schedule.no_class_overlap(cmsc250))

    def test_try_to_add_class_in_middle_of_day_start_time_overlaps_with_previous_end_time(self):
        cmsc250 = TestUtils.course_list.courses["CMSC250"].sections["0307"]
        anth221 = TestUtils.course_list.courses["ANTH221"].sections["FC01"]
        chem271 = TestUtils.course_list.courses["CHEM271"].sections["2247"]
        schedule = MySchedule()
        schedule.add_class(cmsc250)
        schedule.add_class(anth221)
        self.assertFalse(schedule.no_class_overlap(chem271))
        schedule.add_class(chem271)  # try to add chem in between even though its start time overlaps with 250 end time
        self.assertEqual(schedule.total_credits, 7)


class ScheduleWarningTest(unittest.TestCase):
    """
    Tests for ScheduleWarnings generated by MySchedule.
    """

    def test_add_class_no_open_seats_makes_warning(self):
        # List comprehension syntax is really *chef's kiss*
        # This is definitely the simplest way to get a list of all filled sections, it's just hideous.
        full_sections = [section for sections in
                         [course.sections.values() for course in TestUtils.course_list.courses.values()]
                         for section in sections if section.open_seats == 0]
        full_section = full_sections[0]

        schedule = MySchedule()
        self.assertEqual(schedule.warnings_list, [])
        schedule.add_class(full_section)
        self.assertIn("section full", [warning.warning_type for warning in schedule.warnings_list])

    def test_add_multiple_classes_no_open_seats_makes_warnings(self):
        full_sections = [section for sections in
                         [course.sections.values() for course in TestUtils.course_list.courses.values()]
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
                         [course.sections.values() for course in TestUtils.course_list.courses.values()]
                         for section in sections if section.open_seats == 0]
        full_section = full_sections[0]

        schedule = MySchedule()
        schedule.add_class(full_section)
        schedule.remove_class(full_section)
        self.assertNotIn("section full", [warning.warning_type for warning in schedule.warnings_list])

    def test_remove_multiple_classes_no_open_seats_removes_warnings(self):
        full_sections = [section for sections in
                         [course.sections.values() for course in TestUtils.course_list.courses.values()]
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
