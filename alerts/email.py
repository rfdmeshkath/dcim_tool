import smtplib
from time import sleep

from config import MAIL_CREDENTIAL


def send_email(recipient, subject, body):
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (MAIL_CREDENTIAL['username'], ", ".join(TO), SUBJECT, TEXT)
    # try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(MAIL_CREDENTIAL['username'], MAIL_CREDENTIAL['password'])
    server.sendmail(MAIL_CREDENTIAL['username'], TO, message)
    server.close()
    print('successfully sent')


# send_email('rfdmeshkath@gmail.com', 'Automated Mail Header', 'body\n hi')
