import setup_lib
import os
import sys
import configparser

# checking for root

if check_root():
    sys.exit('Root access required, try running as sudo.')

# reading config settings
config = configparser.ConfigParser()
config.read('setup.cfg')
SSID = config['DEFAULT']['SSID']
ReconnectionDelay = config['DEFAULT']['ReconnectionDelay']

print('----------------------------------------------------------')
print('WiFi hotspot onboarding script and visualisation dashboard')
print('SSID: ' + SSID)
print('IP Address: "192.168.1.220"')
print('Port number: 80')
print('Configuration url: "config.com"')
print('Reconnection delay: '+ ReconnectionDelay)
print('----------------------------------------------------------')
install_ans = input('Install WiFi hotspot onboarding script and visualisation dashboard? [y/N]:')

if (install_ans.lower() == 'y'):
    setup_lib.install_packages()
    setup_lib.install_config()
else:
    sys.exit('Installation aborted.')

print('Setup complete!')
reboot_ans = input("Reboot required to activate WiFi settings. Reboot now? [y/N]: ")

if reboot_ans.lower() == 'y':
    os.system('reboot')