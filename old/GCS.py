import threading
import time
from GCS_UDP_client import *
from GCS_GUI import *
import json

HOST = 'localhost'
TELEM_PORT = 3334
VIDEO_PORT = 3333

#dict : {'val_X', {'lbl_name': <label>, 'lbl_val': <label>, 'value': <value>}}
val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'lat_loc', 'lon_loc', 'alt_loc', 'lat_gl', 'lon_gl', 'alt_gl', 'lat_gl_rel', 'lon_gl_rel', 'alt_gl_rel', 'battery', 'last_heartbeat'])

def dict_init_fields():
	for key, val in val_dict.iteritems():
		val_dict[key] = dict.fromkeys(['value', 'lbl_val', 'lbl_name'])
# Init all val_dict fields
dict_init_fields()

def get_telem(telem_client,run_event):
	global val_dict	
	while run_event.is_set():
		data = telem_client.receive()
		#TODO change eval(str(dict)) to smth
		data_dict = eval(data)
		#print data_dict
		for rec_key, rec_val in data_dict.iteritems():
			if val_dict.has_key(rec_key):
				val_dict[rec_key]['value'] = rec_val
			else:
				print 'GCS WARNING: Trying to update not existing item in val_dict: ' + str(rec_key) + ' Message ' + str(rec_val)

def inf_loop():
	while 1:
		time.sleep(1)

def close_all(run_event,get_telem,telem_client):
	print "GSC: Send event to all running threads to close"
	run_event.clear()
	get_telem_thread.join()
	print "GSC: get_telem_thread dead"
	telem_client.close_client()
	print "GSC: Socket closed"
	print "######## GSC: My work here is DONE ########"

if __name__ == "__main__":

	print "*** GSC: START TELEM ***"	
	telem_client = GCS_UDP_client()
	telem_client.connect(HOST,TELEM_PORT)

	run_event = threading.Event()
	run_event.set()
	
	print("GSC: Start get_telem_thread")
	get_telem_thread = threading.Thread(target=get_telem, args=[telem_client,run_event])
	get_telem_thread.start()
	
	print "*** GSC: START GUI ***"
	GUI=GCS_GUI(val_dict)

	print("GSC: Start run_GUI_thread")
	run_GUI_thread = threading.Thread(target=GUI.run_GUI, args=[])
	run_GUI_thread.start()
	
	print "GSC: All set, GO!"

	try:
		inf_loop()
	except(KeyboardInterrupt , SystemExit):
		close_all(run_event,get_telem,telem_client)
		pass

