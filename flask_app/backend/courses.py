import requests
import os
import json
import re
from datetime import datetime


class Course(object):
    """
    Represents a course as seen on the Schedule of Classes.
    Contains a list of sections, the course code, and credits.
    """
    def __init__(self, course_code: str, name: str, course_credits: int, sections: dict):
        self.sess = requests.Session()
        self.course_code = course_code
        self.name = name
        self.credits = course_credits
        self.sections = sections


class Section(object):
    """
    Represents an individual section of a course.
    Contains course code, section id, total and open seats,
    and other information for the schedule builder itself such as color to be displayed.
    """
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
        """
        Args:
            color: str
                Color to set this section as.
        """
        self.color = color
        for day, classes in self.class_meetings.items():
            for meeting_time in classes:
                meeting_time.color = color

    # Specifying the type contents of a dict type hint crashes Flask.
    def get_formatted_weekly_schedule(self) -> dict:
        """
        Returns:
            weekly_schedule: dict[str, str]
                Dict of nicely formatted section info to be used on the course list.
                Keys are strings of format "9AM-10:15AM", etc.
                Values are strings of format "MWF", "TuTh", etc.
        """
        time_per_day = {}
        for day, meeting_time_list in self.class_meetings.items():
            if len(meeting_time_list) > 0:
                for meeting_time in set(meeting_time_list):
                    temp = meeting_time.formatted_start_time + "-" + meeting_time.formatted_end_time
                    if temp in time_per_day:
                        time_per_day[temp] = time_per_day[temp] + day + ""
                    else:
                        time_per_day[temp] = day

        return time_per_day


class MeetingTime(object):
    """
    Class representing a single time-slot of a section.
    Contains time, location, and section id.
    """
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


class CourseList(object):
    """
    Class containing a list of all courses available to add.
    """
    def __init__(self):
        all_courses_list_raw = json.load(open(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/fall2020data.json"))
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
    def make_meeting_dict(meetings_list: list, section_id: str) -> dict:
        """
        Args:
            meetings_list: list[dict]
                List of dict representations of meeting times to be converted to
                a dict of MeetingTimes.
            section_id: str
                The section_id of the section
        Returns:
            weekly_schedule:
                Dict mapping day of the week "M", "Tu", etc
                to a list of MeetingTime objects (in order).
        """
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
