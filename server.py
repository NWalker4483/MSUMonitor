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
    TERM_IN = request.form['trm']
    SUBJECT = request.form['subj'].upper()
    COURSE_ID = request.form['cid']
    CRN = request.form['crn']
    # TODO Add Better/More Status Msgs
    new_student = Student(MSU_USERNAME, MSU_PASSWORD)
    msg = f"Added {MSU_USERNAME} to {SUBJECT} {COURSE_ID} : {CRN} list behind {'null'} others"
    if not manager.hasInfoFor(MSU_USERNAME):
        # Validate Login Info
        if Student.WebsisSessionIsActive(Student.LoginToWebsis(new_student)):
            manager.AddStudent(new_student)
        else:
            msg = "Websis Login Failed Check Info "
    manager.AddCourseSubscribtion(
        TERM_IN, SUBJECT, COURSE_ID, CRN, MSU_USERNAME)
    return render_template('form.html', message=msg)


def ScheduleWebsisCall():
    global manager
    manager.CheckCourseAvailability()
    threading.Timer(60, ScheduleWebsisCall).start()


if __name__ == "__main__":
    MSU_USERNAME, MSU_PASSWORD = auth.username, auth.password

    manager = Manager()

    ScheduleWebsisCall()
    app.run()
