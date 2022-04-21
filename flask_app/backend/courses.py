import requests
import re
from datetime import datetime

from typing import Tuple


class Course(object):
    """
    Represents a course as seen on the Schedule of Classes.
    Contains a list of sections, the course code, and credits.
    """

    def __init__(self, course_code: str, name: str, course_credits: int, sections: dict, professor_to_sections: dict,
                 professor_to_avg_course_gpa: dict, avg_gpa: float = 0):
        self.sess = requests.Session()
        self.course_code = course_code
        self.name = name
        self.credits = course_credits
        self.sections = sections
        self.avg_gpa = avg_gpa
        # note this will be a dict[string: list] since it is just one professor. In the case of co-taught classes,
        # the same section will appear as part of 2 (or more) lists in this dict
        self.professor_to_sections = professor_to_sections
        self.professor_to_avg_course_gpa = professor_to_avg_course_gpa


class Section(object):
    """
    Represents an individual section of a course.
    Contains course code, section id, total and open seats,
    and other information for the schedule builder itself such as color to be displayed.
    """

    def __init__(self, course_code: str, section_id: str, total_seats: int, open_seats: int, class_meetings: dict,
                 professor: list, course: Course):
        self.color = None
        self.sess = requests.Session()
        self.course_code = course_code
        self.section_id = section_id
        self.total_seats = total_seats
        self.open_seats = open_seats
        self.class_meetings = class_meetings
        self.professor = professor
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

    @staticmethod
    def get_course_using_course_code(course_code: str) -> Course:
        """
        Given a course code (e.g. CMSC131)
        this function will call the umd.io API and give back a Course object
        This function will raise an exception if the course code or sections information
        cannot be found on the API (status code from response is not 200)
        """
        return APIGet.get_complete_course_by_course_code(course_code)

    @staticmethod
    def get_courses_using_page_number(page_num: int) -> dict:
        """
        Given a page number, this function will call the API and give back a
        dictionary of course objects in alphabetical order
        in order to display them all on the "see all courses" page
        Each page has 30 courses
        """
        return APIGet.get_course_list_by_page_number(page_num)

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


