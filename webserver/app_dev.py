from flask import Flask, render_template, request, jsonify
import subprocess
import os
import time
import random
import json
from datetime import datetime
from collections import deque

app = Flask(__name__)
app.debug = True


#global variables
timestamp_log = deque(maxlen=72)
P1 = deque(maxlen=72)
P2 = deque(maxlen=72)
P3 = deque(maxlen=72)
P4 = deque(maxlen=72)


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

    # Call set_ap_client_mode() in a thread otherwise the reboot will prevent
    # the response from getting to the browser
    def sleep_and_start_ap():
        time.sleep(2)
        set_ap_client_mode()
    t = Thread(target=sleep_and_start_ap)
    t.start()

    return render_template('save_credentials.html', ssid=ssid)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/_update_live_values', methods=['GET'])
def update_live_values():
    A1, A2, A3, A4 = obtain_live_values()
    return jsonify(A1=A1, A2=A2, A3=A3, A4=A4)

@app.route('/_update_log_values', methods=['GET'])
def update_log_values():
    obtain_log_values()
    return jsonify(timestamp_log=list(timestamp_log), P1=list(P1), P2=list(P2), P3=list(P3), P4=list(P4))


######## FUNCTIONS ##########

def scan_wifi_networks():
    ap_array = ['testap1', 'testap2']
    return ap_array


def create_wpa_supplicant(ssid, wifi_key):
    pass


def set_ap_client_mode():
    pass


def obtain_live_values():
    A1 = random.random()
    A2 = random.random()
    A3 = random.random()
    A4 = random.random()
    return A1, A2, A3, A4


def obtain_log_values():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_log.append(timestamp)
    A1, A2, A3, A4 = obtain_live_values()
    P1.append(A1)
    P2.append(A2)
    P3.append(A3)
    P4.append(A4)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
