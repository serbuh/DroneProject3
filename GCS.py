import threading
import time
from GCS_UDP_client import *

HOST = 'localhost'
TELEM_PORT = 3334
VIDEO_PORT = 3333

val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'lat', 'lon', 'alt', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'last_heartbeat'])

def get_telem(telem_client,run_event):
	global val_dict	
	while run_event.is_set():
		data_json = telem_client.receive()
		print data_json
		#TODO put in val_dict

if __name__ == "__main__":
	telem_client = GCS_UDP_client()
	telem_client.connect(HOST,TELEM_PORT)

	run_event = threading.Event()
	run_event.set()
	
	print("Start get_telem_thread")
	get_telem_thread = threading.Thread(target=get_telem, args=[telem_client,run_event])
	get_telem_thread.start()

	try:
		while 1:
			time.sleep(1)
	except(KeyboardInterrupt , SystemExit):
		print "Send event to all running threads to close"
		run_event.clear()
		get_telem_thread.join()
		print "get_telem_thread dead"
		telem_client.close_client()
		print "Socket closed"
		print "######## My work here is DONE ########"

