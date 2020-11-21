import logging

import utils.websis as websis
import utils.notifications as notify
import auth as auth

log = logging.getLogger("AutoRegistration.sub")


class Student:

    def __init__(self, username: str, password = None):
        self.username = username.strip()
        self.__password = password  # ! Shouldn't be plaintext in the future
        self.__courses = set()  # set((TERM_IN, SUBJECT, COURSE_ID, CRN))
        self.attempts = dict()  # dict((TERM_IN, SUBJECT, COURSE_ID, CRN))
        self.br = None  # Logged In Websis Browser Session

    def getNeededCourses(self) -> set:
        return self.__courses

    def addNeededCourse(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str):
        self.__courses.add((TERM_IN, SUBJECT, COURSE_ID, CRN))
        self.attempts[(TERM_IN, SUBJECT, COURSE_ID, CRN)] = 0
        # Send Confirmation Email
        status = 1 if self.__password == None else 0 
        notify.notifyStudent(self.username, TERM_IN,
                             SUBJECT, COURSE_ID, CRN, status)
 
    def removeNeededCourse(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str, registered=True):
        self.__courses.remove((TERM_IN, SUBJECT, COURSE_ID, CRN))
        # Send Confirmation Email
        notify.notifyStudent(self.username, TERM_IN,
                             SUBJECT, COURSE_ID, CRN, 3 if registered else 4)

    def registerFor(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str) -> bool:
        if (not websis.WebsisSessionIsActive(self.br)):  # Don't Log Back in if we dont have to
            self.br = websis.LoginToWebsis(self)
        success = websis.register_for_course(
            self.br, TERM_IN, SUBJECT, COURSE_ID, CRN)
        if success == True:
            self.removeNeededCourse(
                TERM_IN, SUBJECT, COURSE_ID, CRN)
        else:  # Notify Student of Failed Registration
            notify.notifyStudent(
                self.username, TERM_IN, SUBJECT, COURSE_ID, CRN, 4)
        return success

    def getLoginInfo(self):
        return self.username, self.__password
