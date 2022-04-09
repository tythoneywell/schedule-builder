from collections import defaultdict

import requests
import os
import json
import re
from datetime import datetime


class Course(object):
    def __init__(self, course_code: str, name: str, course_credits: int, sections: dict):
        self.sess = requests.Session()
        self.course_code = course_code
        self.name = name
        self.credits = course_credits
        self.sections = sections


# class which includes information of a section from a specific course
class Section(object):
    def __init__(self, course_code: str, section_id: str, total_seats: int, open_seats: int, class_meetings: dict,
                 professor: str, gpa: float, course: Course):
        self.color = None
        self.sess = requests.Session()
        self.course_code = course_code
        self.section_id = section_id
        self.total_seats = total_seats
        self.open_seats = open_seats
        self.class_meetings = class_meetings
        self.professor = professor
        self.gpa = gpa
        self.course = course

    def set_color(self, color: str):
        self.color = color
        for day, classes in self.class_meetings.items():
            for meeting_time in classes:
                meeting_time.color = color

    def get_formatted_weekly_schedule(self):
        time_per_day = dict()
        for day, meeting_time_list in self.class_meetings.items():
            if len(meeting_time_list) > 0:
                for meeting_time in set(meeting_time_list):
                    temp = meeting_time.formatted_start_time + "-" + meeting_time.formatted_end_time
                    if temp in time_per_day:
                        time_per_day[temp] = time_per_day[temp] + day + ""
                    else:
                        time_per_day[temp] = day

        return time_per_day


class MySchedule(object):

    def __init__(self):
        #  dictionary of day of week to MeetingTime
        self.schedule = {"M": [],
                         "Tu": [],
                         "W": [],
                         "Th": [],
                         "F": []}
        self.total_credits = 0
        self.class_list = []

        self.warnings_list = []

    def no_class_overlap(self, class_to_add: Section):
        for day, class_meeting in class_to_add.class_meetings.items():
            for class_time in class_meeting:
                class_to_add_start_time = class_time.start_time
                class_to_add_end_time = class_time.end_time
                for class_index in range(len(self.schedule[day])):
                    single_class = self.schedule[day][class_index]
                    if single_class.start_time > class_to_add_start_time:  # try to add our class right before this
                        if class_to_add_end_time >= single_class.start_time:  # can't add this specific class slot
                            return False
                        if class_index > 0 and \
                                self.schedule[day][class_index - 1].end_time >= \
                                class_to_add_start_time:
                            return False
                        break
                    elif class_index == len(self.schedule[day]) - 1:  # if we are at end
                        if class_to_add_start_time <= single_class.end_time:
                            return False
                        break
        return True

    def add_class(self, class_to_add: Section) -> str:

        if class_to_add in self.class_list:
            return class_to_add.section_id + " already present in schedule."

        if not self.no_class_overlap(class_to_add):
            return class_to_add.section_id + " has time conflicts with an existing class."

        if class_to_add.open_seats <= 0:
            self.warnings_list.append(MySchedule.ScheduleWarning([class_to_add], "section full"))

        self.total_credits += class_to_add.course.credits
        for day, class_meetings in class_to_add.class_meetings.items():
            for class_time_to_add in class_meetings:
                if len(self.schedule[day]) == 0:
                    self.schedule[day].append(class_time_to_add)
                else:
                    for class_index in range(len(self.schedule[day])):
                        if self.schedule[day][class_index].start_time > class_time_to_add.start_time:  # add before
                            self.schedule[day].insert(class_index, class_time_to_add)
                            break
                        elif class_index == len(self.schedule[day]) - 1 and \
                                self.schedule[day][class_index].start_time <= class_time_to_add.start_time:
                            #  made it to end of list without adding class yet, so add the class at the end of day
                            self.schedule[day].append(class_time_to_add)
        self.class_list.append(class_to_add)

        return class_to_add.section_id + " added."

    def remove_class(self, class_to_remove: Section) -> str:
        class_to_remove.section_id

        class_previously_in_schedule = False
        for day, meeting_times in self.schedule.items():
            new_day_list = []
            for one_class in meeting_times:
                if one_class.section_id != class_to_remove.section_id:
                    new_day_list.append(one_class)
                else:
                    class_previously_in_schedule = True
            self.schedule[day] = new_day_list

        if class_previously_in_schedule:
            self.class_list.remove(class_to_remove)
            self.total_credits -= class_to_remove.course.credits

            for warning in self.warnings_list:
                if class_to_remove in warning.involved_sections:
                    self.warnings_list.remove(warning)
        else:
            return class_to_remove.section_id + " not in schedule."

        return class_to_remove.section_id + " removed."

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

    class ScheduleWarning(object):
        """
        Warning message to be displayed next to the user's schedule,
        when their schedule has some notable issue.
        """
        # A type hint for involved_sections, which should be list[Section],
        # causes Flask not to start. So it's not there.
        def __init__(self, involved_sections: list, warning_type: str):
            self.involved_sections = involved_sections
            self.warning_type = warning_type

            if warning_type == "section full":
                self.warning_text = \
                    involved_sections[0].section_id + \
                    " has no open seats and must be waitlisted."


