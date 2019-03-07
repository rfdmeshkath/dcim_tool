from multiping import MultiPing
from time import sleep


def check_if_device_is_reachable(addresses):
    mp = MultiPing(addresses)
    # Send the pings to those addresses
    mp.send()
    # With a 1 second timeout, wait for responses (may return sooner if all
    # results are received.
    responses, no_responses = mp.receive(1)
    # print(responses.keys(), no_responses)
    # sleep(5)
    if no_responses:
        # print(no_responses)
        return no_responses
    return []






