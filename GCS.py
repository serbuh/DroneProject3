import threading
import time
import UDP_class as UDP
import json
import Tkinter as tk
import random


######## GUI stuff ########
class GUI_main(tk.Frame):
	def __init__(self, root, val_dict, *args, **kwargs):
		self.val_dict = val_dict

		print "GCS: GUI - Start"
		tk.Frame.__init__(self, root, *args, **kwargs)
		self.root = root
		self.root.title("GCS GUI")
		self.root.configure(background='black')
		self.frame1 = tk.Frame(self.root)
		self.frame1.configure(background='black')
		self.frame2 = tk.Frame(self.root)
		self.frame2.configure(background='white')
		self.GUI_init(self.frame1,self.frame2)
		self.frame1.grid(row=0, column=0)
		self.frame2.grid(row=1, column=0)
		self.root.protocol('WM_DELETE_WINDOW', self.on_window_close)
		self.root.after(100,self.GUI_tick)

	def GUI_init(self, frame1, frame2):
		print "GCS: GUI - Init objects"
		# frame1
		self.GUI_init_2labels(frame1, 'roll', label1_text='Roll: ', row1=1, column1=1)
		self.GUI_init_2labels(frame1, 'pitch', label1_text='Pitch: ', row1=2, column1=1)
		self.GUI_init_2labels(frame1, 'yaw', label1_text='Yaw: ', row1=3, column1=1)
		self.GUI_init_2labels(frame1, 'vx', label1_text='Vx: ', row1=4, column1=1)
		self.GUI_init_2labels(frame1, 'vy', label1_text='Vy: ', row1=5, column1=1)
		self.GUI_init_2labels(frame1, 'vz', label1_text='Vz: ', row1=6, column1=1)
		self.GUI_init_2labels(frame1, 'heading', label1_text='Heading: ', row1=7, column1=1)
		self.GUI_init_2labels(frame1, 'rangefinder', label1_text='Rangefinder: ', row1=8, column1=1)
		self.GUI_init_2labels(frame1, 'gimbal_roll', label1_text='Gimbal roll: ', row1=9, column1=1)
		self.GUI_init_2labels(frame1, 'gimbal_pitch', label1_text='Gimbal pitch: ', row1=10, column1=1)
		self.GUI_init_2labels(frame1, 'gimbal_yaw', label1_text='Gimbal yaw: ', row1=11, column1=1)


		self.GUI_init_2labels(frame1, 'gps_0_HDOP', label1_text='HDOP: ', row1=1, column1=3)
		self.GUI_init_2labels(frame1, 'gps_0_VDOP', label1_text='VDOP: ', row1=2, column1=3)
		self.GUI_init_2labels(frame1, 'gps_0_fix', label1_text='GPS fix: ', row1=3, column1=3)
		self.GUI_init_2labels(frame1, 'gps_0_satellites', label1_text='Satellites: ', row1=4, column1=3)
		self.GUI_init_2labels(frame1, 'ekf_ok', label1_text='EKF OK: ', row1=5, column1=3)
		self.GUI_init_2labels(frame1, 'last_heartbeat', label1_text='Last heartbeat: ', row1=6, column1=3)
		self.GUI_init_2labels(frame1, 'battery', label1_text='Battery: ', row1=7, column1=3)
	

		self.GUI_init_2labels(frame1, 'ch1', label1_text='Ch1: ', row1=1, column1=5)
		self.GUI_init_2labels(frame1, 'ch2', label1_text='Ch2: ', row1=2, column1=5)
		self.GUI_init_2labels(frame1, 'ch3', label1_text='Ch3: ', row1=3, column1=5)
		self.GUI_init_2labels(frame1, 'ch4', label1_text='Ch4: ', row1=4, column1=5)
		self.GUI_init_2labels(frame1, 'ch5', label1_text='Ch5: ', row1=5, column1=5)
		self.GUI_init_2labels(frame1, 'ch6', label1_text='Ch6: ', row1=6, column1=5)
		self.GUI_init_2labels(frame1, 'ch7', label1_text='Ch7: ', row1=7, column1=5)
		self.GUI_init_2labels(frame1, 'ch8', label1_text='Ch8: ', row1=8, column1=5)

	    
		self.GUI_init_2labels(frame1, 'frame_loc_north', label1_text='North (loc): ', row1=12, column1=1)
		self.GUI_init_2labels(frame1, 'frame_loc_east', label1_text='East (loc): ', row1=13, column1=1)
		self.GUI_init_2labels(frame1, 'frame_loc_down', label1_text='Down (loc): ', row1=14, column1=1)
		self.GUI_init_2labels(frame1, 'frame_gl_lat', label1_text='Lat (gl): ', row1=12, column1=3)
		self.GUI_init_2labels(frame1, 'frame_gl_lon', label1_text='Lon (gl): ', row1=13, column1=3)
		self.GUI_init_2labels(frame1, 'frame_gl_alt', label1_text='Alt (gl): ', row1=14, column1=3)
		self.GUI_init_2labels(frame1, 'frame_gl_rel_lat', label1_text='Lat (gl rel): ', row1=12, column1=5)
		self.GUI_init_2labels(frame1, 'frame_gl_rel_lon', label1_text='Lon (gl rel): ', row1=13, column1=5)
		self.GUI_init_2labels(frame1, 'frame_gl_rel_alt', label1_text='Alt (gl rel): ', row1=14, column1=5)


		self.GUI_init_2labels(frame1, 'airspeed', label1_text='Airspeed: ', row1=15, column1=1)
		self.GUI_init_2labels(frame1, 'groundspeed', label1_text='Groundspeed: ', row1=16, column1=1)	
		self.GUI_init_2labels(frame1, 'mode', label1_text='Mode: ', row1=17, column1=1)
		self.GUI_init_2labels(frame1, 'armed', label1_text='Armed: ', row1=18, column1=1)
		self.GUI_init_2labels(frame1, 'system_status', label1_text='System status: ', row1=19, column1=1)

		# framw2 - row 0
		self.lbl_title = tk.Label(frame2, text='Mission controllsky - GCS' ,font=('arial', 16, 'bold'), fg='red',bg='white')
		self.lbl_title.grid(row=0, column=0, columnspan=6)
		self.btn_close = tk.Button(frame2, text='Close all', width=25, command= self.on_btn_close)
		self.btn_close.grid(row=0, column=6, columnspan=1)
		# framw2 - row 1
		self.lbl_command = tk.Label(frame2, text='Command:', fg='black',bg='white')
		self.lbl_command.grid(row=1, column=0, columnspan=1)
		self.ent_command = tk.Entry(frame2)
		self.ent_command.grid(row=1, column=1)
		self.lbl_command_param1 = tk.Label(frame2, text='param1:', fg='black',bg='white')
		self.lbl_command_param1.grid(row=1, column=2, columnspan=1)
		self.ent_command_param1 = tk.Entry(frame2)
		self.ent_command_param1.grid(row=1, column=3)
		self.lbl_command_param2 = tk.Label(frame2, text='param2:', fg='black',bg='white')
		self.lbl_command_param2.grid(row=1, column=4, columnspan=1)
		self.ent_command_param2 = tk.Entry(frame2)
		self.ent_command_param2.grid(row=1, column=5)
		self.btn_send = tk.Button(frame2, text='Send command', command=self.on_btn_send)
		self.btn_send.grid(row=1, column=6, columnspan=1)
		# framw2 - row 2
		self.lbl_sent = tk.Label(frame2, fg='black', bg='white', text='')
		self.lbl_sent.grid(row=2, column=0, columnspan=1)
		# framw2 - row 3
		self.btn_listen_keys = tk.Button(frame2, fg='black', activebackground='red', bg='red', text='Listen keys - NO', width=25, command= self.on_btn_listen_keys)
		self.btn_listen_keys.grid(row=3, column=0, columnspan=1)
		self.btn_send_position = tk.Button(frame2, fg='black', activebackground='red', bg='red', text='Send position - NO', width=25, command= self.on_btn_send_position)
		self.btn_send_position.grid(row=3, column=1, columnspan=1)
		# framw2 - row 4

		self.counter = 0
		self.send_move_0 = 0
		self.key_pressed = None

	def on_btn_close(self):
		print "GCS: Close all - GUI button Close"		
		close_all(UDP_client, self)

	def on_btn_send(self):
		pass
		#TODO
		#command = self.ent_command.get()
		#command_param1 = self.ent_command_param1.get()
		#command_param2 = self.ent_command_param2.get()
		#sent_command = "Sending: {" + command + " " + command_param1 + " " + command_param2 +"}"
		#self.lbl_sent.config(text = sent_command)
		#self.vehicle_controll.send_command(command, command_param1, command_param2)

	def on_btn_listen_keys(self):
		if self.btn_listen_keys.cget('bg') == "green":
			self.root.unbind("<Key>")
			self.root.unbind("<KeyRelease>")
			self.lbl_listen_keys.config(text = "Listen keys - NO", activebackground='red', bg='red')
		elif self.btn_listen_keys.cget('bg') == "red":
			self.root.bind("<Key>", self.key_callback)
			self.root.bind("<KeyRelease>", self.key_release_callback)
			self.btn_listen_keys.config(text = "Listen keys - YES", activebackground='green', bg='green')

	def on_btn_send_position(self):
		if self.btn_send_position.cget('bg') == "green":
			self.send_move_0 = 0
			self.btn_send_position.config(text = "Send position - NO", activebackground='red', bg='red')
		elif self.btn_send_position.cget('bg') == "red":
			self.send_move_0 = 1
			self.btn_send_position.config(text = "Send position - YES", activebackground='green', bg='green')

	def on_window_close(self):
		print "GCS: Close all - GUI window close"
		close_all(UDP_client, self)

	def GUI_init_2labels(self, frame, key, label1_text, row1 ,column1):
		row2 = row1
		column2= column1 + 1
		lbl_name = tk.Label(frame, text=label1_text,font=('arial', 10, 'bold'), fg='green',bg='black')
		lbl_val = tk.Label(frame, font=('arial', 10, 'bold'), fg='green',bg='black')
		self.val_dict[key] = {'lbl_name': lbl_name, 'lbl_val': lbl_val, 'value': None}
		self.val_dict[key]['lbl_name'].grid(row=row1, column=column1, columnspan=1)
		self.val_dict[key]['lbl_val'].grid(row=row2, column=column2, columnspan=1)

	def key_release_callback(self, event):
		self.key_pressed = None

	def key_callback(self, event):
		#print "pressed", repr(event.char)
		if (event.char=='z'):
			print "Z pressed"
			#self.vehicle_controll.send_command("arm", 10)
		if (event.char=='w'):
			self.key_pressed = "W"
			#self.vehicle_controll.send_command("forward", 20, 1)
		elif (event.char=='a'):
			self.key_pressed = "A"
			#self.vehicle_controll.send_command("left", 20, 1)
		elif (event.char=='s'):
			self.key_pressed = "S"
			#self.vehicle_controll.send_command("backward", 20, 1)
		elif (event.char=='d'):
			self.key_pressed = "D"
			#self.vehicle_controll.send_command("right", 20, 1)
		elif (event.char=='q'):
			print "Q pressed"
			#self.vehicle_controll.send_command("yaw_left", 10)
		elif (event.char=='e'):
			print "E pressed"
			#self.vehicle_controll.send_command("yaw_right", 10)
		elif (event.char=='l'):
			print "L pressed"
			#self.vehicle_controll.send_command("land", None)
		elif (event.char=='t'):
			print "T pressed"
			#self.vehicle_controll.send_command("triangle", None)
		elif (event.char=='y'):
			print "Y pressed"
			#self.vehicle_controll.send_command("triangle2", None)
		elif (event.char=='u'):
			print "U pressed"
			#self.vehicle_controll.send_command("square", None)
		elif (event.char=='i'):
			print "I pressed"
			#self.vehicle_controll.send_command("square2", None)
		elif (event.char=='p'):
			print "P pressed"
			#self.vehicle_controll.send_command("diamond", None)

	def GUI_close(self):
		self.root.destroy()
		self.root.quit()

	def GUI_tick(self):
		self.GUI_dict_refresh_values()
		self.root.after(100, self.GUI_tick)

	# Update the stored value in the dict with the new ones    
	def GUI_dict_generate_new_values(self):
		for key, val in self.val_dict.iteritems():
			if val['value'] == None:
				val['value'] = 0
			val['value'] += random.randint(1,5)

	# Update label value with stored value in dict    
	def GUI_dict_refresh_values(self):
		for key, val in self.val_dict.iteritems():
			val['lbl_val'].config(text=str(val['value']))
			#val_dict['roll']['lbl_val'].config(text=str(val_dict['roll']['value']))