class APIGet(object):
    """
    Static class which handles API calls to retrieve course/section info.
    """
    headers = {'Accept': 'application/json'}

    @staticmethod
    def get_course_heads_by_query(query: str) -> list:
        """
        Gets a list of courses (without sections) that match a given query.
        To be used when searching for a course to be added to schedule.
        Args:
            query: str
                 Search string to search on planetterp
        Returns:
            found_courses: list[Course]
                List of courses that were found by this search,
                without sections. (Course "heads")
        """
        query = query.upper()
        course_search_return = requests.get('https://api.planetterp.com/v1/search', params={
            'query': query
        }, headers=APIGet.headers)
        course_names = [result["name"] for result in course_search_return.json() if result["type"] == "course"]

        course_heads = []
        for course_name in course_names:
            course_heads += [APIGet.get_course_head_by_course_code(course_name)]

        return course_heads

    @staticmethod
    def get_complete_course_by_course_code(course_code: str) -> Course:
        """
        Gets a complete course (with sections) given its course code.
        To be used when adding a course to the schedule.
        Args:
            course_code: str
                Course code of the course to be gotten.
        Returns:
            course: Course
                Course returned by combined responses of
                planetterp and umd.io APIs
        """
        out_course = APIGet.get_course_head_by_course_code(course_code)
        out_course.sections, out_course.professors_to_sections = APIGet.get_sections_list_by_course(out_course)
        out_course.professor_to_avg_course_gpa = APIGet.get_professor_gpa_breakdown_by_course(course_code)

        return out_course

    @staticmethod
    def get_course_head_by_course_code(course_code: str) -> Course:
        """
        Gets a course "head" (without sections) given its course code.
        Helper method of get_course_heads_by_query and get_complete_course_by_course_code.
        Args:
            course_code: str
                Course code of the course to be gotten.
        Returns:
            course: Course
                Course returned by planetterp API, without sections.
                Will have rating info, etc.
        """
        course_search_return = requests.get('https://api.planetterp.com/v1/course', params={
            'name': course_code
        }, headers=APIGet.headers)

        if course_search_return.status_code != 200:
            raise Exception("Course Code Not Found")

        return APIParse.planetterp_course_raw_to_course_head(course_search_return.json())

    @staticmethod
    def get_course_list_by_page_number(page_num: int) -> dict:
        """
        Given a page number, this function will call the API and give back a
        dictionary of course objects in alphabetical order
        in order to display them all on the "see all courses" page
        Each page has 30 courses
        """
        courses_this_page_raw = requests.get("https://api.planetterp.com/v1/courses", params={
            "limit": 30,
            "offset": page_num
        }, headers=APIGet.headers)

        courses = {}  # dictionary mapping course code (string) to a Course object

        for course_raw in courses_this_page_raw.json():
            course_obj = APIParse.planetterp_course_raw_to_course_head(course_raw)
            course_obj.sections = APIGet.get_sections_list_by_course(course_obj)[0]
            course_code = course_obj.course_code

            courses[course_code] = course_obj

        return courses

    @staticmethod
    def get_sections_list_by_course(course: Course) -> Tuple[dict, dict]:
        """
        Params:
            course: Course
                Base course to get sections of
        Returns:
            sections: dict[str, Section]
                Sections of this course, from umd.io
            professors: dict[str, Section]
                Professors teaching this course with a list of their sections, from umd.io
        """
        sections_response = requests.get("https://api.umd.io/v1/courses/" + course.course_code + "/sections",
                                         headers=APIGet.headers)

        # Not all courses have available sections
        if sections_response.status_code == 200:
            return APIParse.umd_io_sections_raw_to_section_list(sections_response.json(), course)

        else:
            return {}, {}

    @staticmethod
    def get_professor_gpa_breakdown_by_course(course_code: str) -> dict:
        """
        Params:
            course_code: str
                Course code of class to query grade information
        Returns:
            gpa: dict
                Dictionary of [str:float] of professor to calculated average gpa of specific course when taught by that
                professor
        """
        course_search_return = requests.get('https://api.planetterp.com/v1/grades', params={
            'course': course_code
        }, headers=APIGet.headers)

        if course_search_return.status_code != 200:
            raise Exception("Error retrieving gpa information from course")
        return APIParse.planetterp_raw_grade_distribution_to_gpa(course_search_return.json())


