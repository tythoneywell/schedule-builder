from flask_app.backend.courses import Course, Section, CourseList


class MySchedule(object):
    """
    Representation of the user's schedule.
    Contains a list of sections, the number of credits, meeting times for each day,
    and any important warnings about the schedule.
    """
    colors = ["red", "blue", "green", "purple", "orange", "magenta"]

    def __init__(self):
        #  dictionary of day of week to MeetingTime
        self.schedule = {"M": [],
                         "Tu": [],
                         "W": [],
                         "Th": [],
                         "F": []}
        self.total_credits = 0
        self.courses_list = []
        self.sections_list = []

        self.warnings_list = []

    def check_section_no_time_conflicts(self, class_to_add: Section) -> bool:
        """
        Args:
            class_to_add: Section
                Section to test for overlap with existing times.
        Returns:
            can_add: bool
                Whether the class can be added.
        """
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
                                class_to_add_start_time:  # class right in front of one we want to add overlaps
                            return False
                        break
                    elif class_index == len(self.schedule[day]) - 1:  # if we are at end
                        if class_to_add_start_time <= single_class.end_time:
                            return False
                        break
        return True

    def add_course(self, course_to_add: Course) -> str:
        """
        Args:
            course_to_add: Course
                Course to try to add.
        Returns:
            message: bool
                String describing the result of trying to add the course.
        """

        for other_course in self.courses_list:
            if course_to_add.course_code == other_course.course_code:
                return course_to_add.course_code + " already present in schedule."

        self.total_credits += course_to_add.credits
        self.courses_list.append(course_to_add)

        return course_to_add.course_code + " added."

    def remove_course(self, course_to_remove: Course) -> str:
        """
        Args:
            course_to_remove: Course
                Course to try to remove.
        Returns:
            message: bool
                String describing the result of trying to remove the course.
        """

        for course in self.courses_list:
            if course.course_code == course_to_remove.course_code:
                self.courses_list.remove(course)

                self.total_credits -= course_to_remove.credits

                for warning in self.warnings_list:
                    if course_to_remove in warning.involved_sections:
                        self.warnings_list.remove(warning)

                return course_to_remove.course_code + " removed."

        return course_to_remove.course_code + " not in schedule."

    def add_section(self, section_to_add: Section) -> str:
        """
        Args:
            section_to_add: Section
                Section to try to add.
        Returns:
            message: bool
                String describing the result of trying to add the section.
        """

        for section_obj in self.sections_list:
            if section_to_add.section_id == section_obj.section_id:
                return section_to_add.section_id + " already present in schedule."

        if not self.check_section_no_time_conflicts(section_to_add):
            return section_to_add.section_id + " has time conflicts with an existing class."

        if section_to_add.open_seats <= 0:
            self.warnings_list.append(MySchedule.ScheduleWarning([section_to_add], "section full"))

        for day, class_meetings in section_to_add.class_meetings.items():
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
        self.sections_list.append(section_to_add)

        # If the course wasn't already in the course list, add it now.
        self.add_course(section_to_add.course)
        return section_to_add.section_id + " added."

    def remove_section(self, section_to_remove: Section) -> str:
        """
        Args:
            section_to_remove: Section
                Section to try to remove.
        Returns:
            message: bool
                String describing the result of trying to remove the section.
        """

        class_previously_in_schedule = False
        for day, meeting_times in self.schedule.items():
            new_day_list = []
            for one_class in meeting_times:
                if one_class.section_id != section_to_remove.section_id:
                    new_day_list.append(one_class)
                else:
                    class_previously_in_schedule = True
            self.schedule[day] = new_day_list

        if class_previously_in_schedule:
            for index in range(len(self.sections_list)):
                section_obj = self.sections_list[index]
                if section_obj.section_id == section_to_remove.section_id:
                    self.sections_list.pop(index)
                    break

            for warning in self.warnings_list:
                if section_to_remove in warning.involved_sections:
                    self.warnings_list.remove(warning)
        else:
            return section_to_remove.section_id + " not in schedule."

        return section_to_remove.section_id + " removed."

    def add_registered_course_section_by_id(self, section_id: str) -> str:
        """
        TODO Add unit test

        Args:
            section_id: str
                Section ID to try to add, from an already registered course.
        Returns:
            message: bool
                String describing the result of trying to add the section.
        """

        for course in self.courses_list:
            for section in course.sections.values():
                if section.section_id == section_id:
                    return self.add_section(section)

        return "Could not find section to add from registered courses"

    def remove_registered_course_section_by_id(self, section_to_remove: Section) -> str:
        """
        TODO Add unit test

        Args:
            section_to_remove: Section
                Section to try to remove.
        Returns:
            message: bool
                String describing the result of trying to remove the section.
        """

        class_previously_in_schedule = False
        for day, meeting_times in self.schedule.items():
            new_day_list = []
            for one_class in meeting_times:
                if one_class.section_id != section_to_remove.section_id:
                    new_day_list.append(one_class)
                else:
                    class_previously_in_schedule = True
            self.schedule[day] = new_day_list

        if class_previously_in_schedule:
            for index in range(len(self.sections_list)):
                section_obj = self.sections_list[index]
                if section_obj.section_id == section_to_remove.section_id:
                    self.sections_list.pop(index)
                    break

            for warning in self.warnings_list:
                if section_to_remove in warning.involved_sections:
                    self.warnings_list.remove(warning)
        else:
            return section_to_remove.section_id + " not in schedule."

        return section_to_remove.section_id + " removed."

    def remove_all_classes(self) -> None:
        """
        Resets the schedule to be empty.
        TODO Fix for new course/section addition procedure
        """
        self.schedule = {"M": [],
                         "Tu": [],
                         "W": [],
                         "Th": [],
                         "F": []}
        self.total_credits = 0
        self.sections_list = []

        self.warnings_list = []

    def get_schedule_average_gpa(self) -> float:
        """
        Calculates average GPA of the current schedule
        """
        gpa_sum = 0.0
        for schedule_class in self.sections_list:
            gpa_sum += schedule_class.course.avg_gpa * schedule_class.course.credits
        if len(self.sections_list) == 0 or self.total_credits == 0:
            # by default return 0 to avoid errors
            return 0.0
        return gpa_sum / self.total_credits

    def get_serialized_schedule(self) -> str:
        """
        This function serializes the user's schedule to easily be copied by the user on the frontend. The user can
        then use this serialized string to load their schedule through the "load_serialized_schedule" function.

        return:
            str_schedule: str
                A String representation of the user's schedule
        """
        str_schedule = ""
        if len(self.sections_list) == 0:
            return ""
        for section in self.sections_list:
            str_schedule += section.section_id + ","
        str_schedule = str_schedule.rstrip(str_schedule[-1])  # strip trailing comma at end of list
        return str_schedule

    def load_serialized_schedule(self, str_schedule: str) -> None:
        """
        This function takes a string representation of the serialized version of a user's schedule and loads this
        schedule by adding all of the sections/meeting times.

        param:
            str_schedule: str
                A String representation of the user's schedule generated from the get_serialized_schedule function
        """
        if len(str_schedule.strip()) == 0:  # if given empty schedule, just return
            return
        section_arr = str_schedule.split(",")
        for section in section_arr:
            #  if there is no - in the string, this is not a valid section to add to schedule
            if section.find('-') < 0:
                self.warnings_list.append(MySchedule.ScheduleWarning([section], "invalid format"))
                continue
            course_code_without_section = section.split("-")[0]
            course_section_number = section.split("-")[1]
            try:
                course_to_extract_section_from = CourseList.get_course_using_course_code(course_code_without_section)
                self.add_section(course_to_extract_section_from.sections[course_section_number])
            except ConnectionError:
                self.warnings_list.append(MySchedule.ScheduleWarning([course_code_without_section],
                                                                     "course does not exist"))
            except KeyError:
                self.warnings_list.append(MySchedule.ScheduleWarning([course_code_without_section,
                                                                      course_section_number],
                                                                     "section number does not exist"))

    def get_course_color(self, course: Course):
        """
        Returns the color of a course in the schedule

        Args:
            course: Course
                Course to get the color of
        Returns:
            color: str
                Color of the course (in string form)
        """
        try:
            return self.colors[self.courses_list.index(course)]
        except (IndexError, ValueError):
            return "black"

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
            elif warning_type == "course does not exist":
                self.warning_text = involved_sections[0] + " is not a valid course code"
            elif warning_type == "section number does not exist":
                self.warning_text = involved_sections[1] + " is not a valid section number for " + involved_sections[0]
            elif warning_type == "invalid format":
                self.warning_text = involved_sections[0] + " is not a valid format of <course>-<section>"
