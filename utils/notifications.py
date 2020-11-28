import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

MY_ADDRESS = 'msu.register.tool@gmail.com'
PASSWORD = 'MSURegister2'
MAIL_SUBJECT = "MSU Register Tool Update"
SERVER_ADDRESS = "smtp.gmail.com"
PORT = 587

template_list = [
    "Added_to_waitlist_with_registration.txt",
    "Added_to_waitlist_without_registration.txt",
    "Course_availability_found.txt",
    "Course_registration_successful.txt",
    "Course_registration_unsuccessful.txt"
]


class EmailThread(Thread):
    def __init__(self):
        self.msg = None
        Thread.__init__(self)

    def setup(self, USERNAME, TERM_IN, SUBJECT, COURSE_ID, CRN, status=0):
        msg = MIMEMultipart()  # create a message

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = USERNAME + "@morgan.edu"
        msg['Subject'] = MAIL_SUBJECT

        info = {
            'USERNAME': USERNAME,
            'TERM_IN': TERM_IN,
            'SUBJECT': SUBJECT,
            'COURSE_ID': COURSE_ID,
            'CRN': CRN,
        }

        with open("utils/messages/"+template_list[status], 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        message_template = Template(template_file_content)

        # add in the actual person name to the message template
        message = message_template.substitute(**info)
        msg.attach(MIMEText(message, 'plain'))
        self.msg = msg

    def send(self):
        self.start()

    def run(self):
        # set up the SMTP server AND Login
        s = smtplib.SMTP(host=SERVER_ADDRESS, port=PORT)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)
        s.send_message(self.msg)
        s.quit()


def verifyEmail(email):  # https://stackoverflow.com/questions/22233848/how-to-verify-an-email-address-in-python-using-smtplib
    # server = smtplib.SMTP(SERVER_ADDRESS, PORT)
    # server.connect()
    # server.set_debuglevel(True)
    # try:
    #     server.verify(email)
    # except Exception:
    #     return False
    # finally:
    #     server.quit()
    return True


def notifyStudent(USERNAME, TERM_IN, SUBJECT, COURSE_ID, CRN, status=0):
    email = EmailThread()
    email.setup(USERNAME, TERM_IN, SUBJECT, COURSE_ID, CRN, status=status)
    email.send()
