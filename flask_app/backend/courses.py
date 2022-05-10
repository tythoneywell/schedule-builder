from typing import Tuple, Union

import requests
import re
from datetime import datetime
from collections import OrderedDict


class Course(object):
    """
    Represents a course as seen on the Schedule of Classes.
    Contains a list of sections, the course code, and credits.
    """

    def __init__(self, course_code: str, name: str, course_credits: int, sections: dict, professor_to_sections: dict,
                 professor_to_avg_course_gpa: dict, avg_gpa: any = 0, gen_eds: list = None):
        self.sess = requests.Session()
        self.course_code = course_code
        self.name = name
        self.credits = course_credits if course_credits else 0
        self.sections = sections
        self.avg_gpa = avg_gpa
        self.gen_eds = gen_eds if gen_eds else []
        # note this will be a dict[string: list] since it is just one professor. In the case of co-taught classes,
        # the same section will appear as part of 2 (or more) lists in this dict
        self.professor_to_sections = professor_to_sections
        self.professor_to_avg_course_gpa = professor_to_avg_course_gpa

    @staticmethod
    def get_professor_average_rating(professor_name: str) -> Union[float, None]:
        """
        Retrieves an average Planetterp rating for a specified professor by the name

        Args:
            professor_name: str
                Name of professor in section whose rating we want to get.
        Returns:
            rating: any (float/none)
                Rating of said professor
        """
        try:
            return APIGet.get_professor_by_name(professor_name).average_rating
        except ConnectionError:
            return None

    def set_sorted_professors_by_rating(self) -> None:
        """
        This function sorts the existing professors to sections object by the rating to display
        the results properly in sorted order.

        Returns:
            None
        """
        self.professor_to_sections = dict(OrderedDict(sorted(self.professor_to_sections.items(),
                                                             key=lambda prof: (
                                                                 Course.get_professor_average_rating(
                                                                     prof[0]) is not None,
                                                                 Course.get_professor_average_rating(prof[0])),
                                                             reverse=True)))


class Professor(object):
    """
    Represents a Professor Object that is so far used when searching for information about a Professor
    """

    def __init__(self, name: str, course_list: list, instructor_type: str, average_rating: float, reviews: list):
        self.name = name
        self.course_list = course_list
        self.instructor_type = instructor_type
        self.average_rating = average_rating
        self.reviews = reviews

    @staticmethod
    def get_all_professors(page_num: int) -> Tuple[list, list, list]:
        """
        Returns a list of professors

        Args:
            page_num: int
                Page number for the professors to retrieve from planetterp API
        Returns:
            (professor_names, professor_slugs, professor_ratings): Tuple(list, list, list)
                Tuple consisting of list of professor names and slugs and ratings for that page number
        """

        page_num_offset = str((int(page_num) - 1) * 100)

        professors_request = requests.get('https://api.planetterp.com/v1/professors?offset=' + page_num_offset,
                                          headers={'Accept': 'application/json'}).json()

        professor_names = [prof["name"] for prof in professors_request]
        professor_slugs = [prof["slug"] for prof in professors_request]
        professor_ratings = [prof["average_rating"] for prof in professors_request]

        return professor_names, professor_slugs, professor_ratings