class APIParse(object):
    """
    Static class which parses API responses.
    Extract their contents using .json() before calling this class.
    """

    @staticmethod
    def planetterp_course_raw_to_course_head(course_raw: dict) -> Course:
        """
        Makes a response from planetterp's course get into a course (with no sections)
        Args:
            course_raw: dict[str, str]
                The raw response of the planetterp API (converted from json to dict)
        Returns:
            course: Course
                Course object generated from the raw dict. No sections.
        """
        course_code = course_raw["department"] + course_raw["course_number"]
        course_name = course_raw["title"]
        course_credits = course_raw["credits"]
        average_gpa = course_raw["average_gpa"]
        section_dict = {}
        professor_to_sections = {}
        professor_to_avg_course_gpa = {}

        out_course = Course(course_code, course_name, course_credits, section_dict, professor_to_sections,
                            professor_to_avg_course_gpa, average_gpa)

        return out_course

    @staticmethod
    def umd_io_course_raw_to_course_head(course_raw: dict) -> Course:
        """
        Makes a response from umd.io's course get into a course (with no sections)
        Args:
            course_raw: dict[str, str]
                The raw response of the umd.io API (converted from json to dict)
        Returns:
            course: Course
                Course object generated from the raw dict. No sections.
        """
        course_id = course_raw["course_id"]
        course_name = course_raw["name"]
        course_credits = int(course_raw["credits"])
        section_dict = {}
        professor_to_sections = {}
        professor_to_avg_course_gpa = {}

        out_course = Course(course_id, course_name, course_credits, section_dict, professor_to_sections,
                            professor_to_avg_course_gpa)

        return out_course

    @staticmethod
    def umd_io_sections_raw_to_section_list(sections_raw: list, parent_course: Course) -> Tuple[dict, dict]:
        """
        Makes a response from umd.io's sections get into a list of sections
        Args:
            sections_raw: dict[str, str]
                The raw response of the umd.io API (converted from json to dict)
            parent_course: Course
                Course these sections are sections of
        Returns:
            sections: dict[str, Section]
                Dict of Section objects generated from the raw dict.
        """
        section_dict = {}
        professor_to_sections_dict = {}

        for section in sections_raw:
            section_id = section["section_id"]
            section_number = section["number"]
            total_seats = int(section["seats"])
            open_seats = int(section["open_seats"])
            class_meetings = CourseList.make_meeting_dict(section["meetings"], section_id)
            professors = section["instructors"]
            section_to_add = Section(
                parent_course.course_code, section_id, total_seats, open_seats, class_meetings, professors,
                parent_course)
            # set the initial value to an empty list of sections
            for professor in professors:
                professor_to_sections_dict.setdefault(professor, [])
                professor_to_sections_dict[professor].append(section_to_add)
            section_dict[section_number] = section_to_add

        return section_dict, professor_to_sections_dict

    @staticmethod
    def planetterp_raw_grade_distribution_to_gpa(grades_raw) -> dict:
        """
        Makes a response from planetterps's grades get into a gpa float
        Args:
            grades_raw: dict[str, str]
                The raw response of the planetterp API (converted from json to dict)
        Returns:
            gpa: dict
                Dictionary of [string: float] representing Professor to the calculated average GPA of the course
                taught by that specific professor
        """
        professor_to_course_gpa = {}
        professor_to_quality_points = {}
        professor_to_total_grade_entries = {}

        # W's are counted as 0.0, "other" is excluded in gpa calculation
        for semester_grade in grades_raw:
            professor = semester_grade["professor"]
            professor_to_quality_points.setdefault(professor, 0.0)
            professor_to_total_grade_entries.setdefault(professor, 0)

            professor_to_quality_points[professor] += 4 * (semester_grade["A+"] + semester_grade["A"])
            professor_to_total_grade_entries[professor] += semester_grade["A+"] + semester_grade["A"]

            professor_to_quality_points[professor] += 3.7 * semester_grade["A-"]
            professor_to_total_grade_entries[professor] += semester_grade["A-"]

            professor_to_quality_points[professor] += 3.3 * semester_grade["B+"]
            professor_to_total_grade_entries[professor] += semester_grade["B+"]

            professor_to_quality_points[professor] += 3 * semester_grade["B"]
            professor_to_total_grade_entries[professor] += semester_grade["B"]

            professor_to_quality_points[professor] += 2.7 * semester_grade["B-"]
            professor_to_total_grade_entries[professor] += semester_grade["B-"]

            professor_to_quality_points[professor] += 2.3 * semester_grade["C+"]
            professor_to_total_grade_entries[professor] += semester_grade["C+"]

            professor_to_quality_points[professor] += 2 * semester_grade["C"]
            professor_to_total_grade_entries[professor] += semester_grade["C"]

            professor_to_quality_points[professor] += 1.7 * semester_grade["C-"]
            professor_to_total_grade_entries[professor] += semester_grade["C-"]

            professor_to_quality_points[professor] += 1.3 * semester_grade["D+"]
            professor_to_total_grade_entries[professor] += semester_grade["D+"]

            professor_to_quality_points[professor] += 1 * semester_grade["D"]
            professor_to_total_grade_entries[professor] += semester_grade["D"]

            professor_to_quality_points[professor] += .7 * semester_grade["D-"]
            professor_to_total_grade_entries[professor] += semester_grade["D-"]

            professor_to_total_grade_entries[professor] += semester_grade["F"]

            professor_to_total_grade_entries[professor] += semester_grade["W"]

        for professor, quality_points in professor_to_quality_points.items():
            professor_to_course_gpa[professor] = quality_points / professor_to_total_grade_entries[professor]

        return professor_to_course_gpa
