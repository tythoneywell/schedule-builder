import os
import unittest
from flask_app.model import MySchedule, CourseList


class ModelsTest(unittest.TestCase):
    if "tests" in os.getcwd():  # this is needed to get into the correct directory to open the course list file
        os.chdir("../")
    course_list = CourseList()

    def test_schedule_is_empty(self):
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_removing_class_not_in_schedule_doesnt_change_credits(self):
        class_to_try_to_remove = ModelsTest.course_list.courses["CMSC250"].sections[0]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.remove_class(class_to_try_to_remove)
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_add_class_and_credits_and_schedule_correct(self):
        class_to_add = ModelsTest.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
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
        class_to_add = ModelsTest.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
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
        class_to_add = ModelsTest.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
        schedule = MySchedule()
        self.assertEqual(schedule.total_credits, 0)
        schedule.add_class(class_to_add)
        self.assertEqual(schedule.total_credits, 4)
        schedule.remove_class(class_to_add)
        self.assertEqual(schedule.total_credits, 0)
        for day, day_list in schedule.schedule.items():
            self.assertEqual(len(day_list), 0)

    def test_add_two_classes_correct_credits_and_schedule(self):
        cmsc250 = ModelsTest.course_list.courses["CMSC250"].sections[-2]  # getting first section of 250
        comm107 = ModelsTest.course_list.courses["COMM107"].sections[-1]  # getting first section of 250
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
