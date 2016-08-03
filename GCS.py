import threading
import time
import UDP_class as UDP
import json
import Tkinter as tk
import random
import traceback
import re
import argparse

class GUI_main(tk.Frame):
	def __init__(self, root, val_dict, UDP_client, close_all, *args, **kwargs):
		self.val_dict = val_dict
		self.UDP_client = UDP_client
		self.close_all = close_all

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
		# framw2 - row 1
		self.btn_send = tk.Button(frame2, text='Send command', command=self.on_btn_send)
		self.btn_send.grid(row=1, column=0, columnspan=1)
		self.ent_command = tk.Entry(frame2)
		self.ent_command.grid(row=1, column=1)
		self.ent_command.bind('<Return>', self.on_ent_command_enter)   
		# framw2 - row 2
		#self.lbl_command_param1 = tk.Label(frame2, text='param1:', fg='black',bg='white')
		#self.lbl_command_param1.grid(row=2, column=0, columnspan=1)
		#self.ent_command_param1 = tk.Entry(frame2)
		#self.ent_command_param1.grid(row=2, column=1)
		# framw2 - row 2
		#self.lbl_command_param2 = tk.Label(frame2, text='param2:', fg='black',bg='white')
		#self.lbl_command_param2.grid(row=3, column=0, columnspan=1)
		#self.ent_command_param2 = tk.Entry(frame2)
		#self.ent_command_param2.grid(row=3, column=1)
		# framw2 - row 2
		self.btn_listen_keys = tk.Button(frame2, fg='black', activebackground='red', bg='red', text='Listen keys - NO', width=25, command= self.on_btn_listen_keys)
		self.btn_listen_keys.grid(row=2, column=0, columnspan=1)
		self.btn_send_position = tk.Button(frame2, fg='black', activebackground='red', bg='red', text='Send zero position - NO', width=25, command= self.on_btn_send_position)
		self.btn_send_position.grid(row=2, column=1, columnspan=1)
		# framw2 - row 5
		#self.btn_close = tk.Button(frame2, text='Close all', width=25, command= self.on_btn_close)
		#self.btn_close.grid(row=5, column=0, columnspan=1)

		self.send_move_0 = 0
		self.key_pressed = None

	def on_btn_close(self):
		print "GCS: Close all - GUI button Close"
		self.close_all()

	def on_ent_command_enter(self, event):
		self.on_btn_send()
		self.ent_command.delete(0, tk.END)

	def on_btn_send(self):
		command = self.ent_command.get().split(' ')
		self.UDP_client.send_cmd(command)
		#print "GCS: Command sent: " + str(command)

	def on_btn_listen_keys(self):
		if self.btn_listen_keys.cget('bg') == "green":
			self.root.unbind("<Key>")
			self.root.unbind("<KeyRelease>")
			self.btn_listen_keys.config(text = "Listen keys - NO", activebackground='red', bg='red')
		elif self.btn_listen_keys.cget('bg') == "red":
			self.root.bind("<Key>", self.key_callback)
			self.root.bind("<KeyRelease>", self.key_release_callback)
			self.btn_listen_keys.config(text = "Listen keys - YES", activebackground='green', bg='green')

	def on_btn_send_position(self):
		if self.btn_send_position.cget('bg') == "green":
			self.send_move_0 = 0
			self.btn_send_position.config(text = "Send zero position - NO", activebackground='red', bg='red')
		elif self.btn_send_position.cget('bg') == "red":
			self.send_move_0 = 1
			self.btn_send_position.config(text = "Send zero position - YES", activebackground='green', bg='green')

	def on_window_close(self):
		print "GCS: Close all - GUI window close"
		self.close_all()

	def GUI_init_2labels(self, frame, key, label1_text, row1 ,column1):
		row2 = row1
		column2= column1 + 1
		lbl_name = tk.Label(frame, text=label1_text,font=('arial', 10, 'bold'), fg='green',bg='black')
		lbl_val = tk.Label(frame, font=('arial', 10, 'bold'), fg='green',bg='black')
		self.val_dict[key] = {'lbl_name': lbl_name, 'lbl_val': lbl_val, 'value': None}
		self.val_dict[key]['lbl_name'].grid(row=row1, column=column1, columnspan=1)
		self.val_dict[key]['lbl_val'].grid(row=row2, column=column2, columnspan=1)

	def key_release_callback(self, event):
		#self.key_pressed = None
		pass

	def key_callback(self, event):
		#print repr(event.char)	+ "Pressed"
		if (event.char=='z'):
			self.UDP_client.send_cmd(['arm', int(10)])
		if (event.char=='w'):
			self.key_pressed = event.char
		elif (event.char=='a'):
			self.key_pressed = event.char
		elif (event.char=='s'):
			self.key_pressed = event.char
		elif (event.char=='d'):
			self.key_pressed = event.char
		elif (event.char=='q'):
			self.UDP_client.send_cmd(['yaw_left', int(10)])
		elif (event.char=='e'):
			self.UDP_client.send_cmd(['yaw_right', int(10)])
		elif (event.char=='l'):
			self.UDP_client.send_cmd(['land'])
		elif (event.char=='t'):
			self.UDP_client.send_cmd(['triangle'])
		elif (event.char=='y'):
			self.UDP_client.send_cmd(['triangle2'])
		elif (event.char=='u'):
			self.UDP_client.send_cmd(['square'])
		elif (event.char=='i'):
			self.UDP_client.send_cmd(['square2'])
		elif (event.char=='p'):
			self.UDP_client.send_cmd(['diamond'])

	def GUI_close(self):
		self.root.destroy()
		self.root.quit()

	def GUI_tick(self):
		if (self.key_pressed == 'w'):
			self.UDP_client.send_cmd(['forward_once', int(1)])
		elif (self.key_pressed == 'a'):
			self.UDP_client.send_cmd(['left_once', int(1)])
		elif (self.key_pressed == 's'):
			self.UDP_client.send_cmd(['backward_once', int(1)])
		elif (self.key_pressed == 'd'):
			self.UDP_client.send_cmd(['right_once', int(1)])
		elif (self.key_pressed == None):
			#print "None pressed"
			if (self.send_move_0 == 1):
				self.UDP_client.send_cmd(['move_0_once'])
		else:
			print "Drone: WTF am I doing here?"
		# zero the pressed key. It will be renewed when auto press will be activated
		self.key_pressed = None
		
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


