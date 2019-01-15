import requests
import urllib
import mechanize
from bs4 import BeautifulSoup

def getCourseInfo():
    valid_input = False
    while not valid_input:
        try: 
            data = str(raw_input("Please enter the abbreviated course id and course number separated by a space \n for example 'ENGR 101'\n"))
            SUBJECT, COURSE_ID = data.split()
            _ = int(COURSE_ID)
            valid_input = True
        except:
            print("Invalid Input Retry...\n")
    valid_input = False
    while not valid_input:
        data = str(raw_input("Please enter the desired course number for {} {} \n for example '17225'\n".format(SUBJECT,COURSE_ID)))
        CRN = data
        try: 
            if(len(data)==5):
                _ = int(COURSE_ID)
                valid_input = True
            else:
                raise(ValueError)
        except:
            print("Invalid Input Retry...\n")
    return SUBJECT.upper(), COURSE_ID ,CRN

def getLoginInfo():
    username = raw_input(" Enter your MSU Websis username \n Do not add @morgan.edu\n")
    password = raw_input(" Enter your MSU Websis password \n Do not add @morgan.edu\n")
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
        inr = raw_input("Is this all Correct (y/N)")
        if inr in "yY":
            return True 
        elif inr in "nN":
            return False

def register_for_course(br_session,TERM_IN,SUBJECT,COURSE_ID):
    #br_session must be logged in
    get_course_url = "https://lbssbnprod.morgan.edu/nprod/bwskfcls.P_GetCrse"
    # Do not modify GenericParams
    GenericParams = {"SEL_TITLE":"","BEGIN_HH":"0", "BEGIN_MI":"0", "BEGIN_AP":"a", "SEL_DAY":"dummy", "SEL_PTRM":"dummy", "END_HH":"0", "END_MI":"0", "END_AP":"a", 
    "SEL_CAMP":"dummy", "SEL_SCHD":"dummy", "SEL_SESS":"dummy", "SEL_INSTR":"dummy", "SEL_INSTR":"%", "SEL_ATTR":"dummy", "SEL_ATTR":"%", "SEL_LEVL":"dummy", "SEL_LEVL":"%", 
    "SEL_INSM":"dummy", "sel_dunt_code":"", "sel_dunt_unit":"", "call_value_in":"", "rsts":"dummy", "crn":"dummy", "path":"1", "SUB_BTN":"View Sections"}
    # These need to be kept seperate for it to work
    UserSpecifiedParams1 = {"term_in": TERM_IN,"sel_subj":"dummy"}
    UserSpecifiedParams2 = {"sel_subj": SUBJECT, "SEL_CRSE": COURSE_ID}

    GenericParamsEncoded = urllib.urlencode(GenericParams)
    UserSpecifiedParamsEncoded = urllib.urlencode(UserSpecifiedParams1) + "&" + urllib.urlencode(UserSpecifiedParams2)
    AllParamsEncoded = UserSpecifiedParamsEncoded + "&" + GenericParamsEncoded
    full_url = get_course_url + "?" + AllParamsEncoded
    res = br_session.open(full_url)
    return res.read()

def get_courses_page(br_session,TERM_IN,SUBJECT,COURSE_ID):
    #br_session must be logged in
    get_course_url = "https://lbssbnprod.morgan.edu/nprod/bwskfcls.P_GetCrse"
    # Do not modify GenericParams
    GenericParams = {"SEL_TITLE":"","BEGIN_HH":"0", "BEGIN_MI":"0", "BEGIN_AP":"a", "SEL_DAY":"dummy", "SEL_PTRM":"dummy", "END_HH":"0", "END_MI":"0", "END_AP":"a", 
    "SEL_CAMP":"dummy", "SEL_SCHD":"dummy", "SEL_SESS":"dummy", "SEL_INSTR":"dummy", "SEL_INSTR":"%", "SEL_ATTR":"dummy", "SEL_ATTR":"%", "SEL_LEVL":"dummy", "SEL_LEVL":"%", 
    "SEL_INSM":"dummy", "sel_dunt_code":"", "sel_dunt_unit":"", "call_value_in":"", "rsts":"dummy", "crn":"dummy", "path":"1", "SUB_BTN":"View Sections"}
    # These need to be kept seperate for it to work
    UserSpecifiedParams1 = {"term_in": TERM_IN,"sel_subj":"dummy"}
    UserSpecifiedParams2 = {"sel_subj": SUBJECT, "SEL_CRSE": COURSE_ID}

    GenericParamsEncoded = urllib.urlencode(GenericParams)
    UserSpecifiedParamsEncoded = urllib.urlencode(UserSpecifiedParams1) + "&" + urllib.urlencode(UserSpecifiedParams2)
    AllParamsEncoded = UserSpecifiedParamsEncoded + "&" + GenericParamsEncoded
    full_url = get_course_url + "?" + AllParamsEncoded
    res = br_session.open(full_url)
    return res.read()

me = False
if me:
    MSU_USERNAME, MSU_PASSWORD = "niwal7", "######" 
    TERM_IN = "201930" 
    SUBJECT, COURSE_ID, CRN  = "CEGR","106","17225" 
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