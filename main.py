import requests
import urllib
import mechanize
from bs4 import BeautifulSoup
from utils import *

me = False # Skip Manual Login Input
if me:
    MSU_USERNAME, MSU_PASSWORD = "mawar9", "###########" 
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
login_url = "https://lbapp1nprod.morgan.edu/ssomanager/c/SSB"
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots

br.open(login_url)
br.select_form(id="loginForm")
br["password"] = MSU_PASSWORD
br["username"] = MSU_USERNAME
br.submit()
print("Logged In")

html = get_courses_page(br,TERM_IN,SUBJECT,COURSE_ID) # Url for the lists of the courses requested

soup = BeautifulSoup(html,features="html5lib")
table = soup.find("table", attrs={"summary":"This layout table is used to present the sections found"})
rows = table.find_all("tr")[2:]
found = False
for row in rows:
    if row == None:
        continue
    current_course_info = []
    lines = str(row).split("\n")
    for line in lines:
        entry = BeautifulSoup(line,features="html5lib")
        data = entry.text
        if len(data) == 0:
            continue
        current_course_info.append(data)
    if current_course_info[0] == "C":
        print("{} {} CRN: {} is full ".format(current_course_info[2],current_course_info[3],current_course_info[1]))
    else:
        print("{} {} CRN: {} has {} spots left".format(current_course_info[2],current_course_info[3],current_course_info[1],current_course_info[12]))
        if current_course_info[1] == CRN:
            found = True
            print("Requested crn availability was found attempting registration...")
if not found:
    print("The requested course was not available Retrying...")