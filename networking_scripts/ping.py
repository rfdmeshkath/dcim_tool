import os

from alerts.message import send_message


def check_ping(hostname):
    response = os.system("ping " + hostname)
    # checking for response
    if response == 0:
        pingstatus = 'Active'
    else:
        pingstatus = 'Down'

    return pingstatus


hostname = ''
while True:
    status = check_ping(hostname)
    if status == 'Down':
        send_message(phone_no='+353874323320', message_body=hostname + ' is down.')
        break
    elif status == 'Active':
        pass
