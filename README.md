# DroneProject3
Drone Project

We use clean Ubuntu 14.04 with following dependencies installed:

Drone-kit:

FlyCapture:

TkInter:
sudo apt-get install python-tk

Connect via Telem with the following connection string:
sudo python drone_UDP_server.py --connect /dev/ttyUSB0,57600

Connect via USB with the following connection string:
sudo python drone_UDP_server.py --connect /dev/ttyACM0

Possible new GUI + assync UDP design:
https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch09s07.html