class CourseList(object):
    def __init__(self):
        all_courses_list_raw = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/data/fall2020data.json"))
        self.courses = {}  # dictionary mapping course name (string) to a Course object
        for courses in all_courses_list_raw:
            course_id = courses["course_id"]
            course_name = courses["name"]
            course_credits = int(courses["credits"])
            sections = courses["sections"]
            section_dict = {}
            course_obj = Course(course_id, course_name, course_credits, section_dict)

            # populate the sections of the specific course
            for section in sections:
                section_id = section["section_id"]
                section_number = section["number"]
                total_seats = int(section["seats"])
                open_seats = int(section["open_seats"])
                class_meetings = CourseList.make_meeting_dict(section["meetings"], section_id)
                professor = section["instructors"]
                gpa = 3.5
                section_dict[section_number] = \
                    Section(course_id, section_id, total_seats, open_seats, class_meetings, professor, gpa, course_obj)

            self.courses[course_id] = course_obj

    @staticmethod
    def make_meeting_dict(meetings_list: list, section_id: str):
        day_to_meetings = {"M": [],
                           "Tu": [],
                           "W": [],
                           "Th": [],
                           "F": []}
        # a dict of day to times. this is only used to take out the duplicate times that are present in our data
        current_meeting_times = {"M": set(),
                                 "Tu": set(),
                                 "W": set(),
                                 "Th": set(),
                                 "F": set()}
        for meeting in meetings_list:
            days = re.findall('[A-Z][a-z]*', meeting["days"])  # a list of all the days for this meeting time
            for day in days:
                if day == "M" or day == "Tu" or day == "W" or day == "Th" or day == "F":  # ignore weekend classes
                    start_end_tuple = (meeting["start_time"], meeting["end_time"])
                    if start_end_tuple not in current_meeting_times[day]:
                        current_meeting_times[day].add(start_end_tuple)
                        day_to_meetings[day].append(MeetingTime(meeting, section_id))
        return day_to_meetings


class MeetingTime(object):
    def __init__(self, meeting: dict, section_id: str):
        self.room = meeting["room"]
        self.building = meeting["building"]
        self.classtype = meeting["classtype"]
        # these next 2 are used for comparison of time
        self.start_time = datetime.strptime(meeting["start_time"], '%I:%M%p')
        self.end_time = datetime.strptime(meeting["end_time"], '%I:%M%p')
        # these next 2 are used for frontend formatting of time
        self.formatted_start_time = meeting["start_time"]
        self.formatted_end_time = meeting["end_time"]
        self.section_id = section_id
        self.color = None

    def __eq__(self, other):
        if not isinstance(other, MeetingTime):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.start_time == other.start_time \
               and self.end_time == other.end_time \
               and self.section_id == other.section_id

    def __ne__(self, obj):
        return not self == obj

    def __hash__(self):
        return hash(self.section_id)
