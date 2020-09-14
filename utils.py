from urllib.parse import urlencode


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
# ! WARN: Totally doesnt work


def register_for_course(br_session, TERM_IN, SUBJECT, COURSE_ID):
    # br_session must be logged in
    get_course_url = "https://lbssbnprod.morgan.edu/nprod/bwskfcls.P_GetCrse"
    # Do not modify GenericParams
    GenericParams = {"SEL_TITLE": "", "BEGIN_HH": "0", "BEGIN_MI": "0", "BEGIN_AP": "a", "SEL_DAY": "dummy", "SEL_PTRM": "dummy", "END_HH": "0", "END_MI": "0", "END_AP": "a",
                     "SEL_CAMP": "dummy", "SEL_SCHD": "dummy", "SEL_SESS": "dummy", "SEL_INSTR": "dummy", "SEL_INSTR": "%", "SEL_ATTR": "dummy", "SEL_ATTR": "%", "SEL_LEVL": "dummy", "SEL_LEVL": "%",
                     "SEL_INSM": "dummy", "sel_dunt_code": "", "sel_dunt_unit": "", "call_value_in": "", "rsts": "dummy", "crn": "dummy", "path": "1", "SUB_BTN": "View Sections"}
    # These need to be kept seperate for it to work
    UserSpecifiedParams1 = {"term_in": TERM_IN, "sel_subj": "dummy"}
    UserSpecifiedParams2 = {"sel_subj": SUBJECT, "SEL_CRSE": COURSE_ID}

    GenericParamsEncoded = urlencode(GenericParams)
    UserSpecifiedParamsEncoded = urlencode(
        UserSpecifiedParams1) + "&" + urlencode(UserSpecifiedParams2)
    AllParamsEncoded = UserSpecifiedParamsEncoded + "&" + GenericParamsEncoded
    full_url = get_course_url + "?" + AllParamsEncoded
    res = br_session.open(full_url)
    return res.read()


def get_courses_page(br_session, TERM_IN, SUBJECT, COURSE_ID):
    # br_session must be logged in
    get_course_url = "https://lbssbnprod.morgan.edu/nprod/bwskfcls.P_GetCrse"
    # Do not modify GenericParams
    GenericParams = {"SEL_TITLE": "", "BEGIN_HH": "0", "BEGIN_MI": "0", "BEGIN_AP": "a", "SEL_DAY": "dummy", "SEL_PTRM": "dummy", "END_HH": "0", "END_MI": "0", "END_AP": "a",
                     "SEL_CAMP": "dummy", "SEL_SCHD": "dummy", "SEL_SESS": "dummy", "SEL_INSTR": "dummy", "SEL_INSTR": "%", "SEL_ATTR": "dummy", "SEL_ATTR": "%", "SEL_LEVL": "dummy", "SEL_LEVL": "%",
                     "SEL_INSM": "dummy", "sel_dunt_code": "", "sel_dunt_unit": "", "call_value_in": "", "rsts": "dummy", "crn": "dummy", "path": "1", "SUB_BTN": "View Sections"}
    # These need to be kept seperate for it to work
    UserSpecifiedParams1 = {"term_in": TERM_IN, "sel_subj": "dummy"}
    UserSpecifiedParams2 = {"sel_subj": SUBJECT, "SEL_CRSE": COURSE_ID}

    GenericParamsEncoded = urlencode(GenericParams)
    UserSpecifiedParamsEncoded = urlencode(
        UserSpecifiedParams1) + "&" + urlencode(UserSpecifiedParams2)
    AllParamsEncoded = UserSpecifiedParamsEncoded + "&" + GenericParamsEncoded
    full_url = get_course_url + "?" + AllParamsEncoded
    res = br_session.open(full_url)
    return res.read()
