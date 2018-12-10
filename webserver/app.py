from flask import Flask, render_template, request, jsonify
import subprocess
import os
import time
import random
import json
from datetime import datetime
from collections import deque
from threading import Thread
from time import sleep
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.debug = True


#global variables
timestamp_log = deque(maxlen=72)
P1 = deque(maxlen=72)
P2 = deque(maxlen=72)
P3 = deque(maxlen=72)
P4 = deque(maxlen=72)
A1 = 0
A2 = 0
A3 = 0
A4 = 0

@app.route('/config')
def config():
    wifi_ap_array = scan_wifi_networks()

    return render_template('setup.html', wifi_ap_array=wifi_ap_array)


@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')


@app.route('/save_credentials', methods=['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']

    create_wpa_supplicant(ssid, wifi_key)

    def sleep_and_start_ap():
        time.sleep(2)
        set_ap_client_mode()
    t = Thread(target=sleep_and_start_ap)
    t.start()

    return render_template('save_credentials.html', ssid=ssid)

@app.route('/reset_host')
def reset_host():
    def sleep_and_reset_host():
        time.sleep(2)
        reset_to_host()
    t = Thread(target=sleep_and_reset_host)
    t.start()

    return render_template('reset_host.html')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/help')
def help():
    return render_template('help.html')

# GET requests for the graph/live values


@app.route('/_update_live_values', methods=['GET'])
def update_live_values():
    obtain_live_values()
    global A1
    global A2
    global A3
    global A4
    return jsonify(A1=A1, A2=A2, A3=A3, A4=A4)

@app.route('/_update_log_values', methods=['GET'])
def update_log_values():
    #obtain_log_values() # this should instead be triggered by an external timer
    return jsonify(timestamp_log=list(timestamp_log), P1=list(P1), P2=list(P2), P3=list(P3), P4=list(P4))


# Functions

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist', 'scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []

    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)

    return ap_array


def create_wpa_supplicant(ssid, wifi_key):
    temp_conf_file = open('wpa_supplicant.conf.tmp', 'w')

    temp_conf_file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    temp_conf_file.write('update_config=1\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('network={\n')
    temp_conf_file.write('  ssid="' + ssid + '"\n')

    if wifi_key == '':
        temp_conf_file.write('  key_mgmt=NONE\n')
    else:
        temp_conf_file.write('  psk="' + wifi_key + '"\n')

    temp_conf_file.write('  }')

    temp_conf_file.close

    os.system('mv wpa_supplicant.conf.tmp /etc/wpa_supplicant/wpa_supplicant.conf')


def set_ap_client_mode():
    os.system('rm -f /etc/pi-wifi-dash/host')
    os.system('rm /etc/cron.pi-wifi-dash/aphost')
    os.system('cp /usr/lib/pi-wifi-dash/scripts/config/apclient /etc/cron.pi-wifi-dash')
    os.system('chmod +x /etc/cron.pi-wifi-dash/apclient')
    os.system('mv /etc/dnsmasq.conf.orig /etc/dnsmasq.conf')
    os.system('mv /etc/dhcpcd.conf.orig /etc/dhcpcd.conf')
    #os.system('cp /usr/lib/raspiwifi/reset_device/static_files/isc-dhcp-server.apclient /etc/default/isc-dhcp-server')
    os.system('reboot')


def obtain_live_values():
    global A1
    global A2
    global A3
    global A4
    A1 = random.random()
    A2 = random.random()
    A3 = random.random()
    A4 = random.random()


def obtain_log_values():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_log.append(timestamp)
    global A1
    global A2
    global A3
    global A4
    obtain_live_values()
    P1.append(A1)
    P2.append(A2)
    P3.append(A3)
    P4.append(A4)

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

scheduler = BackgroundScheduler()
scheduler.add_job(func=obtain_log_values, trigger="interval", seconds=5)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
