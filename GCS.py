import threading
import time
import UDP_class as UDP
import json
import Tkinter as tk
import random
import traceback
import re
import argparse
import datetime

class GUI_main(tk.Frame):
	def __init__(self, GCS):
		self.GCS = GCS
		self.prnt = GCS.prnt
		self.prnt("GCS","GUI - Start")
		self.root = GCS.root
		self.GUI_init()

		self.root.protocol('WM_DELETE_WINDOW', self.on_window_close)
		self.root.after(100,self.GUI_tick)

	def GUI_init(self):
		self.prnt("GCS", "GUI - Init")
		tk.Frame.__init__(self, self.root)
		self.root.title("GCS GUI")
		self.root.configure(background='black')
		
		self.control_frame_row, self.control_frame_column, = 0, 0
		self.HUD_frame_row, self.HUD_frame_column, = 1, 0
		self.firmware_frame_row, self.firmware_frame_column, self.firmware_frame_hide = 2, 0, True
		self.test_frame_row, self.test_frame_column, self.test_frame_hide = 0, 2, True
		self.mission_frame_row, self.mission_frame_column, self.mission_frame_hide = 0, 1, True

		self.init_control_frame(frame_row=self.control_frame_row, frame_column=self.control_frame_column)
		self.init_HUD_frame(frame_row=self.HUD_frame_row, frame_column=self.HUD_frame_column)
		self.init_firmware_frame(frame_row=self.firmware_frame_row, frame_column=self.firmware_frame_column)
		self.init_test_frame(frame_row=self.test_frame_row, frame_column=self.test_frame_column)
		self.init_mission_frame(frame_row=self.mission_frame_row, frame_column=self.mission_frame_column)

		self.send_move_0 = 0
		self.key_pressed = None



	def init_control_frame(self, frame_row, frame_column):
		self.control_frame = tk.Frame(self.root)
		self.control_frame.configure(background='white')

		# row 0
		self.lbl_title = tk.Label(self.control_frame, text='Mission controllsky - GCS' ,font=('arial', 16, 'bold'), fg='red',bg='white')
		self.lbl_title.grid(row=0, column=0, columnspan=6)

		# row 1
		self.btn_send = tk.Button(self.control_frame, text='Send command ->', width=15, command=self.on_btn_send)
		self.btn_send.grid(row=1, column=0, columnspan=1)

		self.ent_command = tk.Entry(self.control_frame)
		self.ent_command.grid(row=1, column=1)
		self.ent_command.bind('<Return>', self.on_ent_command_enter)

		# row 2
		if (self.firmware_frame_hide == True):
			text_btn_check_firmware = "Show firmware"
		else:
			text_btn_check_firmware = "Hide firmware"
		self.btn_check_firmware = tk.Button(self.control_frame, fg='black', text=text_btn_check_firmware, width=15, command= self.on_btn_check_firmware)
		self.btn_check_firmware.grid(row=2, column=0, columnspan=1)

		if (self.test_frame_hide == True):
			text_btn_test_frame = "Show test frame"
		else:
			text_btn_test_frame = "Hide test frame"
		self.btn_test_frame = tk.Button(self.control_frame, fg='black', text=text_btn_test_frame, width=15, command= self.on_btn_test_frame)
		self.btn_test_frame.grid(row=3, column=0, columnspan=1)


		if (self.mission_frame_hide == True):
			text_btn_mission_frame = "Show mission frame"
		else:
			text_btn_mission_frame = "Hide mission frame"
		self.btn_mission_frame = tk.Button(self.control_frame, fg='black', text=text_btn_mission_frame, width=15, command= self.on_btn_mission_frame)
		self.btn_mission_frame.grid(row=4, column=0, columnspan=1)


		# row 5,6
		self.btn_send_position = tk.Button(self.control_frame, fg='black', text='Send zero position', width=15, command= self.on_btn_send_position)
		self.btn_send_position.grid(row=5, column=0, columnspan=1)
		self.lbl_send_position = tk.Label(self.control_frame, text='NO', fg='black',bg='red')
		self.lbl_send_position.grid(row=5, column=1, columnspan=1)

		self.btn_listen_keys = tk.Button(self.control_frame, fg='black', text='Listen keys', width=15, command= self.on_btn_listen_keys)
		self.btn_listen_keys.grid(row=6, column=0, columnspan=1)
		self.lbl_listen_keys = tk.Label(self.control_frame, text='NO', fg='black',bg='red')
		self.lbl_listen_keys.grid(row=6, column=1, columnspan=1)

		# row 7
		self.lbl_failsafe = tk.Label(self.control_frame, text='Activate flight modes:', font=('arial', 12, 'bold'), fg='red',bg='white')
		self.lbl_failsafe.grid(row=7, column=0, columnspan=3)

		# row 8, 9, 10
		self.btn_land = tk.Button(self.control_frame, fg='black', activebackground='green2', text='Land', width=25, command= self.on_btn_land)
		self.btn_land.grid(row=8, column=0, columnspan=1)

		self.btn_rtl = tk.Button(self.control_frame, fg='black', activebackground='green2', text='RTL', width=25, command= self.on_btn_rtl)
		self.btn_rtl.grid(row=8, column=1, columnspan=1)

		self.btn_stabilize = tk.Button(self.control_frame, fg='black', activebackground='green2', text='Stabilize', width=25, command= self.on_btn_stabilize)
		self.btn_stabilize.grid(row=9, column=0, columnspan=1)

		self.btn_loiter = tk.Button(self.control_frame, fg='black', activebackground='green2', text='Loiter', width=25, command= self.on_btn_loiter)
		self.btn_loiter.grid(row=9, column=1, columnspan=1)

		self.btn_guided = tk.Button(self.control_frame, fg='black', activebackground='green2', text='Guided', width=25, command= self.on_btn_guided)
		self.btn_guided.grid(row=10, column=0, columnspan=1)

		self.btn_poshold = tk.Button(self.control_frame, fg='black', activebackground='green2', text='Position Hold', width=25, command= self.on_btn_poshold)
		self.btn_poshold.grid(row=10, column=1, columnspan=1)

		self.control_frame.grid(row=frame_row, column=frame_column)

	def on_btn_land(self):
		self.GCS.UDP_client.send_cmd(['land'])

	def on_btn_rtl(self):
		self.GCS.UDP_client.send_cmd(['rtl'])

	def on_btn_stabilize(self):
		self.GCS.UDP_client.send_cmd(['stabilize'])

	def on_btn_loiter(self):
		self.GCS.UDP_client.send_cmd(['loiter'])

	def on_btn_guided(self):
		self.GCS.UDP_client.send_cmd(['guided'])

	def on_btn_poshold(self):
		self.GCS.UDP_client.send_cmd(['poshold'])


	def on_btn_refresh_state(self):
		self.GCS.UDP_client.send_cmd(['refresh_state'])


	def on_btn_close(self):
		self.prnt("GCS","Close all - GUI button Close")
		self.GCS.close_all()

	def on_ent_command_enter(self, event):
		self.on_btn_send()
		self.ent_command.delete(0, tk.END)

	def on_btn_send(self):
		command = self.ent_command.get().split(' ')
		self.GCS.UDP_client.send_cmd(command)
		#self.prnt("GCS","Command sent: " + str(command))

	def on_btn_listen_keys(self):
		if self.lbl_listen_keys.cget('bg') == "green3":
			self.root.unbind("<Key>")
			self.root.unbind("<KeyRelease>")
			self.lbl_listen_keys.config(text = "NO", bg='red')
		elif self.lbl_listen_keys.cget('bg') == "red":
			self.root.bind("<Key>", self.key_callback)
			self.root.bind("<KeyRelease>", self.key_release_callback)
			self.lbl_listen_keys.config(text = "YES", bg='green3')

	def on_btn_send_position(self):
		if self.lbl_send_position.cget('bg') == "green3":
			self.send_move_0 = 0
			self.lbl_send_position.config(text = "NO", bg='red')
		elif self.lbl_send_position.cget('bg') == "red":
			self.send_move_0 = 1
			self.lbl_send_position.config(text = "YES", bg='green3')

	def on_btn_check_firmware(self):
		if (self.firmware_frame_hide == True):
			self.firmware_frame.grid(row=self.firmware_frame_row, column=self.firmware_frame_column)
			self.GCS.UDP_client.send_cmd(['check_firmware'])
			self.firmware_frame_hide = False
			self.btn_check_firmware.config(text = "Hide firmware")
		else:
			self.firmware_frame.grid_remove()
			self.firmware_frame_hide = True
			self.btn_check_firmware.config(text = "Show firmware")

	def on_btn_test_frame(self):
		if (self.test_frame_hide == True):
			self.test_frame.grid(row=self.test_frame_row, column=self.test_frame_column)
			self.test_frame_hide = False
			self.btn_test_frame.config(text = "Hide Test frame")
		else:
			self.test_frame.grid_remove()
			self.test_frame_hide = True
			self.btn_test_frame.config(text = "Show Test frame")

	def on_btn_mission_frame(self):
		if (self.mission_frame_hide == True):
			self.mission_frame.grid(row=self.mission_frame_row, column=self.mission_frame_column)
			self.mission_frame_hide = False
			self.btn_mission_frame.config(text = "Hide Mission frame")
		else:
			self.mission_frame.grid_remove()
			self.mission_frame_hide = True
			self.btn_mission_frame.config(text = "Show Mission frame")



	def init_HUD_frame(self, frame_row, frame_column):
		self.HUD_frame = tk.Frame(self.root)
		self.HUD_frame.configure(background='black')

		row, col = 1, 1
		self.GUI_init_2labels(self.HUD_frame, 'frame_loc_north', label1_text='North (loc): ', row1=row+0, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'frame_loc_east', label1_text='East (loc): ', row1=row+1, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'frame_loc_down', label1_text='Down (loc): ', row1=row+2, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'frame_gl_lat', label1_text='Lat (gl): ', row1=row+0, column1=col+2)
		self.GUI_init_2labels(self.HUD_frame, 'frame_gl_lon', label1_text='Lon (gl): ', row1=row+1, column1=col+2)
		self.GUI_init_2labels(self.HUD_frame, 'frame_gl_alt', label1_text='Alt (gl): ', row1=row+2, column1=col+2)
		self.GUI_init_2labels(self.HUD_frame, 'frame_gl_rel_lat', label1_text='Lat (gl rel): ', row1=row+0, column1=col+4)
		self.GUI_init_2labels(self.HUD_frame, 'frame_gl_rel_lon', label1_text='Lon (gl rel): ', row1=row+1, column1=col+4)
		self.GUI_init_2labels(self.HUD_frame, 'frame_gl_rel_alt', label1_text='Alt (gl rel): ', row1=row+2, column1=col+4)
		#self.GUI_init_dummy_label(self.HUD_frame, row=row+3, column=1)

		row, col = 4, 1
		self.btn_refresh_state = tk.Button(self.HUD_frame, text='Refresh state:', command= self.on_btn_refresh_state, font=('arial', 10, 'bold'), bg='black', activebackground='black', fg='green', activeforeground='green3')
		self.btn_refresh_state.grid(row=row+0, column=col, columnspan=1)
		self.GUI_init_2labels(self.HUD_frame, 'ekf_ok', label1_text='EKF OK: ', row1=row+1, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'system_status', label1_text='System status: ', row1=row+2, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'is_armable_on_demand', label1_text='Is Armable: ', row1=row+3, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'mode', label1_text='Mode: ', row1=row+4, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'armed', label1_text='Armed: ', row1=row+5, column1=col)

		row, col= 11, 1
		self.GUI_init_2labels(self.HUD_frame, 'battery', label1_text='Battery: ', row1=row+0, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gps_0_HDOP', label1_text='HDOP: ', row1=row+1, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gps_0_VDOP', label1_text='VDOP: ', row1=row+2, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gps_0_satellites', label1_text='Satellites: ', row1=row+3, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gps_0_fix', label1_text='GPS fix: ', row1=row+4, column1=col)

		row, col = 16, 1
		self.GUI_init_2labels(self.HUD_frame, 'airspeed', label1_text='Airspeed: ', row1=row+0, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'groundspeed', label1_text='Groundspeed: ', row1=row+1, column1=col)	
		self.GUI_init_2labels(self.HUD_frame, 'last_heartbeat', label1_text='Last heartbeat: ', row1=row+2, column1=col)

		row, col = 5, 3
		self.GUI_init_2labels(self.HUD_frame, 'roll', label1_text='Roll: ', row1=row+0, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'pitch', label1_text='Pitch: ', row1=row+1, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'yaw', label1_text='Yaw: ', row1=row+2, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'vx', label1_text='Vx: ', row1=row+3, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'vy', label1_text='Vy: ', row1=row+4, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'vz', label1_text='Vz: ', row1=row+5, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'heading', label1_text='Heading: ', row1=row+6, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'rangefinder', label1_text='Rangefinder: ', row1=row+7, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gimbal_roll', label1_text='Gimbal roll: ', row1=row+8, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gimbal_pitch', label1_text='Gimbal pitch: ', row1=row+9, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'gimbal_yaw', label1_text='Gimbal yaw: ', row1=row+10, column1=col)

		row, col = 5, 5
		self.GUI_init_2labels(self.HUD_frame, 'ch1', label1_text='Ch1: ', row1=row+0, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch2', label1_text='Ch2: ', row1=row+1, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch3', label1_text='Ch3: ', row1=row+2, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch4', label1_text='Ch4: ', row1=row+3, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch5', label1_text='Ch5: ', row1=row+4, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch6', label1_text='Ch6: ', row1=row+5, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch7', label1_text='Ch7: ', row1=row+6, column1=col)
		self.GUI_init_2labels(self.HUD_frame, 'ch8', label1_text='Ch8: ', row1=row+7, column1=col)

		self.HUD_frame.grid(row=frame_row, column=frame_column)



	def init_firmware_frame(self, frame_row, frame_column):
		self.firmware_frame = tk.Frame(self.root)
		self.firmware_frame.configure(background='black')
		
		self.GUI_init_2labels(self.firmware_frame, 'firmware_ver', label1_text='Firmware: ', row1=18, column1=1)
		#self.GUI_init_2labels(self.firmware_frame, 'firmware_ver_major', label1_text='Firmware major: ', row1=19, column1=1)
		#self.GUI_init_2labels(self.firmware_frame, 'firmware_ver_minor', label1_text='Firmware minor: ', row1=20, column1=1)
		#self.GUI_init_2labels(self.firmware_frame, 'firmware_ver_patch', label1_text='Firmware patch: ', row1=21, column1=1)
		self.GUI_init_2labels(self.firmware_frame, 'firmware_ver_release_type', label1_text='Release type: ', row1=22, column1=1)
		#self.GUI_init_2labels(self.firmware_frame, 'firmware_ver_release_ver', label1_text='Realease version: ', row1=23, column1=1)
		self.GUI_init_2labels(self.firmware_frame, 'firmware_ver_release_stable', label1_text='Release stable?: ', row1=24, column1=1)		
		#self.firmware_frame.grid(row=frame_row, column=frame_column)



	def init_test_frame(self, frame_row, frame_column):
		self.test_frame = tk.Frame(self.root)
		self.test_frame.configure(background='white')

		self.lbl_test_frame = tk.Label(self.test_frame, text='Test frame', font=('arial', 12, 'bold'), fg='red',bg='white')
		self.lbl_test_frame.grid(row=0, column=0, columnspan=1)

		self.btn_test1 = tk.Button(self.test_frame, fg='black', text='Test 1', command= self.on_btn_test1)
		self.btn_test1.grid(row=1, column=0, columnspan=1)

		self.btn_test2 = tk.Button(self.test_frame, fg='black', text='Test 2', command= self.on_btn_test2)
		self.btn_test2.grid(row=2, column=0, columnspan=1)

		self.btn_test3 = tk.Button(self.test_frame, fg='black', text='Test 3', command= self.on_btn_test3)
		self.btn_test3.grid(row=3, column=0, columnspan=1)
		#self.test_frame.grid(row=frame_row, column=frame_column)

	def on_btn_test1(self):
		self.GCS.UDP_client.send_cmd(['override'])

	def on_btn_test2(self):
		self.GCS.UDP_client.send_cmd(['release_override'])

	def on_btn_test3(self):
		self.prnt("GCS", "Test 3")



	def init_mission_frame(self, frame_row, frame_column):
		self.mission_frame = tk.Frame(self.root)
		self.mission_frame.configure(background='white')


		self.lbl_mission_frame = tk.Label(self.mission_frame, text='Mission flow:', font=('arial', 12, 'bold'), fg='red',bg='white')
		self.lbl_mission_frame.grid(row=0, column=0, columnspan=4)

		self.lbl_mission1 = tk.Label(self.mission_frame, text='(1) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission1.grid(row=1, column=0, columnspan=1)
		self.btn_mission1 = tk.Button(self.mission_frame, fg='black', text='Arm', width=20, command= self.on_btn_mission1)
		self.btn_mission1.grid(row=1, column=1, columnspan=1)

		self.lbl_mission2 = tk.Label(self.mission_frame, text='(2) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission2.grid(row=2, column=0, columnspan=1)
		self.btn_mission2 = tk.Button(self.mission_frame, fg='black', text='Guided Takeoff, Stay on alt:', width=20, command= self.on_btn_mission2)
		self.btn_mission2.grid(row=2, column=1, columnspan=1)
		self.ent_mission2 = tk.Entry(self.mission_frame)
		self.ent_mission2.insert(0, "3")
		self.ent_mission2.grid(row=2, column=2)
		self.btn_mission2_1 = tk.Button(self.mission_frame, fg='black', text='GUIDED, move_0', width=20, command= self.on_btn_mission2_1)
		self.btn_mission2_1.grid(row=2, column=3, columnspan=1)

		self.lbl_mission3 = tk.Label(self.mission_frame, text='(3) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission3.grid(row=3, column=0, columnspan=1)
		self.btn_mission3 = tk.Button(self.mission_frame, fg='black', text='Listen to WASD keys', width=20, command= self.on_btn_mission3)
		self.btn_mission3.grid(row=3, column=1, columnspan=1)

		self.lbl_mission4 = tk.Label(self.mission_frame, text='(4) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission4.grid(row=4, column=0, columnspan=1)


		self.lbl_mission5 = tk.Label(self.mission_frame, text='(5) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission5.grid(row=5, column=0, columnspan=1)
		self.btn_mission5 = tk.Button(self.mission_frame, fg='black', text='Fly! :)', width=20, command= self.on_btn_mission5)
		self.btn_mission5.grid(row=5, column=1, columnspan=1)

		self.lbl_mission6 = tk.Label(self.mission_frame, text='(6) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission6.grid(row=6, column=0, columnspan=1)
		self.btn_mission6 = tk.Button(self.mission_frame, fg='black', text='LAND', width=20, command= self.on_btn_mission6)
		self.btn_mission6.grid(row=6, column=1, columnspan=1)

		self.btn_mission6_1 = tk.Button(self.mission_frame, fg='black', text='POSHOLD', width=20, command= self.on_btn_mission6_1)
		self.btn_mission6_1.grid(row=6, column=2, columnspan=1)

		self.btn_mission6_2 = tk.Button(self.mission_frame, fg='black', text='LOITER', width=20, command= self.on_btn_mission6_2)
		self.btn_mission6_2.grid(row=6, column=3, columnspan=1)

		self.lbl_mission7 = tk.Label(self.mission_frame, text='(7) ', font=('arial', 10), fg='black',bg='white')
		self.lbl_mission7.grid(row=7, column=0, columnspan=1)
		self.btn_mission7 = tk.Button(self.mission_frame, fg='black', text='Disarm', width=20, command= self.on_btn_mission7)
		self.btn_mission7.grid(row=7, column=1, columnspan=1)


	def on_btn_mission1(self):
		self.prnt("Mission", "Arm")
		self.GCS.UDP_client.send_cmd(['arm'])

	def on_btn_mission2(self):
		altitude = self.ent_mission2.get()	
		self.prnt("Mission", "Takeoff to " + str(altitude) + " meters")
		self.GCS.UDP_client.send_cmd(['takeoff', int(altitude)])

	def on_btn_mission2_1(self):
		self.prnt("Mission","GUIDED, move_0")
		self.GCS.UDP_client.send_cmd(['guided'])
		if self.lbl_send_position.cget('bg') == "red":
			self.send_move_0 = 1
			self.lbl_send_position.config(text = "YES", bg='green3')

	def on_btn_mission3(self):
		self.prnt("Mission", "Listen to WASD keys")
		if self.lbl_listen_keys.cget('bg') == "red":
			self.root.bind("<Key>", self.key_callback)
			self.root.bind("<KeyRelease>", self.key_release_callback)
			self.lbl_listen_keys.config(text = "YES", bg='green3')

#TODO terminal to label
#TODO simulte panic triger from GCS / GCS.close_all in droneside
#TODO finish mission flow

	def on_btn_mission5(self):
		self.prnt("Mission", "Fly! :)")

	def on_btn_mission6(self):
		self.prnt("Mission", "LAND mode")
		self.GCS.UDP_client.send_cmd(['land'])

	def on_btn_mission6_1(self):
		self.prnt("Mission", "POSHOLD mode")
		self.GCS.UDP_client.send_cmd(['poshold'])

	def on_btn_mission6_2(self):
		self.prnt("Mission", "LOITER mode")
		self.GCS.UDP_client.send_cmd(['loiter'])

	def on_btn_mission7(self):
		self.prnt("Mission", "Disarm")
		self.GCS.UDP_client.send_cmd(['disarm'])


	def on_window_close(self):
		self.prnt("Mission", "Close all - GUI window close")
		self.GCS.close_all()

	def GUI_init_2labels(self, frame, key, label1_text, row1 ,column1):
		row2 = row1
		column2= column1 + 1
		lbl_name = tk.Label(frame, text=label1_text, font=('arial', 10, 'bold'), fg='green', bg='black')
		lbl_val = tk.Label(frame, font=('arial', 10, 'bold'), fg='green', bg='black')
		self.GCS.val_dict[key] = {'lbl_name': lbl_name, 'lbl_val': lbl_val, 'value': None}
		self.GCS.val_dict[key]['lbl_name'].grid(row=row1, column=column1, columnspan=1)
		self.GCS.val_dict[key]['lbl_val'].grid(row=row2, column=column2, columnspan=1)

	def GUI_init_dummy_label(self, frame, row, column):
		lbl_name = tk.Label(frame, text='',font=('arial', 10, 'bold'), fg='green',bg='black')
		lbl_name.grid(row=row, column=column, columnspan=1)


	def key_release_callback(self, event):
		#self.key_pressed = None
		pass

	def key_callback(self, event):
		#print repr(event.char)	+ "Pressed"
		if (event.char=='p'):
			self.GCS.UDP_client.send_cmd(['arm', int(10)])
		if (event.char=='w'):
			self.key_pressed = event.char
		elif (event.char=='a'):
			self.key_pressed = event.char
		elif (event.char=='s'):
			self.key_pressed = event.char
		elif (event.char=='d'):
			self.key_pressed = event.char
		elif (event.char=='z'):
			self.key_pressed = event.char
		elif (event.char=='x'):
			self.key_pressed = event.char
		elif (event.char=='q'):
			self.GCS.UDP_client.send_cmd(['yaw_left', int(10)])
		elif (event.char=='e'):
			self.GCS.UDP_client.send_cmd(['yaw_right', int(10)])
		elif (event.char=='l'):
			self.GCS.UDP_client.send_cmd(['land'])
		#elif (event.char=='t'):
		#	self.GCS.UDP_client.send_cmd(['triangle'])
		#elif (event.char=='y'):
		#	self.GCS.UDP_client.send_cmd(['triangle2'])
		#elif (event.char=='u'):
		#	self.GCS.UDP_client.send_cmd(['square'])
		#elif (event.char=='i'):
		#	self.GCS.UDP_client.send_cmd(['square2'])
		#elif (event.char=='h'):
		#	self.GCS.UDP_client.send_cmd(['diamond'])

	def GUI_close(self):
		self.root.destroy()
		self.root.quit()

	def GUI_tick(self):
		if (self.key_pressed == 'w'):
			self.GCS.UDP_client.send_cmd(['forward', int(1)])
		elif (self.key_pressed == 'a'):
			self.GCS.UDP_client.send_cmd(['left', int(1)])
		elif (self.key_pressed == 's'):
			self.GCS.UDP_client.send_cmd(['backward', int(1)])
		elif (self.key_pressed == 'd'):
			self.GCS.UDP_client.send_cmd(['right', int(1)])
		elif (self.key_pressed == 'z'):
			self.GCS.UDP_client.send_cmd(['up', int(1)])
		elif (self.key_pressed == 'x'):
			self.GCS.UDP_client.send_cmd(['down', int(1)])
		elif (self.key_pressed == None):
			#print "None pressed"
			if (self.send_move_0 == 1):
				self.GCS.UDP_client.send_cmd(['move_0'])
		else:
			self.prnt("Drone", "WTF am I doing here?")
		# zero the pressed key. It will be renewed when auto press will be activated
		self.key_pressed = None
		
		self.GUI_dict_refresh_values()
		self.root.after(100, self.GUI_tick)

	# Update the stored value in the dict with the new ones    
	def GUI_dict_generate_new_values(self):
		for key, val in self.GCS.val_dict.iteritems():
			if val['value'] == None:
				val['value'] = 0
			val['value'] += random.randint(1,5)

	# Update label value with stored value in dict    
	def GUI_dict_refresh_values(self):
		for key, val in self.GCS.val_dict.iteritems():
			val['lbl_val'].config(text=str(val['value']))
			#GCS.val_dict['roll']['lbl_val'].config(text=str(GCS.val_dict['roll']['value']))


class GCS():
	def __init__(self):
		try:
			self.GUI = None
			#global dict : {'val_X', {'lbl_name': <label>, 'lbl_val': <label>, 'value': <value>}}
			self.val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'frame_loc_north', 'frame_loc_east', 'frame_loc_down', 'frame_gl_lat', 'frame_gl_lon', 'frame_gl_alt', 'frame_gl_rel_lat', 'frame_gl_rel_lon', 'frame_gl_rel_alt', 'battery', 'last_heartbeat', 'gps_0_HDOP', 'gps_0_VDOP', 'gps_0_fix', 'gps_0_satellites', 'ekf_ok', 'mode', 'armed', 'system_status', 'is_armable_on_demand'])
			# Init all val_dict fields
			self.dict_init_fields()

			self.parser = argparse.ArgumentParser(description='GCS module')
			self.parser.add_argument('--drone_ip')
			self.args = self.parser.parse_args()
			if not self.args.drone_ip:
				self.drone_ip = "255.255.255.255"
			else:
				self.drone_ip = self.args.drone_ip
			self.prnt("GSC", "Open socket for Telemetry and user commands")
			self.UDP_client = UDP.UDP(0, "Telem/Cmd", "0.0.0.0", 6000, self.drone_ip, 5001)
			self.prnt("GSC", "Open socket for drone Report")
			self.UDP_client_Report = UDP.UDP(0, "Drone Report", "0.0.0.0", 6100, self.drone_ip, 5101)
			
			self.prnt("GSC", "Start receive Telem thread")
			self.UDP_client.receive_loop_telem_thread(self.val_dict)
			self.prnt("GSC", "Start receive Report thread")
			self.UDP_client_Report.receive_loop_report_thread()
	
			self.run_GUI()

		except KeyboardInterrupt:
			self.prnt("GSC", "Close all - keyboard interrupt in main")
			self.close_all()

	def prnt(self, module, msg):
		print datetime.datetime.utcnow().strftime('%H:%M:%S.%f') + ": <" + str(module) + "> " + str(msg)

	def dict_init_fields(self):
		for key, val in self.val_dict.iteritems():
			self.val_dict[key] = dict.fromkeys(['value', 'lbl_val', 'lbl_name'])

	def run_GUI(self):
		self.root = tk.Tk()
		self.GUI = GUI_main(self)
		try:
			self.prnt("GSC", "GUI - Enter the mainloop")
			self.root.mainloop()
		except(KeyboardInterrupt , SystemExit):
			self.prnt("GSC", "Close all - keyboard interrupt in GUI/console")
			self.close_all()

	def close_all(self):
	
		self.prnt("GSC", "Close all - Telemetry/commands")
		self.UDP_client.close_UDP()
		self.prnt("GSC", "Close all - Drone Report")
		self.UDP_client_Report.close_UDP()
	
		self.prnt("GSC", "Close all - GUI")
		self.GUI.GUI_close()

		self.prnt("GSC", "Close all - Complete")


if __name__ == "__main__":
		GCS = GCS()
else:
	print("You are running me not as a main?")
