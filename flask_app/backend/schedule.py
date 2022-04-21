from flask_app.backend.courses import Section


class MySchedule(object):
    """
    Representation of the user's schedule.
    Contains a list of sections, the number of credits, meeting times for each day,
    and any important warnings about the schedule.
    """

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

    def no_class_overlap(self, class_to_add: Section) -> bool:
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

    def add_class(self, class_to_add: Section) -> str:
        """
        Args:
            class_to_add: Section
                Section to try to add.
        Returns:
            message: bool
                String describing the result of trying to add the class.
        """

        for section_obj in self.class_list:
            if class_to_add.section_id == section_obj.section_id:
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
        """
        Args:
            class_to_remove: Section
                Section to try to add.
        Returns:
            message: bool
                String describing the result of trying to remove the class.
        """

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
            for index in range(len(self.class_list)):
                section_obj = self.class_list[index]
                if section_obj.section_id == class_to_remove.section_id:
                    self.class_list.pop(index)
                    break

            self.total_credits -= class_to_remove.course.credits

            for warning in self.warnings_list:
                if class_to_remove in warning.involved_sections:
                    self.warnings_list.remove(warning)
        else:
            return class_to_remove.section_id + " not in schedule."

        return class_to_remove.section_id + " removed."

    def remove_all_classes(self) -> None:
        """
        Resets the schedule to be empty.
        """
        self.schedule = {"M": [],
                         "Tu": [],
                         "W": [],
                         "Th": [],
                         "F": []}
        self.total_credits = 0
        self.class_list = []

        self.warnings_list = []

    def get_schedule_average_gpa(self) -> float:
        """
        Calculates average GPA of the current schedule
        """
        gpa_sum = 0.0
        for schedule_class in self.class_list:
            gpa_sum += schedule_class.course.avg_gpa * schedule_class.course.credits
        if len(self.class_list) == 0 or self.total_credits == 0:
            # by default return 0 to avoid errors
            return 0.0
        return gpa_sum / self.total_credits

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

