# DroneProject3

**Connect Odroid**  
1. Connect to remote computer to qtcopter Wi-Fi.  
2. Connect remote computer via SSH to Odroid:  
   ```
ssh odroid@192.168.12.1
   ```
   (password: odroid)
3. Go to the drone's code folder:  
   ```
cd DroneProject3/
   ```  
4. Run the Drone's code on Odroid  
  a. If Odroid connected via USB:  
   ```
   sudo python drone_CoPilot.py --connect /dev/ttyACM0 --gcs_ip 192.168.x.x
   ```  
   b. If Odroid connected via Telem:  
   ```
   sudo python drone_CoPilot.py --connect /dev/ttyUSB0,57600 --gcs_ip 192.168.x.x
   ```  
   c. If you want to add a video transmit from a drone add  
   ```
   --video_client_ip xxx.xxx.xxx.xxx --video_client_port yyyy --video_server_port zzzz
   ```  
   (flag. xxx.xxx.xxx.xxx - is the client's ip, yyyy - client's port, zzzz - server's port (of the socket through which we are sending the video))  
5. Run the GCS on Remote computer, (connected to Drone via Wi-Fi)  
  a. On Windows:  
   ```
   sudo python GCS.py --drone_ip 192.168.12.1
   ```  
   b. On Linux:  
   ```
   python GCS.py --drone_ip 192.168.12.1
   ```  
   c. If you want to add a video receive from a drone add  
   ```
   --video_port xxxx
   ```  
   (flag. xxxx - is the port for receiving the video)  
6. (Optional) Run Mission Planer on another or same remote computer (connected through Telemetry dongle):  
   ```
   mavproxy.py --master tcp:127.0.0.1:5763 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551 --map 
   ``` 

Connect via Telem with the following connection string:
```
sudo python drone_UDP_server.py --connect /dev/ttyUSB0,57600
```
   
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

Install serial:
```sh
sudo pip install pyserial
```


Install MAVProxy:
```sh
sudo pip install MAVProxy
```

Connect MAVProxy from Odroid to Pixhawk via (1) Telem or (2) USB
```sh
mavproxy.py --master=/dev/ttyACM0 --baudrate 115200
mavproxy.py --master=/dev/ttyUSB0 --baudrate 57600
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



**ESC Calibration sequence**  
1. Remove props  
2. Turn on RC  
3. Throttle to MAX  
4. Connect battery  
5. Notice LED pattern (Blue,Red,Green)  
6. Disconnect battery  
7. Re-connect battery  
8. Press the safety switch  
9. Wait for single beep  
10. Throttle to MIN  
11. Wait for three beeps  
12. Disconnect battery  
  
tutorial link: https://www.youtube.com/watch?v=Hl-Q7RPOn18
