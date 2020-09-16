from urllib.parse import urlencode
import mechanize


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


def get_courses_page(br_session, TERM_IN, SUBJECT, COURSE_ID) -> str:  # html
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


def get_available_courses(TERM_IN: str) -> dict:  # str
    sample = dict({"MATH":["241","201"],
                   "ENGR":["110","214"],
                   "COSC":["241","243"]})
    return sample


def WebsisSessionIsActive(sess: mechanize.Browser) -> bool:  # NOTE Not Done
    # Check wether a user is properly logged in
    try:
        return True
    except:
        pass
    return False


def LoginToWebsis(student):
    login_url = "https://lbapp1nprod.morgan.edu/ssomanager/c/SSB"
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)  # ignore robots
        br.open(login_url)
        br.select_form(id="loginForm")
        br["username"], br["password"] = student.getLoginInfo()
        br.submit()
        return br
    except Exception as e:
        raise(e)
