import requests
import urllib
import mechanize
from bs4 import BeautifulSoup
MSU_USERNAME = "######" # Do not add @morgan.edu
MSU_PASSWORD = "######"
TERM_IN = "201930" # Spring 2019
SUBJECT = "CEGR"
COURSE_ID = 106
GOAL_CRN = '12345'
logged_in = False
login_url = "https://lbapp1nprod.morgan.edu/ssomanager/c/SSB"
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots
fails = 0 
while not logged_in:
    fails+=1
    if fails > 2:
        print("Login Errors") 
        break
    br.open(login_url)
    br.select_form(id="loginForm")
    br["password"] = MSU_PASSWORD 
    br["username"] = MSU_USERNAME
    br.submit()
    #Add Check
    logged_in = True
print("Logged In")

get_course_url = "https://lbssbnprod.morgan.edu/nprod/bwskfcls.P_GetCrse"
GenericParams = {
    "SEL_TITLE":"",
    "BEGIN_HH":"0", 
    "BEGIN_MI":"0", 
    "BEGIN_AP":"a", 
    "SEL_DAY":"dummy", 
    "SEL_PTRM":"dummy", 
    "END_HH":"0", 
    "END_MI":"0", 
    "END_AP":"a", 
    "SEL_CAMP":"dummy", 
    "SEL_SCHD":"dummy", 
    "SEL_SESS":"dummy", 
    "SEL_INSTR":"dummy", 
    "SEL_INSTR":"%", 
    "SEL_ATTR":"dummy", 
    "SEL_ATTR":"%", 
    "SEL_LEVL":"dummy", 
    "SEL_LEVL":"%", 
    "SEL_INSM":"dummy", 
    "sel_dunt_code":"", 
    "sel_dunt_unit":"", 
    "call_value_in":"", 
    "rsts":"dummy", 
    "crn":"dummy", 
    "path":"1", 
    "SUB_BTN":"View Sections"}
UserSpecifiedParams1 = {
    "term_in": TERM_IN,
    "sel_subj":"dummy"}
UserSpecifiedParams2 = {
    "sel_subj": SUBJECT,
    "SEL_CRSE": COURSE_ID}

GenericParamsEncoded = urllib.urlencode(GenericParams)
UserSpecifiedParamsEncoded = urllib.urlencode(UserSpecifiedParams1) + "&" + urllib.urlencode(UserSpecifiedParams2)
AllParamsEncoded = UserSpecifiedParamsEncoded + "&" + GenericParamsEncoded#urllib.urlencode(AllParams)
full_url = get_course_url + "?" + AllParamsEncoded
res = br.open(full_url)

html = res.read() # Url for the lists of the courses requested

soup = BeautifulSoup(html,features="html5lib")
table = soup.find("table", attrs={"summary":"This layout table is used to present the sections found"})
available_courses = set()
entries = []
rows = table.find_all("tr")[2:]

for j in range(0,len(rows),22):
    entry = []
    for i in range(22):
        try:
            #print(rows[j+i])
            entry.append(str(rows[j+i].text[15:-4]))
        except:
            pass
    entries.append(entry)
for entr in entries[0]:
    data = entr.split('\n')
    if data[0] != 'heet':
        if int(data[11]) > 0:
            print("{} {} CRN: {} is available".format(data[1],data[2],data[0]))
            available_courses.add(data[0])
        else:
            print("{} {} CRN: {} is not available".format(data[1],data[2],data[0]))
    elif data[14] > 0: # Output Fails
        print("{} {} CRN: {} is available".format(data[4],data[5],data[3]))
    else:
        print("{} {} CRN: {} is not available".format(data[4],data[5],data[3]))

print("###\n"+full_url)

