import requests
import urllib
from bs4 import BeautifulSoup
from utils import *
from test import Manager, Student

me = True # Skip Manual Login Input
if me:
    MSU_USERNAME, MSU_PASSWORD = "niwal7", "Qfr3*9u9" 
    TERM_IN = "201930" 
    SUBJECT, COURSE_ID, CRN  = "MATH","241","18067" 
else:
    begin = False 
    while not begin:
        MSU_USERNAME, MSU_PASSWORD = getLoginInfo()
        TERM_IN = "201930" # Spring 2019
        SUBJECT, COURSE_ID, CRN  = getCourseInfo()
        begin = ConfirmInfo(MSU_USERNAME, MSU_PASSWORD,SUBJECT, COURSE_ID, CRN)

print("Beggining...")
app = Manager()
app.AddStudent(Student(MSU_USERNAME, MSU_PASSWORD))
app.AddCourseSubscribtion(TERM_IN, SUBJECT, COURSE_ID, CRN, MSU_USERNAME)
app.CheckCourseAvailability()