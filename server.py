from classes import Manager, Student
from flask import Flask, request, render_template
import threading
import auth

app = Flask(__name__)


@app.route('/')
def my_form():
    global manager
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    global manager
    MSU_USERNAME = request.form['username']
    MSU_PASSWORD = request.form['password']
    TERM_IN = "201930" #request.form['text']
    SUBJECT = request.form['subj'].upper()
    COURSE_ID = request.form['cid']
    CRN = request.form['crn']
    manager.AddStudent(Student(MSU_USERNAME, MSU_PASSWORD))
    manager.AddCourseSubscribtion(
        TERM_IN, SUBJECT, COURSE_ID, CRN, MSU_USERNAME)
    return render_template('form.html', message = "Added")
def ScheduleWebsisCall():
    global manager
    manager.CheckCourseAvailability()
    threading.Timer(60, ScheduleWebsisCall).start()


if __name__ == "__main__":
    MSU_USERNAME, MSU_PASSWORD = auth.username, auth.password
    TERM_IN = "201930"
    SUBJECT, COURSE_ID, CRN = "MATH", "241", "18067"
    manager = Manager()

    ScheduleWebsisCall()
    app.run()
