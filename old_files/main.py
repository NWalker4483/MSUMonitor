import requests
import urllib
from bs4 import BeautifulSoup
from classes import Manager, Student
import time 
import auth 

def getCourseInfo():
    valid_input = False
    while not valid_input:
        try:
            data = str(input(
                "Please enter the abbreviated course id and course number separated by a space \n for example 'ENGR 101'\n"))
            SUBJECT, COURSE_ID = data.split()
            _ = int(COURSE_ID)
            valid_input = True
        except:
            print("Invalid Input Retry...\n")
    valid_input = False
    while not valid_input:
        data = str(input("Please enter the desired course number for {} {} \n for example '17225'\n".format(
            SUBJECT, COURSE_ID)))
        CRN = data
        try:
            if(len(data) == 5):
                _ = int(COURSE_ID)
                valid_input = True
            else:
                raise(ValueError)
        except:
            print("Invalid Input Retry...\n")
    return SUBJECT.upper(), COURSE_ID, CRN


def getLoginInfo():
    username = input(
        " Enter your MSU Websis username \n Do not add @morgan.edu\n").strip()
    password = input(
        " Enter your MSU Websis password \n Do not add @morgan.edu\n").strip()
    return username, password


def ConfirmInfo(MSU_USERNAME, MSU_PASSWORD, SUBJECT, COURSE_ID, CRN):
    warning = """Please be aware that this software has no checks in order to ensure that the course information entered is valid. please take this time to thoroughly check the information you've entered \n""".upper()
    print(warning)
    print("MSU_USERNAME: {}".format(MSU_USERNAME))
    print("MSU_PASSWORD: {}".format(MSU_PASSWORD))
    print("SUBJECT: {}".format(SUBJECT))
    print("COURSE_ID: {}".format(COURSE_ID))
    print("CRN: {}".format(CRN))
    while True:
        inr = input("Is this all Correct (y/N)").strip()
        if inr in "yY":
            return True
        elif inr in "nN":
            return False
me = False # Skip Manual Login Input
if me:
    MSU_USERNAME, MSU_PASSWORD = auth.username, auth.password
    TERM_IN = "201930" 
    SUBJECT, COURSE_ID, CRN  = "MATH","241","18067" 
else:
    begin = False 
    while not begin:
        MSU_USERNAME, MSU_PASSWORD = getLoginInfo()
        TERM_IN = "201930" # Spring 2019
        SUBJECT, COURSE_ID, CRN  = getCourseInfo()
        begin = ConfirmInfo(MSU_USERNAME, MSU_PASSWORD, SUBJECT, COURSE_ID, CRN)

app = Manager()
app.AddStudent(Student(MSU_USERNAME, MSU_PASSWORD))
app.AddCourseSubscribtion(TERM_IN, SUBJECT, COURSE_ID, CRN, MSU_USERNAME)
while True:
    try:
        app.CheckCourseAvailability()
        time.sleep(10)
    except KeyboardInterrupt:
        break 
    finally:
        pass