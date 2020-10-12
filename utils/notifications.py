import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_NAME = "Nile Walker"
MY_ADDRESS = 'msu.register.tool@gmail.com'
PASSWORD = 'MSURegister1'
SUBJECT = "Google Housing Request"
SERVER_ADDRESS = "smtp.gmail.com"
PORT = 587

template_list = [
    "Added_to_waitlist_with_registration.txt",
    "Added_to_waitlist_without_registration.txt",
    "Course_availability_found.txt ",
    "Course_registration_successful.txt",
    "Course_registration_unsuccessful.txt"
]

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def notifyStudent(USERNAME, TERM_IN, SUBJECT, COURSE_ID, CRN, status=0):
    message_template = read_template("messages/"+template_list[status])

    # set up the SMTP server AND Login
    s = smtplib.SMTP(host=SERVER_ADDRESS, port=PORT)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()  # create a message

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = USERNAME + "@morgan.edu"

    msg['Subject'] = SUBJECT

    info = {
        'USERNAME': USERNAME,
        'TERM_IN': TERM_IN,
        'SUBJECT': SUBJECT,
        'COURSE_ID': COURSE_ID,
        'CRN': CRN,
    }

    # add in the actual person name to the message template
    message = message_template.substitute(**info)

    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    # Terminate the SMTP session and close the connection
    s.quit()
