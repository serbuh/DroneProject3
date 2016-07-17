from dronekit import connect, VehicleMode
import time
import socket
import time
import argparse
import json
import drone_controll
import Tkinter as tk

def send_telem(data_dict):	
	data_str = str(data_dict)
	#print "SENDING: " + data_str
	socket_telem.sendto(data_str, (HOST,PORT_TELEM))
	
def connect2FCU():
	#Set up option parsing to get connection string	
	parser = argparse.ArgumentParser(description='HUD module')
	parser.add_argument('--connect', help="E.g. /dev/ttyACM0 or /dev/ttyUSB0,57600")
	args = parser.parse_args()
	connection_string = args.connect
	sitl=None
	if not args.connect:
    		print "The connect string was not specified. Running SITL!"
		from dronekit_sitl import SITL
		sitl = SITL()
		sitl.download('copter', '3.3', verbose=True)
		sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
		sitl.launch(sitl_args, await_ready=True, restart=True)
		connection_string = 'tcp:127.0.0.1:5760'

	# Connect to the Vehicle. 
	#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
	print "\nConnecting to vehicle on: %s" % connection_string
	vehicle = connect(connection_string, wait_ready=True)
	vehicle.wait_ready('autopilot_version')
	# Get all vehicle attributes (state)
	print "======================================================="
	print "\nGet all vehicle attribute values:"
	print " Autopilot Firmware version: %s" % vehicle.version
	print "   Major version number: %s" % vehicle.version.major
	print "   Minor version number: %s" % vehicle.version.minor
	print "   Patch version number: %s" % vehicle.version.patch
	print "   Release type: %s" % vehicle.version.release_type()
	print "   Release version: %s" % vehicle.version.release_version()
	print "   Stable release?: %s" % vehicle.version.is_stable()
	print " Autopilot capabilities"
	print "   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float
	print "   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float
	print "   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int
	print "   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int
	print "   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union
	print "   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp
	print "   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target
	print "   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned
	print "   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int
	print "   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain
	print "   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target
	print "   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination
	print "   Supports mission_float message type: %s" % vehicle.capabilities.mission_float
	print "   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration
	print " Global Location: %s" % vehicle.location.global_frame
	print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
	print " Local Location: %s" % vehicle.location.local_frame
	print " Attitude: %s" % vehicle.attitude
	print " Velocity: %s" % vehicle.velocity
	print " GPS: %s" % vehicle.gps_0
	print " Gimbal status: %s" % vehicle.gimbal
	print " Battery: %s" % vehicle.battery
	print " EKF OK?: %s" % vehicle.ekf_ok
	print " Last Heartbeat: %s" % vehicle.last_heartbeat
	print " Rangefinder: %s" % vehicle.rangefinder
	print " Rangefinder distance: %s" % vehicle.rangefinder.distance
	print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
	print " Heading: %s" % vehicle.heading
	print " Is Armable?: %s" % vehicle.is_armable
	print " System status: %s" % vehicle.system_status.state
	print " Groundspeed: %s" % vehicle.groundspeed    # settable
	print " Airspeed: %s" % vehicle.airspeed    # settable
	print " Mode: %s" % vehicle.mode.name    # settable
	print " Armed: %s" % vehicle.armed    # settable
	print "======================================================="
	return vehicle, sitl

########### Telem ###########

