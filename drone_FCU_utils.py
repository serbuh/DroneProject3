from dronekit import connect, VehicleMode
import time
import socket
import time
import argparse
import json

def send_telem(data_dict):
	data_json = json.dumps(data_dict)
	print "SENDING: " + data_json
	socket_telem.sendto(data_json, (HOST,PORT_TELEM))

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
	#vehicle.wait_ready('autopilot_version')
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
		data = {'lidar': round(value.distance,2)}

	elif attr_name=="location.global_relative_frame":
		#print "global_relative_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		data = {'lat_gl_rel': value.lat, 'lon_gl_rel': value.lon, 'alt_gl_rel': value.alt}

	elif attr_name=="location.global_frame":
		#print "location.global_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		data = {'lat_gl': value.lat, 'lon_gl': value.lon, 'alt_gl': value.alt}

	elif attr_name=="location.local_frame":
		#print "location.local_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		data = {'lat_loc': value.lat, 'lon_loc': value.lon, 'alt_loc': value.alt}

	elif attr_name=="location":
		#print "location_wtf {}".format(dir(value))
		#print "location_wtf {}".format(value)
		pass

	elif attr_name=="heading":
		#print "Heading: {}".format(value)
		data = {'heading': value}
	
	elif attr_name=="airspeed":
		#print "Airspeed: {}".format(value)
		data = {'airspeed': value}

	elif attr_name=="groundspeed":
		#print "Groundspeed: {}".format(value)
		data = {'groundspeed': value}

	elif attr_name=="channels":		
		#print "channels 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}".format(value['1'], value['2'], value['3'], value['4'], value['5'], value['6'], value['7'], value['8'], )
		data = {'ch1': value[1], 'ch2': value[2], 'ch3': value[3], 'ch4': value[4], 'ch5': value[5], 'ch6': value[6], 'ch7': value[7], 'ch8': value[8]}

	elif attr_name=="last_heartbeat":
		#print "last_heartbeat: {}".format(round(value,2))		
		data = {'last_heartbeat': round(value,2)}

	elif attr_name=="gimbal":
		#print "Gimbal. pitch: {} roll: {} yaw:{}".format(value.pitch, value.roll, value.yaw)
		data = {'gimbal_roll': value.roll, 'gimbal_pitch': value.pitch, 'gimbal_yaw': value.yaw}

	elif attr_name=="battery":
		#print "Battery: {}".format(value.voltage)
		data = {'battery': value.voltage}

	#TODO: is_armable, system_status, armed, mode
	elif attr_name=="is_armable":
		#print "is_armable: {}".format(value)
		#print "is_armable: {}".format(dir(value))
		pass

	if data:
		send_telem(data)

def close(vehicle,sitl):
	#Close vehicle object before exiting script
	print "\n### Closing vehicle object ###"
	vehicle.close()

	# Shut down simulator if it was started.
	print("### Closing SITL ###")	
	if sitl is not None:
    		sitl.stop()
	print("### Close Complete ###")

if __name__ == "__main__":
	try:
		#PORT_VIDEO = 3333
		PORT_TELEM = 3334

		#socket_video = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		socket_telem = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

		HOST = 'localhost'
		#HOST = '192.168.150.1'
		print "Connect to FCU from drone_FCU_utils.py"
		vehicle, sitl = connect2FCU()
		vehicle.add_attribute_listener('*', wildcard_callback)
		while(1):
			time.sleep(1)
	except KeyboardInterrupt:
		close(vehicle,sitl)	
else:
	print("You are running drone_FCU_utils.py not as a main?")

