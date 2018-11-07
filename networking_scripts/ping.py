from multiping import MultiPing
from time import sleep

from alerts.message import send_message


addresses = ["192.168.0.17"]
while True:
    mp = MultiPing(addresses)

    # Send the pings to those addresses
    mp.send()

    # With a 1 second timeout, wait for responses (may return sooner if all
    # results are received.
    responses, no_responses = mp.receive(1)
    print(responses.keys(), no_responses)
    sleep(5)
    if no_responses:
        print(no_responses)
        # send_message(phone_no='+353874323320', message_body='\n {} device(s) is down'.format(' '.join(no_responses)))
        break
    else:
        pass





