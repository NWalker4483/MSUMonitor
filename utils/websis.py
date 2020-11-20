from urllib.parse import urlencode
import mechanize
from bs4 import BeautifulSoup

CURRENT_TERM_ID = "202070"

def register_for_course(br_session, TERM_IN, SUBJECT, COURSE_ID, CRN):
    # ! WARN: Totally doesnt work
    return ""

def get_options_for(br_session ,TERM_IN, SUBJECT, COURSE_ID):
    if (SUBJECT, COURSE_ID) == ("TEST","101"):
        return dict({"111111":1})
    options = dict()
    html = get_courses_page(br_session, TERM_IN, SUBJECT, COURSE_ID)

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
        Remaining, CRN = current_course_info[0], current_course_info[1]
        try:
            options[CRN] = int(Remaining)
        except Exception as e:
            #print(e)
            options[CRN] = 0 
   
        ###########################################
  
    return options

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
        return True, br
    except Exception as e:
        return False, br
if __name__ == "__main__":
    pass