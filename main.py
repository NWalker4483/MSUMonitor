import requests
import urllib
from bs4 import BeautifulSoup
from utils import *
from test import Manager, Student
import time 
import auth 
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