class Section(object):
    """
    Represents an individual section of a course.
    Contains course code, section id, total and open seats,
    and other information for the schedule builder itself such as color to be displayed.
    """

    def __init__(self, course_code: str, section_id: str, total_seats: int, open_seats: int, class_meetings: dict,
                 professor: list, course: Course, is_synchronous: bool):
        self.sess = requests.Session()
        self.course_code = course_code
        self.section_id = section_id
        self.total_seats = total_seats
        self.open_seats = open_seats
        self.class_meetings = class_meetings
        self.professor_name_list = professor
        self.course = course
        self.is_synchronous = is_synchronous

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

    def __init__(self, meeting: dict, section_id: str, course: Course):
        self.room = meeting["room"]
        self.building = meeting["building"]
        self.classtype = meeting["classtype"]
        # these next 2 are used for comparison of time
        self.start_time = datetime.strptime(meeting["start_time"], '%I:%M%p')
        self.end_time = datetime.strptime(meeting["end_time"], '%I:%M%p')
        # these next 2 are used for frontend formatting of time
        self.formatted_start_time = meeting["start_time"]
        self.formatted_end_time = meeting["end_time"]
        self.course = course
        self.section_id = section_id

    def __eq__(self, other):
        if not isinstance(other, MeetingTime):
            # don't attempt to compare against unrelated types
            return False

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

        Args:
            course_code: str
                String of the course code (e.g. cmsc131)

        Returns:
            course: Course
                Returns a Course object corresponding with the course code string
        """
        return APIGet.get_complete_course_by_course_code(course_code)

    @staticmethod
    def get_courses_using_page_number(page_num: int) -> dict:
        """
        Given a page number, this function will call the API and give back a
        dictionary of course objects in alphabetical order
        in order to display them all on the "see all courses" page
        Each page has 30 courses

        Args:
            page_num: int
                The page number of all courses to load
        Returns:
            courses: dict
                Returns a dictionary of course objects (maximum of 30) to be displayed in the all courses tab
        """
        return APIGet.get_course_list_by_page_number(page_num)

    @staticmethod
    def make_meeting_dict(meetings_list: list, section_id: str, course: Course) -> dict:
        """
        Args:
            meetings_list: list[dict]
                List of dict representations of meeting times to be converted to
                a dict of MeetingTimes.
            section_id: str
                The section_id of the section
            course: Course
                The parent Course of the section
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
                        day_to_meetings[day].append(MeetingTime(meeting, section_id, course))
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
        course_search_return = RequestProxy.planetterp_search_by_query(query)
        course_names = [result["name"] for result in course_search_return if result["type"] == "course"]

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
        out_course.sections, out_course.professor_to_sections = APIGet.get_sections_list_by_course(out_course)
        out_course.professor_to_avg_course_gpa = APIGet.get_professor_gpa_breakdown_by_course(course_code)
        out_course.set_sorted_professors_by_rating()

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
        course_search_return = RequestProxy.planetterp_get_course_by_course_code(course_code)

        return APIParse.planetterp_course_raw_to_course_head(course_search_return)

    @staticmethod
    def get_course_list_by_page_number(page_num: int) -> dict:
        """
        Given a page number, this function will call the API and give back a
        dictionary of course objects in alphabetical order
        in order to display them all on the "see all courses" page
        Each page has 30 courses

        Args:
            page_num: int
                The page number of all courses to load
        Returns:
            courses: dict
                Dictionary of courses in alphabetical order to display in the "all courses" page (max of 30)
        """
        courses_this_page = RequestProxy.planetterp_get_courses_by_page(page_num)

        courses = {}  # dictionary mapping course code (string) to a Course object

        for course_raw in courses_this_page:
            course_obj = APIParse.planetterp_course_raw_to_course_head(course_raw)
            course_obj.sections = APIGet.get_sections_list_by_course(course_obj)[0]
            course_code = course_obj.course_code

            courses[course_code] = course_obj

        return courses

    @staticmethod
    def get_course_list_by_gen_ed(department_id: str, gen_ed: str) -> list:
        """
        Returns a list of all courses within a department that satisfy a single gen ed
        requirement (max 30)

        Args:
            department_id: str
                The department in which to search for courses
            gen_ed: str
                The gen ed requirement to search for
        Returns:
            courses: list
                List of courses satisfying input arguments
        """
        courses_this_page = RequestProxy.umdio_get_courses_by_gened(department_id, gen_ed)

        out_courses = []

        if not courses_this_page:
            return []

        for course_raw in courses_this_page:
            course_obj = APIParse.umd_io_course_raw_to_course_head(course_raw)
            try:
                course_obj.avg_gpa = RequestProxy.planetterp_get_course_by_course_code(
                    course_obj.course_code)["average_gpa"]
            except ConnectionError:
                pass

            out_courses.append(course_obj)

        return out_courses

    @staticmethod
    def get_sections_list_by_course(course: Course) -> Tuple:
        """
        Args:
            course: Course
                Base course to get sections of
        Returns:
            sections: dict[str, Section]
                Sections of this course, from umd.io
            professors: dict[str, Section]
                Professors teaching this course with a list of their sections, from umd.io
        """
        sections_response = RequestProxy.umdio_get_sections_by_course_code(course)

        return APIParse.umd_io_sections_raw_to_section_list(sections_response, course)

    @staticmethod
    def get_professor_gpa_breakdown_by_course(course_code: str) -> dict:
        """
        Args:
            course_code: str
                Course code of class to query grade information
        Returns:
            gpa: dict
                Dictionary of [str:float] of professor to calculated average gpa of specific course when taught by that
                professor
        """
        grade_search_return = RequestProxy.planetterp_get_grades_by_course_code(course_code)

        return APIParse.planetterp_raw_grade_distribution_to_gpa(grade_search_return)

    @staticmethod
    def get_professor_by_name(professor_name: str, get_reviews="false") -> Professor:
        """
        Args:
            professor_name: str
                Professor Name whose object we want to get
            get_reviews: bool
                Boolean representing if API call should return the Professor reviews too
        Returns:
            professor: Professor
                The object of this professor
        """
        prof_search_return = RequestProxy.planetterp_get_professor_by_name(professor_name, get_reviews=get_reviews)

        return APIParse.planetterp_prof_raw_to_prof_head(prof_search_return)


