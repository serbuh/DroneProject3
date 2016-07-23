# DroneProject3

We use clean Ubuntu 14.04 with following dependencies installed:
- Drone-kit:
- FlyCapture:
[Fly Capture Guide](https://github.com/jordens/pyflycapture2)
```sh
mkdir ~/git
cd ~/git
git clone https://github.com/peterpolidoro/pyflycapture2.git
sudo apt-get install python-pip -y
sudo pip install cython
sudo pip install numpy
cd ~/git/pyflycapture2/
sudo python setup.py install
```

- TkInter:
```sh
sudo apt-get install python-tk
```

Connect via Telem with the following connection string:
```sh
sudo python drone_UDP_server.py --connect /dev/ttyUSB0,57600
```

Connect via USB with the following connection string:
```sh
sudo python drone_UDP_server.py --connect /dev/ttyACM0
```
Install MAVProxy:
```sh
pip install MAVProxy
```

Connect additional GCS (MAVProxy)
```sh
mavproxy.py --master tcp:127.0.0.1:5763 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --map
```

If module map is not loaded (fails to import cv) simply install that:
```sh
sudo apt-get install python-matplotlib python-serial python-wxgtk2.8 python-lxml
sudo apt-get install python-scipy python-opencv ccache gawk git python-pip python-pexpect
```

Possible new GUI + assync UDP design:
- [https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch09s07.html
](https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch09s07.html
)
- [http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/](http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/)


- drone's PC is a UDP Server. Need to put a client's IP in a HOST parameter.
- GCS PC is a UDP Client. Need to put localhost in a HOST parameter.
- hotspot:
Read http://odroid.com/dokuwiki/doku.php?id=en:xu4_wlan_ap#configuration_for_wifi_module_3
In short, download and patch hostapd, replace with existing. Then use create_ap for AP creation.
```
sudo apt-get install libnl-3-dev libnl-genl-3-dev libssl-dev hostapd iptables
sudo apt-get install --reinstall pkg-config
$ git clone https://github.com/pritambaral/hostapd-rtl871xdrv.git
$
$ wget https://w1.fi/releases/hostapd-2.5.tar.gz
$ tar xvfz hostapd-2.5.tar.gz
$ cd hostapd-2.5
$ patch -p1 < ../hostapd-rtl871xdrv/rtlxdrv.patch
$ cd hostapd
$ cp defconfig .config
$ echo CONFIG_LIBNL32=y >> .config
$ echo CONFIG_DRIVER_RTW=y >> .config
$ 
$ make
```
Backup the hostapd demon. Replace the demon with configured one.
```
$ cp /usr/sbin/hostapd /usr/sbin/hostapd.back
$ cp hostapd /usr/sbin/hostapd
```
Verify that you have installed the latest version
```
$ /usr/sbin/hostapd -v
hostapd v2.5 for Realtek rtl871xdrv
User space daemon for IEEE 802.11 AP management,
IEEE 802.1X/WPA/WPA2/EAP/RADIUS Authenticator
Copyright (c) 2002-2015, Jouni Malinen <j@w1.fi> and contributors
```
If Odroid has on ip with lan cable connected, run
```
dhclient eth0
```
To install create_ap: http://askubuntu.com/a/701049
```
git clone https://github.com/oblique/create_ap
cd create_ap
make install
```
No passphrase (open network):
```
create_ap wlan0 eth0 MyAccessPoint
```
WPA + WPA2 passphrase:
```
create_ap wlan0 eth0 MyAccessPoint MyPassPhrase
```
To create a service (AP on boot), copy create_ap.service from git repository (https://github.com/oblique/create_ap) to /etc/systemd/system/create_ap.service then edit it. This instructions is from http://www.runeaudio.com/forum/hostapd-configuration-wifi-hotspot-setup-t567.html
