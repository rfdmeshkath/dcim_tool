import smtplib

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
    print('successfully sent the alerts')
    # except:
    #     print ("failed to send alerts")


send_email('rfdmeshkath@gmail.com', 'Automated Mail Header', 'Mail Body goes here.')
