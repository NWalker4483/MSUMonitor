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
        self.__master_sess = websis.LoginToWebsis(self.master)
        self.__students = dict()  # {uname: Student}

    def getMasterSess(self):
        return self.__master_sess

    def CheckCourseAvailability(self):
        # Aggregate Course Requests
        courses2check = set()  # {(TERM_IN,SUBJECT,COURSE_ID)}
        crns2check = dict()  # {CRN: [Student()]}
        for student in self.__students.values():
            for TERM_IN, SUBJECT, COURSE_ID, CRN in student.getNeededCourses():
                courses2check.add((TERM_IN, SUBJECT, COURSE_ID))
                if CRN in crns2check:
                    crns2check[CRN].append(student)
                else:
                    crns2check[CRN] = [student]
        # Fufill Course Requests
        for TERM_IN, SUBJECT, COURSE_ID in courses2check:
            log.info(
                f"Checking {TERM_IN} {SUBJECT} {COURSE_ID} for availabilities")
            options = websis.get_options_for(websis.LoginToWebsis(
                self.master), TERM_IN, SUBJECT, COURSE_ID)
            for CRN in options:
                if options[CRN] > 0:
                    if CRN in crns2check:
                        # ? Should be sorted by the order they were added in
                        for student in crns2check[CRN]:
                            # If their password is not None
                            if student.getLoginInfo()[1] != None:
                                student.registerFor(
                                    TERM_IN, SUBJECT, COURSE_ID, CRN)
                                if (len(student.getNeededCourses()) == 0):
                                    self.RemoveStudent(student.username)
                            else:
                                notify.notifyStudent(
                                    student.username, TERM_IN, SUBJECT, COURSE_ID, CRN, 2)

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