class RequestProxy(object):
    """
    Handles sending requests to the API.
    Can be set to emulate the API in order to complete tests. Set test_mode = True.
    Emulation consists of returning the sample responses
    listed on the respective APIs.
    Returns error sample response when bad_request is set to True.
    """
    test_mode = False
    bad_request = False

    @classmethod
    def planetterp_search_by_query(cls, query: str) -> list:
        """
        Ask planetterp to match query to course names

        Args:
            query: str
                Partial string to search
        Returns:
            matched_courses: list
                List of courses that were matched (from json response)
        """
        if not cls.test_mode:
            return requests.get('https://api.planetterp.com/v1/search',
                                params={'query': query},
                                headers=APIGet.headers).json()

        else:
            return [{"name": "CMSC131", "slug": "CMSC131", "type": "course"}]

    @classmethod
    def planetterp_get_course_by_course_code(cls, course_code: str) -> dict:
        """
        Ask planetterp to search for a course given a specific course code

        Args:
            course_code: str
                Course code string to get
        Returns:
            course: dict
                Course that was found, in dict form (from json response)
        """
        if not cls.test_mode:
            course_search_return = requests.get('https://api.planetterp.com/v1/course',
                                                params={'name': course_code},
                                                headers=APIGet.headers)

            if course_search_return.status_code != 200:
                raise ConnectionError("Course Code Not Found")

            return course_search_return.json()

        else:
            if not cls.bad_request:
                return {
                    "department": "MATH",
                    "course_number": "140",
                    "title": "Calculus I",
                    "description": "Introduction to calculus, including functions, limits, continuity, "
                                   "derivatives and applications of the derivative, sketching of graphs of "
                                   "functions, definite and indefinite integrals, and calculation of area. "
                                   "The course is especially recommended "
                                   "for science, engineering and mathematics majors.",
                    "credits": 3,
                    "professors": [
                        [
                            "Jon Snow",
                            "Tyrion Lannister"
                        ]
                    ],
                    "average_gpa": 3.17244
                }

            else:
                raise ConnectionError("Course Code Not Found")

    @classmethod
    def planetterp_get_courses_by_page(cls, page_num: int) -> list:
        """
        Ask planetterp to get a page from the list of all courses

        Args:
            page_num: str
                Page number to get
        Returns:
            courses: list
                List of course on this page (from json response)
        """
        if not cls.test_mode:
            return requests.get("https://api.planetterp.com/v1/courses", params={
                "limit": 30,
                "offset": page_num
            }, headers=APIGet.headers).json()

        else:
            if not cls.bad_request:
                return [{
                    "department": "MATH",
                    "course_number": "140",
                    "title": "Calculus I",
                    "description": "Introduction to calculus, including functions, limits, continuity, derivatives "
                                   "and applications of the derivative, sketching of graphs of functions, "
                                   "definite and indefinite integrals, and calculation of area. The course is "
                                   "especially recommended"
                                   "for science, engineering and mathematics majors.",
                    "credits": 3,
                    "professors": [
                        [
                            "Jon Snow",
                            "Tyrion Lannister"
                        ]
                    ],
                    "average_gpa": 3.17244
                }]
            else:
                return []

    @classmethod
    def umdio_get_sections_by_course_code(cls, course: Course) -> list:
        """
        Ask umd.io to get a list of sections from a course code

        Args:
            course: str
                Course whose course code will be used for search
        Returns:
            sections: list
                List of sections for the course (from json response)
        """
        if not cls.test_mode:
            sections_response = requests.get("https://api.umd.io/v1/courses/" + course.course_code + "/sections",
                                             params={},
                                             headers=APIGet.headers)

            # Not all courses have sections
            if sections_response.status_code != 200:
                return []

            return sections_response.json()

        else:
            if not cls.bad_request:
                return [{
                    "course": "ENGL101",
                    "section_id": "ENGL101-0101",
                    "semester": 201501,
                    "number": 0,
                    "seats": 0,
                    "meetings": [
                        {
                            "days": "MWF",
                            "room": "string",
                            "building": "string",
                            "classtype": "string",
                            "start_time": "9:00AM",
                            "end_time": "10:00AM"
                        }
                    ],
                    "open_seats": 0,
                    "waitlist": 0,
                    "instructors": [
                        "string"
                    ]
                }]

            else:
                return []

    @classmethod
    def umdio_get_courses_by_gened(cls, department_id: str, gen_ed: str) -> list:
        """
        Ask umd.io to get a list of courses with a specific gen-ed requirement

        Args:
            department_id: str
                Department ID to match (i.e. CMSC)
            gen_ed: str
                Gened requirement to search for
        Returns:
            courses: list
                List of courses satisfying the gened (from json response)
        """
        if not cls.test_mode:
            if department_id == "":
                sections_response = requests.get("https://api.umd.io/v1/courses",
                                                 params={"gen_ed": gen_ed},
                                                 headers=APIGet.headers)
            else:
                sections_response = requests.get("https://api.umd.io/v1/courses",
                                                 params={"dept_id": department_id,
                                                         "gen_ed": gen_ed},
                                                 headers=APIGet.headers)

            # No courses found
            if sections_response.status_code != 200:
                return []

            return sections_response.json()

        else:
            if not cls.bad_request:
                return [{
                    "course_id": "MATH140",
                    "semester": 202001,
                    "name": "Calculus I",
                    "dept_id": "MATH",
                    "department": "Mathematics",
                    "credits": "4",
                    "description": "Introduction to calculus, including functions, limits, continuity, "
                                   "derivatives and applications of the derivative, sketching of graphs "
                                   "of functions, definite and indefinite integrals, and calculation "
                                   "of area. The course is especially recommended for science, "
                                   "engineering and mathematics majors.",
                    "grading_method": [
                        "Regular",
                        "Pass-Fail",
                        "Audit"
                    ],
                    "gen_ed": [
                        [
                            "FSAR",
                            "FSMA"
                        ]
                    ],
                    "core": [
                        "MS"
                    ],
                    "relationships": {
                        "coreqs": None,
                        "prereqs": "Minimum grade of C- in MATH115.",
                        "formerly": None,
                        "restrictions": None,
                        "additional_info": "Or must have math eligibility of MATH140 or higher; "
                                           "and math eligibility is based on the Math Placement "
                                           "Test.  All sections will require the use of a TI "
                                           "graphics calculator. Instructor will use a TI-83, "
                                           "TI-83+, or TI-86 calculator. If purchasing used "
                                           "books additional software may be required.",
                        "also_offered_as": None,
                        "credit_granted_for": "MATH120, MATH130, MATH136, MATH140 or MATH220."
                    },
                    "sections": [
                        "MATH140-0111",
                        "MATH140-0121",
                        "MATH140-0131",
                        "MATH140-0141",
                        "MATH140-0211",
                        "MATH140-0221",
                        "MATH140-0231",
                        "MATH140-0241",
                        "MATH140-0311",
                        "MATH140-0321",
                        "MATH140-0112",
                        "MATH140-0113",
                        "MATH140-0122",
                        "MATH140-0123",
                        "MATH140-0132",
                        "MATH140-0142"
                    ]
                }]
            else:
                return []

    @classmethod
    def planetterp_get_grades_by_course_code(cls, course_code: str) -> list:
        """
        Ask planetterp to get grades for a course

        Args:
            course_code: str
                Course code to get grades for
        Returns:
            grades: list
                List of letter grades for this course (from json response)
        """
        if not cls.test_mode:
            grade_search_return = requests.get('https://api.planetterp.com/v1/grades', params={
                'course': course_code
            }, headers=APIGet.headers)

            if grade_search_return.status_code != 200:
                raise ConnectionError("Error retrieving gpa information from course")

            return grade_search_return.json()

        else:
            if not cls.bad_request:
                return [{
                    "course": "MATH140",
                    "professor": "Jon Snow",
                    "semester": "202001",
                    "section": "0101",
                    "A+": 1,
                    "A": 1,
                    "A-": 1,
                    "B+": 1,
                    "B": 1,
                    "B-": 1,
                    "C+": 1,
                    "C": 1,
                    "C-": 1,
                    "D+": 1,
                    "D": 1,
                    "D-": 1,
                    "F": 1,
                    "W": 1,
                    "Other": 1
                }]

            else:
                raise ConnectionError("Error retrieving gpa information from course")

    @classmethod
    def planetterp_get_professor_by_name(cls, professor_name: str, get_reviews="false") -> dict:
        """
        Ask planetterp for information on a professor

        Args:
            professor_name: str
                Professor Name whose object we want to get
            get_reviews: bool
                Boolean representing if API call should also return Professor reviews
        Returns:
            prof_raw: a json dict with professor information
        """
        if not cls.test_mode:
            course_search_return = requests.get('https://api.planetterp.com/v1/professor', params={
                'name': professor_name,
                'reviews': get_reviews
            }, headers=APIGet.headers)

            if course_search_return.status_code != 200:
                raise ConnectionError("Professor Not Found")

            prof_raw = course_search_return.json()
            return prof_raw
        else:
            if not cls.bad_request:
                return {
                    "name": "Jon Snow",
                    "slug": "snow",
                    "type": "professor",
                    "courses": [
                        "MATH140"
                    ],
                    "average_rating": 4.125
                }
            else:
                raise ConnectionError("Professor Not Found")


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
        TODO Add unit test
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
        gen_eds = course_raw["gen_ed"][0]
        section_dict = {}
        professor_to_sections = {}
        professor_to_avg_course_gpa = {}

        out_course = Course(course_id, course_name, course_credits, section_dict, professor_to_sections,
                            professor_to_avg_course_gpa, gen_eds=gen_eds)

        return out_course

    @staticmethod
    def umd_io_sections_raw_to_section_list(sections_raw: list, parent_course: Course) \
            -> Tuple[dict, dict]:
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
            class_meetings = CourseList.make_meeting_dict(section["meetings"], section_id, parent_course)
            is_synchronous = False
            for meeting in class_meetings.values():
                if len(meeting) != 0:
                    is_synchronous = True
            professors = section["instructors"]
            section_to_add = Section(
                parent_course.course_code, section_id, total_seats, open_seats, class_meetings, professors,
                parent_course, is_synchronous)
            # set the initial value to an empty list of sections
            for professor in professors:
                professor_to_sections_dict.setdefault(professor, [])
                professor_to_sections_dict[professor].append(section_to_add)
            section_dict[section_number] = section_to_add

        return section_dict, professor_to_sections_dict

    @staticmethod
    def planetterp_raw_grade_distribution_to_gpa(grades_raw: list) -> dict:
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

    @staticmethod
    def planetterp_prof_raw_to_prof_head(prof_raw: dict) -> Professor:
        """
        Makes a response from planetterp's professor get into a course (with no sections)

        Args:
            prof_raw: dict[str, str]
                The raw response of the planetterp API (converted from json to dict)
        Returns:
            professor: Professor
                Professor object generated from the raw dict. No reviews (yet).
        """
        prof_type = prof_raw["type"]
        prof_name = prof_raw["name"]
        course_list = prof_raw["courses"]
        average_rating = prof_raw["average_rating"]

        if "reviews" in prof_raw.keys():
            reviews = prof_raw["reviews"]

            for review in reviews:
                del review["professor"]
                del review["created"]

        else:
            reviews = None

        out_prof = Professor(prof_name, course_list, prof_type, average_rating, reviews)

        return out_prof
