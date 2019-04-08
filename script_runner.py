from time import sleep

from checks.check_device_status import device_status_main
from checks.check_disconnected_connections import disconnected_connection_main
from checks.check_memory import memory_main
from checks.check_port_error import port_error_main
from config import all_devices
from networking_scripts.basic_info_collector import basic_info_collector
from networking_scripts.details_info_collector import details_info_collector


while True:
    # running information collector
    basic_info_collector(all_devices)
    sleep(1)
    details_info_collector(all_devices)
    sleep(1)
    # after collecting collecting data about devices
    # running checks on them
    device_status_main()
    sleep(1)
    disconnected_connection_main()
    sleep(1)
    memory_main()
    sleep(1)
    port_error_main()
    sleep(1)
    break