def wildcard_callback(self, attr_name, value):
	#print "(%s): %s" % (attr_name,value)
	global socket_telem
	data = None
	if attr_name=="attitude":
		#print"roll, pitch, yaw = {} {} {}".format(round(value.roll,2),round(value.pitch,2),round(value.yaw,2))
		data = {'roll': round(value.roll,2), 'pitch': round(value.pitch,2), 'yaw': round(value.yaw,2)}
	
	elif attr_name=="velocity":
		#print "Vx, Vy, Vz = {} {} {}".format(value[0], value[1], value[2])
		data = {'vx': value[0], 'vy': value[1], 'vz': value[2]}

	elif attr_name=="rangefinder":
		#print "Lidar {}".format(round(value.distance,2))
		data = {'rangefinder': round(value.distance,2)}

	elif attr_name=="location.global_relative_frame":
		#print "location.global_relative_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		data = {'frame_gl_rel_lat': value.lat, 'frame_gl_rel_lon': value.lon, 'frame_gl_rel_alt': value.alt}

	elif attr_name=="location.global_frame":
		#print "location.global_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		data = {'frame_gl_lat': value.lat, 'frame_gl_lon': value.lon, 'frame_gl_alt': value.alt}

	elif attr_name=="location.local_frame":
		#print "location.local_frame north, east, down = {} {} {}".format(value.north, value.east, value.down)
		data = {'frame_loc_north': round(value.north,3), 'frame_loc_east': round(value.east,3), 'frame_loc_down': round(value.down,3)}

	elif attr_name=="location":
		#print "location_all {}".format(dir(value))
		#print "location_all {}".format(value)
		pass

	elif attr_name=="heading":
		#print "Heading: {}".format(value)
		data = {'heading': value}
	
	elif attr_name=="airspeed":
		#print "Airspeed: {}".format(value)
		data = {'airspeed': round(value,3)}

	elif attr_name=="groundspeed":
		#print "Groundspeed: {}".format(value)
		data = {'groundspeed': round(value,3)}

	elif attr_name=="channels":		
		#print "Channels. 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}".format(value['1'], value['2'], value['3'], value['4'], value['5'], value['6'], value['7'], value['8'], )
		data = {'ch1': value[1], 'ch2': value[2], 'ch3': value[3], 'ch4': value[4], 'ch5': value[5], 'ch6': value[6], 'ch7': value[7], 'ch8': value[8]}

	elif attr_name=="last_heartbeat":
		#print "last_heartbeat: {}".format(round(value,2))		
		data = {'last_heartbeat': round(value,2)}

	elif attr_name=="gimbal":
		#print "Gimbal. pitch: {} roll: {} yaw:{}".format(value.pitch, value.roll, value.yaw)
		data = {'gimbal_roll': value.roll, 'gimbal_pitch': value.pitch, 'gimbal_yaw': value.yaw}

	elif attr_name=="battery":
		#print "Battery. {}".format(value.voltage)
		data = {'battery': value.voltage}

	elif attr_name=="gps_0":
		#print "gps_0. eph: {} epv: {} fix_type: {} satellites_visible: {}".format(value.eph, value.epv, value.fix_type, value.satellites_visible)
		data = {'gps_0_HDOP': value.eph, 'gps_0_VDOP': value.epv, 'gps_0_fix': value.fix_type, 'gps_0_satellites': value.satellites_visible}

	elif attr_name=="ekf_ok":
		#print "ekf_ok: {}".format(value)
		data = {'ekf_ok': value}

	elif attr_name=="mount":
		#method is replaced by gimbal
		#print "mount: {}".format(value)
		pass

	elif attr_name=="mode":		
		#print "mode: {}".format(value.name)
		data = {'mode': value.name}

	elif attr_name=="armed":		
		#print "armed: {}".format(value)
		data = {'armed': str(value)}

	elif attr_name=="is_armable":
		#print "is_armable: {}".format(value)
		print "is_armable: {}".format(dir(value))

	elif attr_name=="system_status":
		#print "System status {}".format(value.state)
		data = {'system_status': value.state}
	else:
		print "### NOT SENT:" + attr_name
	if data:
		send_telem(data)
	
########### Telem end ############



############# GUI #################