######## GUI stuff end ########

def run_GUI(val_dict):
	root = tk.Tk()
	GUI = GUI_main(root, val_dict)
	try:
		print "GSC: GUI - Enter the mainloop"
		root.mainloop()
	except(KeyboardInterrupt , SystemExit):
		print "GCS: Close all - keyboard interrupt in GUI"
		close_all(UDP_client, GUI)

def close_all(UDP_client, GUI):
	
	print "GCS: Close all - Telemetry"
	UDP_client.close_UDP()
	
	print "GCS: Close all - GUI"
	GUI.GUI_close()

	print "GCS: Close all - Complete"


def dict_init_fields():
	for key, val in val_dict.iteritems():
		val_dict[key] = dict.fromkeys(['value', 'lbl_val', 'lbl_name'])



if __name__ == "__main__":
	try:
		GUI = None
		#global dict : {'val_X', {'lbl_name': <label>, 'lbl_val': <label>, 'value': <value>}}
		val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'frame_loc_north', 'frame_loc_east', 'frame_loc_down', 'frame_gl_lat', 'frame_gl_lon', 'frame_gl_alt', 'frame_gl_rel_lat', 'frame_gl_rel_lon', 'frame_gl_rel_alt', 'battery', 'last_heartbeat', 'gps_0_HDOP', 'gps_0_VDOP', 'gps_0_fix', 'gps_0_satellites', 'ekf_ok', 'mode', 'armed', 'system_status'])
		# Init all val_dict fields
		dict_init_fields()

		print "GSC: Main - Start Telem"
		UDP_client = UDP.UDP(0, "0.0.0.0", 6000, "255.255.255.255", 5001)

		print "GSC: Main - Start receive Telem thread"
		UDP_client.receive_loop_telem_thread(val_dict)
	
		run_GUI(val_dict)

	except KeyboardInterrupt:
		print "GCS: Close all - keyboard interrupt in main"		
		close_all(UDP_client, self)
else:
	print("You are running me not as a main?")
