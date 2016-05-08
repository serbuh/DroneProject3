from dronekit import connect, VehicleMode
import time
import socket
import time
import argparse


HOST = '192.168.150.1'
PORT_TELEM = 3334

socket_telem = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def connect2FCU():
	#Set up option parsing to get connection string	
	parser = argparse.ArgumentParser(description='HUD module')
	parser.add_argument('--connect', help="E.g. /dev/ttyACM0 or /dev/ttyUSB0,57600")
	args = parser.parse_args()
	connection_string = args.connect
	if not args.connect:
    		print "Please specify the connect string"

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
	return vehicle

def wildcard_callback(self, attr_name, value):
	#print "(%s): %s" % (attr_name,value)
	global socket_telem
	if attr_name=="attitude":
		data = "Roll: {} Pitch: {} Yaw: {}".format(round(value.roll,2), round(value.pitch,2), round(value.yaw,2))
		print "SENT: " + data
		socket_telem.sendto(data,(HOST,PORT_TELEM))
		pass

	elif attr_name=="velocity":
		#print "Vx, Vy, Vz = {} {} {}".format(value[0], value[1], value[2])
		pass

	elif attr_name=="rangefinder":
		#print "Lidar {}".format(round(value.distance,2))
		pass

	elif attr_name=="location.global_relative_frame":
		#print "global_relative_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		pass

	elif attr_name=="location.global_frame":
		#print "location.global_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		pass

	elif attr_name=="location.local_frame":
		#print "location.local_frame lat, lon, alt = {} {} {}".format(value.lat, value.lon, value.alt)
		pass

	elif attr_name=="location":
		#print "location_wtf {}".format(dir(value))
		#print "location_wtf {}".format(value)
		pass

	elif attr_name=="heading":
		#print "Heading: {}".format(value)
		pass
	
	elif attr_name=="airspeed":
		#print "Airspeed: {}".format(value)
		pass

	elif attr_name=="groundspeed":
		#print "Groundspeed: {}".format(value)
		pass

	elif attr_name=="channels":		
		#print "channels 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}".format(value['1'], value['2'], value['3'], value['4'], value['5'], value['6'], value['7'], value['8'], )
		pass

	elif attr_name=="last_heartbeat":
		#print "last_heartbeat: {}".format(round(value,2))		
		pass

	elif attr_name=="gimbal":
		#print "Gimbal. pitch: {} roll: {} yaw:{}".format(value.pitch, value.roll, value.yaw)
		pass

	elif attr_name=="battery":
		#print "Battery: {}".format(value.voltage)
		pass
	#TODO: is_armable, system_status, armed, mode
	elif attr_name=="is_armable":
		#print "is_armable: {}".format(value)
		#print "is_armable: {}".format(dir(value))
		pass


if __name__ == "__main__":
	print "Connect to FCU"
	connect2FCU()