class GUI_main(tk.Frame):
	def __init__(self, root, vehicle, sitl, vehicle_controll, *args, **kwargs):
		self.vehicle = vehicle
		self.sitl = sitl
		self.vehicle_controll = vehicle_controll		
		print "Drone: GUI - Start"
		tk.Frame.__init__(self, root, *args, **kwargs)
		self.root = root
		self.frame1 = tk.Frame(self.root)
		self.root.title("drone GUI")
		self.frame1.configure(background='white')
		self.GUI_init(self.frame1)
		self.frame1.grid(row=0, column=0)
		self.root.after(0,self.drone_GUI_tick)

	def GUI_init(self, frame):
		print "Drone: GUI - Init objects"
		self.root.protocol('WM_DELETE_WINDOW', self.on_window_close)		
		#0
		self.lbl_title = tk.Label(frame, text='Mission controllsky' ,font=('arial', 16, 'bold'), fg='red',bg='white')
		self.lbl_title.grid(row=0, column=0, columnspan=6)
		self.btn_stop = tk.Button(frame, text='Stop', width=25, command= self.on_btn_stop)
		self.btn_stop.grid(row=0, column=6, columnspan=1)
		#1
		self.lbl_command = tk.Label(frame, text='Command:', fg='black',bg='white')
		self.lbl_command.grid(row=1, column=0, columnspan=1)
		self.ent_command = tk.Entry(frame)
		self.ent_command.grid(row=1, column=1)
		self.lbl_command_param1 = tk.Label(frame, text='param1:', fg='black',bg='white')
		self.lbl_command_param1.grid(row=1, column=2, columnspan=1)
		self.ent_command_param1 = tk.Entry(frame)
		self.ent_command_param1.grid(row=1, column=3)
		self.lbl_command_param2 = tk.Label(frame, text='param2:', fg='black',bg='white')
		self.lbl_command_param2.grid(row=1, column=4, columnspan=1)
		self.ent_command_param2 = tk.Entry(frame)
		self.ent_command_param2.grid(row=1, column=5)
		self.btn_send = tk.Button(frame, text='Send command', command=self.on_btn_send)
		self.btn_send.grid(row=1, column=6, columnspan=1)
		#2
		self.lbl_sent = tk.Label(frame, fg='black', bg='white', text='')
		self.lbl_sent.grid(row=2, column=0, columnspan=1)
		#3
		self.btn_listen_keys = tk.Button(frame, text='Listen for keys', width=25, command= self.on_btn_listen_keys)
		self.btn_listen_keys.grid(row=3, column=0, columnspan=1)
		self.lbl_listen_keys = tk.Label(frame, fg='black', bg='red', text='Listen keys - NO')
		self.lbl_listen_keys.grid(row=3, column=1, columnspan=1)
		#4

		#self.root.bind("<Key>", self.key_callback)
		self.counter = 0

	def on_btn_send(self):
		command = self.ent_command.get()
		command_param1 = self.ent_command_param1.get()
		command_param2 = self.ent_command_param2.get()
		sent_command = "Sending: {" + command + " " + command_param1 + " " + command_param2 +"}"
		self.lbl_sent.config(text = sent_command)
		self.vehicle_controll.send_command(command, command_param1, command_param2)

	def on_window_close(self):
		print "Drone: Close all - GUI window close"
		close_all(self.vehicle,self.sitl,self)

	def on_btn_stop(self):
		print "Drone: Close all - GUI button Stop"
		close_all(self.vehicle,self.sitl,self)

	def on_btn_listen_keys(self):
		if self.lbl_listen_keys.cget('bg') == "green":
			self.root.unbind("<Key>")
			self.lbl_listen_keys.config(text = "Listen keys - NO", bg='red')
		elif self.lbl_listen_keys.cget('bg') == "red":
			self.root.bind("<Key>", self.key_callback)
			self.lbl_listen_keys.config(text = "Listen keys - YES", bg='green')

	def drone_GUI_close(self):
		self.root.destroy()
		self.root.quit()

	def drone_GUI_tick(self):
		self.root.after(200, self.drone_GUI_tick)

	def key_callback(self, event):
		if vehicle_controll is None:
			print "Drone: GUI - Warning: vehicle controll is None. Run telem module first."
			print "Drone: GUI - ", repr(event.char), " pressed"
			return

		#print "pressed", repr(event.char)
		if (event.char=='z'):
			print "Z pressed"
			self.vehicle_controll.send_command("arm", 10)
		if (event.char=='w'):
			print "W pressed"
			self.vehicle_controll.send_command("forward", 20, 1)
		elif (event.char=='a'):
			print "A pressed"
			self.vehicle_controll.send_command("left", 20, 1)
		elif (event.char=='s'):
			print "S pressed"
			self.vehicle_controll.send_command("backward", 20, 1)
		elif (event.char=='d'):
			print "D pressed"
			self.vehicle_controll.send_command("right", 20, 1)
		elif (event.char=='q'):
			print "Q pressed"
			self.vehicle_controll.send_command("yaw_left", 10)
		elif (event.char=='e'):
			print "E pressed"
			self.vehicle_controll.send_command("yaw_right", 10)
		elif (event.char=='l'):
			print "L pressed"
			self.vehicle_controll.send_command("land", None)
		elif (event.char=='t'):
			print "T pressed"
			self.vehicle_controll.send_command("triangle", None)
		elif (event.char=='y'):
			print "Y pressed"
			self.vehicle_controll.send_command("triangle2", None)
		elif (event.char=='u'):
			print "U pressed"
			self.vehicle_controll.send_command("square", None)
		elif (event.char=='i'):
			print "I pressed"
			self.vehicle_controll.send_command("square2", None)
		elif (event.char=='p'):
			print "P pressed"
			self.vehicle_controll.send_command("diamond", None)

######## GUI stuff end ########

def run_GUI(vehicle, sitl, vehicle_controll):
	root = tk.Tk()
	GUI = GUI_main(root,vehicle,sitl,vehicle_controll)
	try:
		print "Drone: GUI - Enter the mainloop"
		root.mainloop()
	except(KeyboardInterrupt):
		print "Drone: Close all - keyboard interrupt in GUI"
		close_all(vehicle,sitl,GUI)

def close_all(vehicle,sitl,GUI):
	
	if sitl is not None:
		print("Drone: Close all - SITL")
    		sitl.stop()

	if telem_enabled:
		print("Drone: Close all - Vehicle object")
		vehicle.close()

	if GUI_enabled:
		print("Drone: Close all - GUI")
		GUI.drone_GUI_close()

	print "Drone: Close all - Complete"

if __name__ == "__main__":
	try:
		GUI_enabled = 1
		telem_enabled = 1

		vehicle = None
		sitl = None
		GUI = None
		vehicle_controll = None

		if (telem_enabled != 0) :
			PORT_TELEM = 3334		
			socket_telem = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			HOST = 'localhost'
			#HOST = '192.168.150.1'
			print "Connect to FCU"
			vehicle, sitl = connect2FCU()
			print "Start to listen and SEND!"
			vehicle.add_attribute_listener('*', wildcard_callback)
			vehicle_controll = drone_controll.vehicle_controll(vehicle)

		if (GUI_enabled != 0) :
			run_GUI(vehicle, sitl, vehicle_controll)
		else:
			# if GUI disabled - here is the inf. loop
			while(1):
				time.sleep(1)		
	except KeyboardInterrupt:
		print "Drone: Close all - keyboard interrupt in main"		
		close_all(vehicle,sitl,GUI)	
else:
	print("You are running me not as a main?")

