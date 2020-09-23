from classes import Manager, Student
import utils.websis as websis
from flask import Flask, request, render_template
import threading
import auth
import logging
import sys 
import time 
logging.basicConfig(filename='AutoRegistration.log', format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)

app = Flask("AutoRegistration")
app.logger.addHandler(handler)

@app.route('/')
def my_form():
    global manager
    return render_template('form.html',courses = websis.get_available_courses(""))

@app.route('/check', methods=['POST'])
def CheckCourseSubscriptions():
    global manager

@app.route('/subscribe', methods=['POST'])
def ProcessCourseSubscribtionForm():
    global manager
    MSU_USERNAME = request.form['username'].strip()
    MSU_PASSWORD = request.form['password']
    TERM_IN = request.form['trm']
    SUBJECT, COURSE_ID = request.form["course"].split()
    CRN = request.form['crn'] # TODO Add Better/More Status Msgs
    new_student = Student(MSU_USERNAME, MSU_PASSWORD)
    msg = f"Added {MSU_USERNAME} to {SUBJECT} {COURSE_ID} : {CRN} list behind {'null'} others"
    if not manager.hasInfoFor(MSU_USERNAME):
        # Validate Login Info
        if websis.WebsisSessionIsActive(websis.LoginToWebsis(new_student)):
            manager.AddStudent(new_student)
        else:
            msg = "Websis Login Failed Check Info "
            app.logger.error("Websis Login Failed Check Info ")

    if manager.hasInfoFor(MSU_USERNAME):
        manager.AddCourseSubscribtion(
            TERM_IN, SUBJECT, COURSE_ID, CRN, MSU_USERNAME)
        app.logger.info(msg)
            
    return render_template('form.html', message=msg, courses = websis.get_available_courses(""))


def ScheduleWebsisCheck(t=60):
    global manager
    manager.CheckCourseAvailability()
    threading.Timer(t, ScheduleWebsisCheck).start()


if __name__ == "__main__":
    manager = Manager()
    ScheduleWebsisCheck(60)# Seconds 
    app.run(debug=True)
