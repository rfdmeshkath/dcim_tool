from twilio.rest import Client


def send_message(phone_no='+353874323320', message_body=''):
    """
    phone_no = '+353874323320' - is the Phone number I used to verify my Twilio account
    for now I can only send text message to this number
    :param phone_no: receivers phone number
    :param message_body: message body
    :return: nothing for now
    """
    account_sid = 'AC7a988332a024a8ab8aeaa6526e2e4863'  # got this from Twilio Console Dashboard
    auth_token = '430b39388e991c940f3b5b2e1ffa4eb8'  # got this from Twilio Console Dashboard
    client = Client(account_sid, auth_token)

    # Phone number given to you by Twilio
    # all message will come from this number
    twilio_number = '+18507249675'
    message_body = '\n' + message_body
    client.messages.create(to=phone_no, from_=twilio_number, body=message_body)
