import time
import sys
import os
import reset_lib
import configparser

active_count = 0
time_with_no_connection = 0
# reading config settings
config = configparser.ConfigParser()
config.read('/usr/lib/pi-wifi-dash/scripts/config/setup.cfg')
reconnection_delay = int(config['DEFAULT']['ReconnectionDelay'])

while True:
    time.sleep(10)
    # Check for wifi connection every 10 secs
    if reset_lib.is_wifi_active() == False:
        time_with_no_connection += 10
        print("No wifi connection! Time with no connetion:", time_with_no_connection)
        active_count = 0
    else:
        print("Wifi connection found!")
        active_count += 1
        time_with_no_connection = 0
        if active_count >= 2:
            time_with_no_connection = 0
            active_count = 0
    if time_with_no_connection >= reconnection_delay:
        print("Resetting to host mode!")
        reset_lib.reset_to_host()