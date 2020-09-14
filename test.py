import mechanize
from bs4 import BeautifulSoup
from utils import get_courses_page


class Status:
    TRIED_AND_SUCCEEDED = 0
    TRIED_AND_FAILED = 1
    LOGIN_FAILED = 2


class Student:
    login_url = "https://lbapp1nprod.morgan.edu/ssomanager/c/SSB"

    def __init__(self, username, password):
        self.__phone_num = None
        self.__username = username.strip()
        self.__password = password  # ! Shouldn't be plaintext in the future
        self.__courses = set()
        self.email = self.__username + "@morgan.edu"
        self.br = None  # Logged In Websis Browser Session

    def getNeededCourses(self) -> set:
        return self.__courses

    def addNeededCourse(self, TERM_IN, SUBJECT, COURSE_ID, CRN):
        self.__courses.add((TERM_IN, SUBJECT, COURSE_ID, CRN))

    def registerFor(self, TERM_IN, SUBJECT, COURSE_ID):
        if (not Student.WebsisSessionIsActive(self.br)):
            self.br = Student.LoginToWebsis(self)
        pass

    def notify(self, msg: str):
        print(self.email)

    def getLoginInfo(self):
        return self.__username, self.__password

    @staticmethod
    def WebsisSessionIsActive(sess: mechanize.Browser) -> bool:
        try:
            pass
        except:
            pass

    @staticmethod
    def LoginToWebsis(student):
        try:
            br = mechanize.Browser()
            br.set_handle_robots(False)  # ignore robots
            br.open(Student.login_url)
            br.select_form(id="loginForm")
            br["username"], br["password"] = student.getLoginInfo()
            br.submit()
            return br
        except Exception as e:
            raise(e)

class Manager:
    def __init__(self):
        # * Only one user is required to check any given course we use a master user for reliability
        self.master = Student("niwal7", input("Master Password\n"))
        self.__master_sess = Student.LoginToWebsis(self.master)
        self.__students = dict() # {uname: Student}

    def CheckCourseAvailability(self):
        # Aggregate Course Requests 
        courses2check = set()  # {(TERM_IN,SUBJECT,COURSE_ID)}
        crns2check = dict() # {CRN: [Student()]}
        for student in self.__students.values():
            for TERM_IN, SUBJECT, COURSE_ID, CRN in student.getNeededCourses():
                courses2check.add((TERM_IN, SUBJECT, COURSE_ID))
                if CRN in crns2check:
                    crns2check[CRN].append(student)
                else:
                    crns2check[CRN] = [student]
        # Fufill Course Requests 
        for TERM_IN, SUBJECT, COURSE_ID in courses2check:
            html = get_courses_page(
                self.__master_sess, TERM_IN, SUBJECT, COURSE_ID)
            soup = BeautifulSoup(html, features="html5lib")
            table = soup.find("table", attrs={
                              "summary": "This layout table is used to present the sections found"})
            rows = table.find_all("tr")[2:]

            # * Needs to be cleaned/commented desperately
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
                if current_course_info[0] == "C":
                    continue  # Course on this row is full
                else:
                    if current_course_info[1] in crns2check:
                        for student in crns2check[current_course_info[1]]:
                            student.notify("Test")
                    print("{} {} CRN: {} has {} spots left".format(
                        current_course_info[2], current_course_info[3], current_course_info[1], current_course_info[12]))
                    
    def AddCourseSubscribtion(self, TERM_IN, SUBJECT, COURSE_ID, CRN, username: str):
        self.__students[username].addNeededCourse(TERM_IN, SUBJECT, COURSE_ID, CRN)

    def AddStudent(self, student: Student):
        self.__students[student.getLoginInfo()[0]] = student
        

