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


def scan_wifi_networks():
    ap_array = ['testap1', 'testap2']
    return ap_array


def create_wpa_supplicant(ssid, wifi_key):
    pass


def set_ap_client_mode():
    pass


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

scheduler = BackgroundScheduler()
scheduler.add_job(func=obtain_log_values, trigger="interval", seconds=5)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
