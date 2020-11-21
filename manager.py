import logging

import utils.websis as websis
import utils.notifications as notify
import auth as auth
from student import Student

log = logging.getLogger("AutoRegistration.sub")

class Manager:
    def __init__(self):
        # * Only one user is required to check any given course we use a master user for reliability
        self.master = Student(auth.username, auth.password)
        self.__master_sess = websis.LoginToWebsis(self.master)[1]
        self.__students = dict()  # {uname: Student}

    def getMasterSess(self):
        return self.__master_sess

    def CheckCourseAvailability(self):
        # Aggregate Course Requests
        course_cache = dict()
        # ? Should be sorted by the order they were added in
        for student in self.__students.values():
            for TERM_IN, SUBJECT, COURSE_ID, CRN in student.getNeededCourses().copy():
                course = (TERM_IN, SUBJECT, COURSE_ID)
                if course not in course_cache:
                    course_cache[course] = websis.get_options_for(websis.LoginToWebsis(self.master)[1], TERM_IN, SUBJECT, COURSE_ID)
                    log.info(f"Checking {TERM_IN} {SUBJECT} {COURSE_ID} for availabilities")
                if course_cache[course].get(CRN, 0) > 0:
                    # If their password is not None
                    if student.getLoginInfo()[1] != None:
                        student.registerFor(
                            TERM_IN, SUBJECT, COURSE_ID, CRN)
                        if (len(student.getNeededCourses()) == 0):
                            self.RemoveStudent(student.username)
                    else:
                        notify.notifyStudent(
                            student.username, TERM_IN, SUBJECT, COURSE_ID, CRN, 2)
                    if student.attempts[(TERM_IN, SUBJECT, COURSE_ID, CRN)] < 3:
                        student.attempts[(TERM_IN, SUBJECT, COURSE_ID, CRN)] += 1 
                    else: 
                        self.RemoveCourseSubscribtion(TERM_IN, SUBJECT, COURSE_ID, CRN, student.username)
    def AddCourseSubscribtion(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str, username: str):
        self.__students[username].addNeededCourse(
            TERM_IN, SUBJECT, COURSE_ID, CRN)

    def RemoveCourseSubscribtion(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str, username: str, fufilled=True):
        self.__students[username].removeNeededCourse(
            TERM_IN, SUBJECT, COURSE_ID, CRN)

    def AddStudent(self, student: Student):
        self.__students[student.getLoginInfo()[0]] = student

    def RemoveStudent(self, username: str):
        if (self.hasInfoFor(username)):
            if (len(self.__students[username].getNeededCourses()) != 0):
                log.warning(
                    f"{username} was removed from the registry with {len(self.__students[username].getNeededCourses())} courses unfufilled")
                courses_left = self.__students[username].getNeededCourses().copy()
                for TERM_IN, SUBJECT, COURSE_ID, CRN in courses_left:
                    self.__students[username].removeNeededCourse(
                        TERM_IN, SUBJECT, COURSE_ID, CRN, False)
            else:
                log.info(
                    f"{username} was removed from the registry with all courses fuffiled")
            del self.__students[username]
        else:
            log.warning(
                f"Deletion Failed as no info on {username} was found")

    def hasInfoFor(self, username: str):
        return username in self.__students
    def getStudentNames(self):
        return [username for username in self.__students]
