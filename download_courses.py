# ! This process is painfully slow just set it and forget it
import mechanize
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import auth
import utils.websis as websis
import tqdm
login_url = "https://lbapp1nprod.morgan.edu/ssomanager/c/SSB"
CURRENT_TERM_ID = "202070"
sess = mechanize.Browser()
sess.set_handle_robots(False)  # ignore robots
sess.open(login_url)
sess.select_form(id="loginForm")
sess["username"], sess["password"] = auth.username, auth.password
sess.submit()

options = dict()
sess.open("https://lbssbnprod.morgan.edu/nprod/bwskfcls.p_sel_crse_search")

sess.select_form(nr=1)
sess["p_term"] = [CURRENT_TERM_ID]
res = sess.submit()
soup = BeautifulSoup(res.read(),features="lxml")

get_course_url = "https://lbssbnprod.morgan.edu/nprod/bwskfcls.P_GetCrse"
GenericParams = {"rsts": "dummy", "crn": "dummy",
                "sel_day": "dummy", "sel_schd": "dummy", "sel_insm": "dummy", "sel_camp": "dummy", "sel_levl": "dummy", "sel_sess": "dummy",
                "sel_instr": "dummy", "sel_ptrm": "dummy", "sel_attr": "dummy", "sel_crse": "", "sel_to_cred": "", "sel_title": "",
                "sel_from_cred": "", "begin_ap": "x", "end_ap": "y", "path": "1", "SUB_BTN": "Course Search",# "sel_ptrm": "%",
                "begin_hh": "0", "begin_mi": "0", "end_hh": "0", "end_mi": "0"}
# These need to be kept seperate for it to work
UserSpecifiedParams1 = {"term_in": CURRENT_TERM_ID, "sel_subj": "dummy"}
print("Downloading Course Info this will take several minutes")
a = 0
for option in tqdm.tqdm(soup.find("select").find_all('option')):
    UserSpecifiedParams2 = {"sel_subj": option['value']}
    options[option['value']] = dict()

    GenericParamsEncoded = urlencode(GenericParams)
    UserSpecifiedParamsEncoded = urlencode(
        UserSpecifiedParams1) + "&" + urlencode(UserSpecifiedParams2)
    AllParamsEncoded = UserSpecifiedParamsEncoded + "&" + GenericParamsEncoded
    full_url = get_course_url + "?" + AllParamsEncoded
    res = sess.open(full_url)
    html = res.read()

    soup = BeautifulSoup(html, features="html5lib")
    table = soup.find_all("table", attrs={
                        "summary": "This layout table is used to present the course found"})[1]
    rows = table.find_all("tr")[2:]
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
        ops = websis.get_options_for(sess,websis.CURRENT_TERM_ID,option["value"],current_course_info[0])    
        options[option['value']][current_course_info[0]] = list(ops.keys())
        #print(a)
        a += 1
    sess.back()

f = open('static/courses.json','w')
f.write(str(options).replace("\'","\""))
f.close()