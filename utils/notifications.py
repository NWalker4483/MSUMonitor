import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_NAME="Nile Walker"
MY_ADDRESS = 'nilezwalker@gmail.com'
PASSWORD = input('Enter the password for {}\n'.format(MY_ADDRESS))
MY_NUMBER='410-805-0012'
SUBJECT="Google Housing Request"
SERVER_ADDRESS="smtp.gmail.com"
PORT=587

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host=SERVER_ADDRESS, port=PORT)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for i in range(len(contacts)):
        info={
        'MY_NAME':MY_NAME,
        'MY_ADDRESS':MY_ADDRESS,
        'MY_NUMBER':MY_NUMBER,
        'LOCATION':contacts['Internship Location'][i],
        'FIRST_NAME':contacts["First Name"][i],
        'LAST_NAME':contacts["Last Name"][i],
        'START_DATE':contacts['Start Date'][i],
        'END_DATE':contacts['End Date'][i]
        }
        msg = MIMEMultipart()       # create a message
        # add in the actual person name to the message template
        message = message_template.substitute(**info)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=contacts['Email'][i]
        msg['Subject']=SUBJECT
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()

def SendEmail():
    pass