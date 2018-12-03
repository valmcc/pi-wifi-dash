import os


def check_root():
    return os.getuid()

def install_packages():
    print('Installing required packages')
    os.system('apt-get update')
    os.system('apt-get install python3 python3-rpi.gpio python3-pip dnsmasq hostapd -y')
    os.system('pip3 install flask pyopenssl')
    print('Packages installed!')

def install_config():
    os.system('mkdir /usr/lib/pi-wifi-dash')
    os.system('mkdir /etc/pi-wifi-dash')
    os.system('cp -a -r scripts /usr/lib/pi-wifi-dash/')
    os.system('cp -a -r webserver /usr/lib/pi-wifi-dash/')
    os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
    os.system('rm -f ./tmp/*')
    # copying configuration files for wifi hotspot
    os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak')
    os.system('cp /usr/lib/pi-wifi-dash/scripts/config/dnsmasq.conf /etc/')
    os.system('cp -a /usr/lib/pi-wifi-dash/scripts/config/hostapd.conf /etc/hostapd/')
    os.system('mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bak')
    os.system('cp /usr/lib/pi-wifi-dash/scripts/config/dhcpcd.conf /etc/')
    # making cronjob
    os.system('mkdir /etc/cron.pi-wifi-dash')
    os.system('cp /usr/lib/pi-wifi-dash/scripts/config/aphost /etc/cron.pi-wifi-dash')
    os.system('chmod +x /etc/cron.pi-wifi-dash/aphost')
    # making the aphost script run on startup
    os.system('echo "@reboot root run-parts /etc/cron.pi-wifi-dash/" >> /etc/crontab')
    # making a copy of the config file for future reference
    os.system('cp setup.cfg /usr/lib/pi-wifi-dash/scripts/config/')
    # referencing current mode
    os.system('touch /etc/pi-wifi-dash/host')


