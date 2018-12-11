import os
import reset_lib
import configparser

# reading config settings
config = configparser.ConfigParser()
config.read('/usr/lib/pi-wifi-dash/scripts/config/setup.cfg')
ssid = config['DEFAULT']['SSID']

# Check if ssid is the temporary one
ssid_temp = 'ssidtemp'

hostapd_reset = reset_lib.reset_required_check(ssid)

if hostapd_reset == True:
    reset_lib.update_ssid(ssid)
    os.system('reboot')

