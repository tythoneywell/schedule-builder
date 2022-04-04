import requests


class MyClass(object):
    def __init__(self, course_code, time, professor, gpa):
        self.sess = requests.Session()
        self.course_code = course_code
        self.time = time
        self.professor = professor
        self.gpa = gpa