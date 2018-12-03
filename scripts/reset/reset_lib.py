import os
import subprocess
import time


def reset_required_check(ssid):
    hostapd_conf = open('/etc/hostapd/hostapd.conf', 'r')
    reset = True
    for line in hostapd_conf:
        if ssid in line:
            reset = False

    return reset


def update_ssid(ssid):
    os.system('cp -a /usr/lib/pi-wifi-dash/scripts/config/hostapd.conf /etc/hostapd/')

    with fileinput.FileInput("/etc/hostapd/hostapd.conf", inplace=True) as file:
        for line in file:
            print(line.replace("ssidtemp", ssid), end='')
            file.close

def is_wifi_active():
    iwconfig_out = subprocess.check_output(['iwconfig']).decode('utf-8')
    wifi_active = True
    if "Access Point: Not-Associated" in iwconfig_out:
        wifi_active = False

    return wifi_active

def reset_to_host():
    if not os.path.isfile('/etc/pi-wifi-dash/host'):  # if not already in host mode
        os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
        os.system('rm /etc/cron.pi-wifi-dash/apclient')
        os.system('cp /usr/lib/pi-wifi-dash/scripts/config/aphost /etc/cron.pi-wifi-dash')
        os.system('chmod +x /etc/cron.pi-wifi-dash/aphost')
        os.system('mv /etc/dhcpcd.conf /etc/dhcpcd.conf.orig')
        os.system('cp /usr/lib/pi-wifi-dash/scripts/config/dhcpcd.conf /etc/')
        os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig')
        os.system('cp /usr/lib/pi-wifi-dash/scripts/config/dnsmasq.conf /etc/')
        os.system('cp /usr/lib/pi-wifi-dash/scripts/config/hostapd.conf /etc/hostapd/')
        os.system('touch /etc/pi-wifi-dash/host')
    os.system('reboot')
