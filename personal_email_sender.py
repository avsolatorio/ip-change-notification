import smtplib
from datetime import datetime
import cPickle
import os
import enum

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "aivin.solatorio.ext@gmail.com"
you = "avsolatorio@gmail.com"

class return_code_enum(enum.Enum):
    failed = 0
    success = 1


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'personal_email_creds.dict')) as fl:
    # Load the credentials containing name and passwd for gmail.
    creds = cPickle.load(fl)


def email_to_me(text, html='', subject='Public IP Change'):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    return_code = return_code_enum.success
    try:
        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        # Uses less secure app
        mail.login(creds['name'], creds['passwd'])
        mail.sendmail(me, you, msg.as_string())
        mail.quit()
    except Exception as e:
        print('{}: Error ({})\n\tMessage ({})'.format(datetime.now(), type(e), e.args[0]))
        print('\tMessage not sent: {}'.format(text))
        return_code = return_code_enum.failed

    return return_code

