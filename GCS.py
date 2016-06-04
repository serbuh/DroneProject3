import threading
import time
import GCS_UDP_client as UDP
import json
import Tkinter as tk
import random

HOST = 'localhost'
TELEM_PORT = 3334
VIDEO_PORT = 3333


def dict_init_fields():
	for key, val in val_dict.iteritems():
		val_dict[key] = dict.fromkeys(['value', 'lbl_val', 'lbl_name'])

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

def close_all(run_event,get_telem,telem_client):
	print "GSC: Send event to all running threads to close"
	run_event.clear()
	get_telem_thread.join()
	print "GSC: get_telem_thread dead"
	telem_client.close_client()
	GUI_close()
	print "GUI: GUI closed"
	print "######## GSC: My work here is DONE ########"

######## GUI stuff ########
def GUI_init_2labels(key, label1_text, row1 ,column1):
	global GUI_root, val_dict
	row2 = row1
	column2= column1 + 1
	lbl_name = tk.Label(GUI_root, text=label1_text,font=('arial', 10, 'bold'), fg='green',bg='black')
	lbl_val = tk.Label(GUI_root, font=('arial', 10, 'bold'), fg='green',bg='black')     
	val_dict[key] = {'lbl_name': lbl_name, 'lbl_val': lbl_val, 'value': None}
	val_dict[key]['lbl_name'].grid(row=row1, column=column1, columnspan=1)
	val_dict[key]['lbl_val'].grid(row=row2, column=column2, columnspan=1)

# Initializing GUI
def GUI_init():
	GUI_init_2labels('roll', label1_text='Roll: ', row1=1, column1=1)
	GUI_init_2labels('pitch', label1_text='Pitch: ', row1=2, column1=1)
	GUI_init_2labels('yaw', label1_text='Yaw: ', row1=3, column1=1)
	GUI_init_2labels('vx', label1_text='Vx: ', row1=4, column1=1)
	GUI_init_2labels('vy', label1_text='Vy: ', row1=5, column1=1)
	GUI_init_2labels('vz', label1_text='Vz: ', row1=6, column1=1)
	GUI_init_2labels('heading', label1_text='Heading: ', row1=7, column1=1)
	GUI_init_2labels('rangefinder', label1_text='Rangefinder: ', row1=8, column1=1)
	GUI_init_2labels('gimbal_roll', label1_text='Gimbal roll: ', row1=9, column1=1)
	GUI_init_2labels('gimbal_pitch', label1_text='Gimbal pitch: ', row1=10, column1=1)
	GUI_init_2labels('gimbal_yaw', label1_text='Gimbal yaw: ', row1=11, column1=1)


	GUI_init_2labels('gps_0_HDOP', label1_text='HDOP: ', row1=1, column1=3)
	GUI_init_2labels('gps_0_VDOP', label1_text='VDOP: ', row1=2, column1=3)
	GUI_init_2labels('gps_0_fix', label1_text='GPS fix: ', row1=3, column1=3)
	GUI_init_2labels('gps_0_satellites', label1_text='Satellites: ', row1=4, column1=3)
	GUI_init_2labels('ekf_ok', label1_text='EKF OK: ', row1=5, column1=3)
	GUI_init_2labels('last_heartbeat', label1_text='Last heartbeat: ', row1=6, column1=3)
	GUI_init_2labels('battery', label1_text='Battery: ', row1=7, column1=3)
	

	GUI_init_2labels('ch1', label1_text='Ch1: ', row1=1, column1=5)
	GUI_init_2labels('ch2', label1_text='Ch2: ', row1=2, column1=5)
	GUI_init_2labels('ch3', label1_text='Ch3: ', row1=3, column1=5)
	GUI_init_2labels('ch4', label1_text='Ch4: ', row1=4, column1=5)
	GUI_init_2labels('ch5', label1_text='Ch5: ', row1=5, column1=5)
	GUI_init_2labels('ch6', label1_text='Ch6: ', row1=6, column1=5)
	GUI_init_2labels('ch7', label1_text='Ch7: ', row1=7, column1=5)
	GUI_init_2labels('ch8', label1_text='Ch8: ', row1=8, column1=5)

    
	GUI_init_2labels('frame_loc_north', label1_text='North (loc): ', row1=12, column1=1)
	GUI_init_2labels('frame_loc_east', label1_text='East (loc): ', row1=13, column1=1)
	GUI_init_2labels('frame_loc_down', label1_text='Down (loc): ', row1=14, column1=1)
	GUI_init_2labels('frame_gl_lat', label1_text='Lat (gl): ', row1=12, column1=3)
	GUI_init_2labels('frame_gl_lon', label1_text='Lon (gl): ', row1=13, column1=3)
	GUI_init_2labels('frame_gl_alt', label1_text='Alt (gl): ', row1=14, column1=3)
	GUI_init_2labels('frame_gl_rel_lat', label1_text='Lat (gl rel): ', row1=12, column1=5)
	GUI_init_2labels('frame_gl_rel_lon', label1_text='Lon (gl rel): ', row1=13, column1=5)
	GUI_init_2labels('frame_gl_rel_alt', label1_text='Alt (gl rel): ', row1=14, column1=5)


	GUI_init_2labels('airspeed', label1_text='Airspeed: ', row1=15, column1=1)
	GUI_init_2labels('groundspeed', label1_text='Groundspeed: ', row1=16, column1=1)	
	GUI_init_2labels('mode', label1_text='Mode: ', row1=17, column1=1)
	GUI_init_2labels('armed', label1_text='Armed: ', row1=18, column1=1)
	GUI_init_2labels('system_status', label1_text='System status: ', row1=19, column1=1)

	#TODO Design Q: why do we see here run_event, get_telem, telem_client. It is not defined as global...
	#TODO Design Q: Do I need to define globals then (GUI_root, val_dict)?
	GUI_button = tk.Button(text='Stop', width=25, command= lambda: close_all(run_event,get_telem,telem_client))
	GUI_button.grid(row=26, column=1, columnspan=2)

