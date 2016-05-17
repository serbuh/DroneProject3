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

Possible new GUI + assync UDP design:
- [https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch09s07.html
](https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch09s07.html
)
- [http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/](http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/)


- drone's PC is a UDP Server. Need to put a client's IP in a HOST parameter.
- GCS PC is a UDP Client. Need to put localhost in a HOST parameter.
- hotspot:
ap-hotspot uses hostapd
- hostapd, 64 bit:
cd /tmp
wget http://old-releases.ubuntu.com/ubuntu/pool/universe/w/wpa/hostapd_1.0-3ubuntu2.1_amd64.deb
sudo dpkg -i hostapd*.deb
sudo apt-mark hold hostapd

- hostapd, 32 bit:
cd /tmp
wget http://old-releases.ubuntu.com/ubuntu/pool/universe/w/wpa/hostapd_1.0-3ubuntu2.1_i386.deb
sudo dpkg -i hostapd*.deb
sudo apt-mark hold hostapd


 ```sh
apt-get install hostapd
```
Configure:
```sh
sudo ap-hotspot configure
```
Start/Stop:
```sh
sudo ap-hotspot start
sudo ap-hotspot stop
sudo ap-hotspot restart
```
List of commands:
```sh
ap-hotspot
```

```sh
cd /etc/hostapd
cat host.conf
```
