import mechanize
from bs4 import BeautifulSoup
import logging

import utils.websis as websis
import utils.notifications as notify
import auth as auth

log = logging.getLogger("AutoRegistration.sub")


class Student:

    def __init__(self, username: str, password=None):
        self.username = username.strip()
        self.__password = password  # ! Shouldn't be plaintext in the future
        self.__courses = set()  # set((TERM_IN, SUBJECT, COURSE_ID, CRN))
        self.email = self.username + "@morgan.edu"
        self.br = None  # Logged In Websis Browser Session

    def getNeededCourses(self) -> set:
        return self.__courses

    def addNeededCourse(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str):
        self.__courses.add((TERM_IN, SUBJECT, COURSE_ID, CRN))
        # Send Confirmation Email
        notify.notifyStudent(self.username, TERM_IN,
                             SUBJECT, COURSE_ID, CRN, 0)

    def removeNeededCourse(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str, registred=True):
        self.__courses.remove((TERM_IN, SUBJECT, COURSE_ID, CRN))
        # Send Confirmation Email
        if registred:
            notify.notifyStudent(self.username, TERM_IN,
                                 SUBJECT, COURSE_ID, CRN, 3)
        else:
            notify.notifyStudent(self.username, TERM_IN,
                                 SUBJECT, COURSE_ID, CRN, 4)

    def registerFor(self, TERM_IN: str, SUBJECT: str, COURSE_ID: str, CRN: str) -> bool:
        if (not websis.WebsisSessionIsActive(self.br)):  # Don't Log Back in if we dont have to
            self.br = websis.LoginToWebsis(self)
        return websis.register_for_course(self.br, TERM_IN, SUBJECT, COURSE_ID, CRN)

    def getLoginInfo(self):
        return self.username, self.__password


class Manager:
    def __init__(self):
        # * Only one user is required to check any given course we use a master user for reliability
        self.master = Student(auth.username, auth.password)
        self.__master_sess = websis.LoginToWebsis(self.master)
        self.__students = dict()  # {uname: Student}

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
            html = websis.get_courses_page(
                websis.LoginToWebsis(self.master), TERM_IN, SUBJECT, COURSE_ID)

            soup = BeautifulSoup(html, features="html5lib")
            table = soup.find("table", attrs={
                              "summary": "This layout table is used to present the sections found"})
            rows = table.find_all("tr")[2:]

            # * Needs to be cleaned/commented desperately
            # * TBH Cant remember why this chunk works
            for row in rows:
                if row == None:
                    continue
                current_course_info = []
                lines = str(row).split("\n")
                for line in lines:
                    entry = BeautifulSoup(line, features="html5lib")
                    data = entry.text
                    if len(data) == 0:
                        continue
                    current_course_info.append(data)
            ###########################################
                if current_course_info[0] == "C":
                    continue  # Course on this row is full
                else:
                    if current_course_info[1] in crns2check:
                        # ? Should be sorted by the order they were added in
                        for student in crns2check[current_course_info[1]]:
                            if student.getLoginInfo()[1] != None:
                                succeeded = student.registerFor(
                                    current_course_info[1])
                                if succeeded == True:
                                    student.removeNeededCourse(
                                        TERM_IN, SUBJECT, COURSE_ID, current_course_info[1])
                                else:  # Notify Student of Failed Registration
                                    notify.notifyStudent(
                                        student.username, TERM_IN, SUBJECT, COURSE_ID, current_course_info[1], 4)
                                if (len(student.getNeededCourses()) == 0):
                                    self.RemoveStudent(student.username)
                            else:
                                notify.notifyStudent(
                                    student.username, TERM_IN, SUBJECT, COURSE_ID, current_course_info[1], 2)

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
            else:
                log.info(
                    f"{username} was removed from the registry with all courses fuffiled")
            del self.__students[username]
        else:
            log.warning(
                f"Deletion Failed as no info on {username} was found")

    def hasInfoFor(self, username: str):
        return username in self.__students