# Update the stored value in the dict with the new ones    
def GUI_dict_generate_new_values():
	global val_dict
	for key, val in val_dict.iteritems():
		if val['value'] == None:
			val['value'] = 0
		val['value'] += random.randint(1,5)

# Update label value with stored value in dict    
def GUI_dict_refresh_values():
	for key, val in val_dict.iteritems():
		val['lbl_val'].config(text=str(val['value']))
		#val_dict['roll']['lbl_val'].config(text=str(val_dict['roll']['value']))

def GUI_close():
	global GUI_root
	print("GUI: Closing GUI ...")
	GUI_root.destroy()
	GUI_root.quit()

def GUI_tick():
	global GUI_root	
	#GUI_dict_generate_new_values()
	GUI_dict_refresh_values()
	GUI_root.after(200, GUI_tick)

######## GUI stuff end ########



if __name__ == "__main__":
	#global dict : {'val_X', {'lbl_name': <label>, 'lbl_val': <label>, 'value': <value>}}
	val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'frame_loc_north', 'frame_loc_east', 'frame_loc_down', 'frame_gl_lat', 'frame_gl_lon', 'frame_gl_alt', 'frame_gl_rel_lat', 'frame_gl_rel_lon', 'frame_gl_rel_alt', 'battery', 'last_heartbeat', 'gps_0_HDOP', 'gps_0_VDOP', 'gps_0_fix', 'gps_0_satellites', 'ekf_ok', 'mode', 'armed', 'system_status'])
	# Init all val_dict fields
	dict_init_fields()

	print "*** GSC: START TELEM ***"	
	telem_client = UDP.GCS_UDP_client()
	telem_client.connect(HOST,TELEM_PORT)

	run_event = threading.Event()
	run_event.set()
	
	print("GSC: Start get_telem_thread")
	get_telem_thread = threading.Thread(target=get_telem, args=[telem_client,run_event])
	get_telem_thread.start()
	
####### Run GUI #######
	print "*** GSC: START GUI ***"
	GUI_root = tk.Tk()
	GUI_root.title("GCS GUI")
	GUI_root.configure(background='black')
	print "GUI: Init object"
	GUI_init()
	GUI_root.protocol('WM_DELETE_WINDOW', lambda: close_all(run_event,get_telem,telem_client))		
	print "GUI: Run GUI"
	GUI_root.after(0,GUI_tick)
	print "GSC: All set, GO!"
	try:
		GUI_root.mainloop()
	except(KeyboardInterrupt , SystemExit):
		close_all(run_event,get_telem,telem_client)
####### GUI end #######
