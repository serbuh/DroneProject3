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