class GCS():
	def __init__(self):
		try:
			self.GUI = None
			#global dict : {'val_X', {'lbl_name': <label>, 'lbl_val': <label>, 'value': <value>}}
			self.val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'frame_loc_north', 'frame_loc_east', 'frame_loc_down', 'frame_gl_lat', 'frame_gl_lon', 'frame_gl_alt', 'frame_gl_rel_lat', 'frame_gl_rel_lon', 'frame_gl_rel_alt', 'battery', 'last_heartbeat', 'gps_0_HDOP', 'gps_0_VDOP', 'gps_0_fix', 'gps_0_satellites', 'ekf_ok', 'mode', 'armed', 'system_status'])
			# Init all val_dict fields
			self.dict_init_fields()

			self.parser = argparse.ArgumentParser(description='GCS module')
			self.parser.add_argument('--drone_ip')
			self.args = self.parser.parse_args()
			if not self.args.drone_ip:
				self.drone_ip = "255.255.255.255"
			else:
				self.drone_ip = self.args.drone_ip
			print "GSC: Open socket for Telemetry and user commands"
			self.UDP_client = UDP.UDP(0, "Telem/Cmd", "0.0.0.0", 6000, self.drone_ip, 5001)
			print "GSC: Open socket for drone Report"
			self.UDP_client_Report = UDP.UDP(0, "Drone Report", "0.0.0.0", 6100, self.drone_ip, 5101)
			
			print "GSC: Start receive Telem thread"
			self.UDP_client.receive_loop_telem_thread(self.val_dict)
			print "GSC: Start receive Report thread"
			self.UDP_client_Report.receive_loop_report_thread()
	
			self.run_GUI()

		except KeyboardInterrupt:
			print "GCS: Close all - keyboard interrupt in main"		
			self.close_all()


	def dict_init_fields(self):
		for key, val in self.val_dict.iteritems():
			self.val_dict[key] = dict.fromkeys(['value', 'lbl_val', 'lbl_name'])

	def run_GUI(self):
		self.root = tk.Tk()
		self.GUI = GUI_main(self.root, self.val_dict, self.UDP_client, self.close_all)
		try:
			print "GSC: GUI - Enter the mainloop"
			self.root.mainloop()
		except(KeyboardInterrupt , SystemExit):
			print "GCS: Close all - keyboard interrupt in GUI/console"
			self.close_all()

	def close_all(self):
	
		print "GCS: Close all - Telemetry/commands"
		self.UDP_client.close_UDP()
		print "GCS: Close all - Drone Report"
		self.UDP_client_Report.close_UDP()
	
		print "GCS: Close all - GUI"
		self.GUI.GUI_close()

		print "GCS: Close all - Complete"


if __name__ == "__main__":
		GCS = GCS()
else:
	print("You are running me not as a main?")
