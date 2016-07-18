"""
adapted from DroneKit example guided_set_speed_yaw.py
Example documentation: http://python.dronekit.io/examples/guided-set-speed-yaw-demo.html
"""

from dronekit import VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import math
import time
import sys, traceback

class vehicle_controll:
	vehicle = None
	
	DURATION = 1 #Set duration for each segment.

	#Set up velocity vector to map to each direction.
	# vx > 0 => fly North
	# vx < 0 => fly South
	NORTH = 1
	SOUTH = -1

	# Note for vy:
	# vy > 0 => fly East
	# vy < 0 => fly West
	EAST = 1
	WEST = -1

	# Note for vz: 
	# vz < 0 => ascend
	# vz > 0 => descend
	UP = -0.5
	DOWN = 0.5

	def __init__(self, vehicle):
		self.vehicle = vehicle
		print("Set airspeed to 2m/s, (10m/s max).")
		self.vehicle.airspeed = 2
		print("Set groundspeed to 2m/s, (15m/s max).")
		self.vehicle.groundspeed = 2
		
	"""
	The example is completing. LAND at current location.
	"""

	def send_command(self, *args):
		if args[0] == "arm":
			self.arm_and_takeoff(int(args[1]))
		elif args[0] == "land":
			self.land_here()
		elif args[0] == "forward":
			self.move_forward(int(args[1]), int(args[2]))
		elif args[0] == "backward":
			self.move_backward(int(args[1]), int(args[2]))
		elif args[0] == "left":
			self.move_left(int(args[1]), int(args[2]))
		elif args[0] == "right":
			self.move_right(int(args[1]), int(args[2]))

		elif args[0] == "forward_once":
			self.move_forward_once(int(args[1]))
		elif args[0] == "backward_once":
			self.move_backward_once(int(args[1]))
		elif args[0] == "left_once":
			self.move_left_once(int(args[1]))
		elif args[0] == "right_once":
			self.move_right_once(int(args[1]))
		elif args[0] == "move_0_once":
			self.move_0_once()

		elif args[0] == "yaw_left":
			self.yaw_left(int(args[1]))
		elif args[0] == "yaw_right":
			self.yaw_right(int(args[1]))
		elif args[0] == "triangle":
			self.triangle()
		elif args[0] == "triangle2":
			self.triangle2()
		elif args[0] == "square":
			self.square()
		elif args[0] == "square2":
			self.square2()
		elif args[0] == "diamond":
			self.diamond()
		else:
			print "Drone: drone controll - Warning: command " + str(args[0]) + " does not exist!"


	def arm_and_takeoff(self, aTargetAltitude):
		print "Drone: drone controll - Arm: arm and takeoff to " + str(aTargetAltitude) + " meters"
		print "Drone: drone controll - Arm: Basic pre-arm checks"
		# Don't let the user try to arm until autopilot is ready
		while not self.vehicle.is_armable:
			print "Drone: drone controll - Arm: Waiting for vehicle to initialise..."
			time.sleep(1)

		print "Drone: drone controll - Arm: Arming motors"
		# Copter should arm in GUIDED mode
		self.vehicle.mode = VehicleMode("GUIDED")
		self.vehicle.armed = True

		while not self.vehicle.armed:      
			print "Drone: drone controll - Arm: Waiting for arming..."
			time.sleep(1)

		print "Drone: drone controll - Arm: Taking off!"
		self.vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

		# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
		#  after Vehicle.simple_takeoff will execute immediately).
		while True:
			print "Drone: drone controll - Arm: Altitude: ", self.vehicle.location.global_relative_frame.alt      
			if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
				print "Drone: drone controll - Arm: Reached target altitude"
				self.move_0()
				break
			time.sleep(1)

	def land_here(self):
		print "Drone: drone controll - land here"
		self.vehicle.mode = VehicleMode("LAND")


	def move_0_once(self):
		print "Drone: drone controll - move to the current position once"
		self.send_ned_velocity_once(0,0,0)

	def move_forward_once(self, velocity):
		print "Drone: drone controll - Forward " + str(velocity) + " m/s"
		self.send_ned_velocity_once(velocity,0,0)

	def move_backward_once(self, velocity):
		print "Drone: drone controll - Backward " + str(velocity) + " m/s"
		self.send_ned_velocity_once(-velocity,0,0)

	def move_left_once(self, velocity):
		print "Drone: drone controll - Left " + str(velocity) + " m/s"
		self.send_ned_velocity_once(0,-velocity,0)

	def move_right_once(self, velocity):
		print "Drone: drone controll - Right " + str(velocity) + " m/s"
		self.send_ned_velocity_once(0,velocity,0)


	def move_0(self):
		print "Drone: drone controll - move to the current position (to allow the yaw controll)"
		self.send_ned_velocity(0,0,0,1)

	def move_forward(self, velocity, duration):
		print "Drone: drone controll - move forward, vel: " + str(velocity) + ", duration:" + str(duration) + " *0.1 sec"
		self.send_ned_velocity(velocity,0,0,duration)
		self.send_ned_velocity(0,0,0,1)

	def move_backward(self, velocity, duration):
		print "Drone: drone controll - move backward, vel: " + str(velocity) + ", duration:" + str(duration) + " *0.1 sec"
		self.send_ned_velocity(-velocity,0,0,duration)
		self.send_ned_velocity(0,0,0,1)

	def move_left(self, velocity, duration):
		print "Drone: drone controll - move left, vel: " + str(velocity) + ", duration:" + str(duration) + " *0.1 sec"
		self.send_ned_velocity(0,-velocity,0,duration)
		self.send_ned_velocity(0,0,0,1)

	def move_right(self, velocity, duration):
		print "Drone: drone controll - move right, vel: " + str(velocity) + ", duration:" + str(duration) + " *0.1 sec"
		self.send_ned_velocity(0,velocity,0,duration)
		self.send_ned_velocity(0,0,0,1)

	def yaw_left(self, angle):
		print("Drone: drone controll - Yaw left " + str(angle) + " relative (to previous yaw heading)")
		self.condition_yaw(360-angle, relative=True)

	def yaw_right(self, angle):
		print("Drone: drone controll - Yaw right " + str(angle) + " relative (to previous yaw heading)")
		self.condition_yaw(angle, relative=True)


	def send_ned_velocity_once(self, velocity_x, velocity_y, velocity_z):
		"""
		Move vehicle in direction based on specified velocity vectors and
		for the specified duration.

		This uses the SET_POSITION_TARGET_LOCAL_NED command with a type mask enabling only 
		velocity components 
		(http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned).

		Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
		with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
		velocity persists until it is canceled. The code below should work on either version 
		(sending the message multiple times does not cause problems).

		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.
		"""
		msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
			0,       # time_boot_ms (not used)
			0, 0,    # target system, target component
			#mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
			mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame
			0b0000111111000111, # type_mask (only speeds enabled)
			0, 0, 0, # x, y, z positions (not used)
			velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
			0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
			0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

		# send single command to vehicle instantly
		self.vehicle.send_mavlink(msg)


	def send_ned_velocity(self, velocity_x, velocity_y, velocity_z, duration):
		"""
		Move vehicle in direction based on specified velocity vectors and
		for the specified duration.

		This uses the SET_POSITION_TARGET_LOCAL_NED command with a type mask enabling only 
		velocity components 
		(http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned).

		Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
		with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
		velocity persists until it is canceled. The code below should work on either version 
		(sending the message multiple times does not cause problems).

		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.
		"""
		msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
			0,       # time_boot_ms (not used)
			0, 0,    # target system, target component
			#mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
			mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame
			0b0000111111000111, # type_mask (only speeds enabled)
			0, 0, 0, # x, y, z positions (not used)
			velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
			0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
			0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

		# send command to vehicle on 1 Hz cycle
		#for x in range(0,duration):
		#	self.vehicle.send_mavlink(msg)
		#	time.sleep(1)

		# send command to vehicle on 10 Hz cycle
		for x in range(0,duration):
			self.vehicle.send_mavlink(msg)
			time.sleep(0.1)


	def send_global_velocity(self, velocity_x, velocity_y, velocity_z, duration):
		"""
		Move vehicle in direction based on specified velocity vectors.

		This uses the SET_POSITION_TARGET_GLOBAL_INT command with type mask enabling only 
		velocity components 
		(http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_global_int).

		Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
		with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
		velocity persists until it is canceled. The code below should work on either version 
		(sending the message multiple times does not cause problems).

		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.
		"""
		msg = self.vehicle.message_factory.set_position_target_global_int_encode(
			0,       # time_boot_ms (not used)
			0, 0,    # target system, target component
			mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
			0b0000111111000111, # type_mask (only speeds enabled)
			0, # lat_int - X Position in WGS84 frame in 1e7 * meters
			0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
			0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
			# altitude above terrain if GLOBAL_TERRAIN_ALT_INT
			velocity_x, # X velocity in NED frame in m/s
			velocity_y, # Y velocity in NED frame in m/s
			velocity_z, # Z velocity in NED frame in m/s
			0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
			0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

		# send command to vehicle on 1 Hz cycle
		for x in range(0,duration):
			self.vehicle.send_mavlink(msg)
			time.sleep(1)


	def condition_yaw(self, heading, relative=False):
		"""
		Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).

		This method sets an absolute heading by default, but you can set the `relative` parameter
		to `True` to set yaw relative to the current yaw heading.

		By default the yaw of the vehicle will follow the direction of travel. After setting 
		the yaw using this function there is no way to return to the default yaw "follow direction 
		of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)

		For more information see: 
		http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
		"""
		if relative:
			is_relative = 1 #yaw relative to direction of travel
		else:
			is_relative = 0 #yaw is an absolute angle
		# create the CONDITION_YAW command using command_long_encode()
		msg = self.vehicle.message_factory.command_long_encode(
			0, 0,    # target system, target component
			mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
			0, #confirmation
			heading,    # param 1, yaw in degrees
			0,          # param 2, yaw speed deg/s
			1,          # param 3, direction -1 ccw, 1 cw
			is_relative, # param 4, relative offset 1, absolute angle 0
			0, 0, 0)    # param 5 ~ 7 not used
		# send command to vehicle
		self.vehicle.send_mavlink(msg)


	def set_roi(self, location):
		"""
		Send MAV_CMD_DO_SET_ROI message to point camera gimbal at a 
		specified region of interest (LocationGlobal).
		The vehicle may also turn to face the ROI.

		For more information see: 
		http://copter.ardupilot.com/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_do_set_roi
		"""
		# create the MAV_CMD_DO_SET_ROI command
		msg = self.vehicle.message_factory.command_long_encode(
			0, 0,    # target system, target component
			mavutil.mavlink.MAV_CMD_DO_SET_ROI, #command
			0, #confirmation
			0, 0, 0, 0, #params 1-4
			location.lat,
			location.lon,
			location.alt
			)
		# send command to vehicle
		self.vehicle.send_mavlink(msg)



	"""
	Functions to make it easy to convert between the different frames-of-reference. In particular these
	make it easy to navigate in terms of "metres from the current position" when using commands that take 
	absolute positions in decimal degrees.

	The methods are approximations only, and may be less accurate over longer distances, and when close 
	to the Earth's poles.

	Specifically, it provides:
	* get_location_metres - Get LocationGlobal (decimal degrees) at distance (m) North & East of a given LocationGlobal.
	* get_distance_metres - Get the distance between two LocationGlobal objects in metres
	* get_bearing - Get the bearing in degrees to a LocationGlobal
	"""

	def get_location_metres(self, original_location, dNorth, dEast):
		"""
		Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
		specified `original_location`. The returned LocationGlobal has the same `alt` value
		as `original_location`.

		The function is useful when you want to move the vehicle around specifying locations relative to 
		the current vehicle position.

		The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.

		For more information see:
		http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
		"""
		earth_radius = 6378137.0 #Radius of "spherical" earth
		#Coordinate offsets in radians
		dLat = dNorth/earth_radius
		dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

		#New position in decimal degrees
		newlat = original_location.lat + (dLat * 180/math.pi)
		newlon = original_location.lon + (dLon * 180/math.pi)
		if type(original_location) is LocationGlobal:
			targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
		elif type(original_location) is LocationGlobalRelative:
			targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
		else:
			raise Exception("Invalid Location object passed")
		
		return targetlocation;


	def get_distance_metres(self, aLocation1, aLocation2):
		"""
		Returns the ground distance in metres between two LocationGlobal objects.

		This method is an approximation, and will not be accurate over large distances and close to the 
		earth's poles. It comes from the ArduPilot test code: 
		https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
		"""
		dlat = aLocation2.lat - aLocation1.lat
		dlong = aLocation2.lon - aLocation1.lon
		return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


	def get_bearing(self, aLocation1, aLocation2):
		"""
		Returns the bearing between the two LocationGlobal objects passed as parameters.

		This method is an approximation, and may not be accurate over large distances and close to the 
		earth's poles. It comes from the ArduPilot test code: 
		https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
		"""	
		off_x = aLocation2.lon - aLocation1.lon
		off_y = aLocation2.lat - aLocation1.lat
		bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
		if bearing < 0:
			bearing += 360.00
		return bearing;



	"""
	Functions to move the vehicle to a specified position (as opposed to controlling movement by setting velocity components).

	The methods include:
	* goto_position_target_global_int - Sets position using SET_POSITION_TARGET_GLOBAL_INT command in 
	    MAV_FRAME_GLOBAL_RELATIVE_ALT_INT frame
	* goto_position_target_local_ned - Sets position using SET_POSITION_TARGET_LOCAL_NED command in 
	    MAV_FRAME_BODY_NED frame
	* goto - A convenience function that can use Vehicle.simple_goto (default) or 
	    goto_position_target_global_int to travel to a specific position in metres 
	    North and East from the current location. 
	    This method reports distance to the destination.
	"""

	def goto_position_target_global_int(self, aLocation):
		"""
		Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified LocationGlobal.

		For more information see: https://pixhawk.ethz.ch/mavlink/#SET_POSITION_TARGET_GLOBAL_INT

		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.
		"""
		msg = self.vehicle.message_factory.set_position_target_global_int_encode(
			0,       # time_boot_ms (not used)
			0, 0,    # target system, target component
			mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
			0b0000111111111000, # type_mask (only speeds enabled)
			aLocation.lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
			aLocation.lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
			aLocation.alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
			0, # X velocity in NED frame in m/s
			0, # Y velocity in NED frame in m/s
			0, # Z velocity in NED frame in m/s
			0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
			0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
		# send command to vehicle
		self.vehicle.send_mavlink(msg)


	def goto_position_target_local_ned(self, north, east, down):
		"""	
		Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
		location in the North, East, Down frame.

		It is important to remember that in this frame, positive altitudes are entered as negative 
		"Down" values. So if down is "10", this will be 10 metres below the home altitude.

		Starting from AC3.3 the method respects the frame setting. Prior to that the frame was
		ignored. For more information see: 
		http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned

		See the above link for information on the type_mask (0=enable, 1=ignore). 
		At time of writing, acceleration and yaw bits are ignored.

		"""
		msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
			0,       # time_boot_ms (not used)
			0, 0,    # target system, target component
			mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
			0b0000111111111000, # type_mask (only positions enabled)
			north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
			0, 0, 0, # x, y, z velocity in m/s  (not used)
			0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
			0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
		# send command to vehicle
		self.vehicle.send_mavlink(msg)



	def goto(self, dNorth, dEast, gotoFunction=None):
		if gotoFunction is None:
			gotoFunction = self.vehicle.simple_goto
		"""
		Moves the vehicle to a position dNorth metres North and dEast metres East of the current position.

		The method takes a function pointer argument with a single `dronekit.lib.LocationGlobal` parameter for 
		the target position. This allows it to be called with different position-setting commands. 
		By default it uses the standard method: dronekit.lib.Vehicle.simple_goto().

		The method reports the distance to target every two seconds.
		"""

		currentLocation = self.vehicle.location.global_relative_frame
		targetLocation = self.get_location_metres(currentLocation, dNorth, dEast)
		targetDistance = self.get_distance_metres(currentLocation, targetLocation)
		gotoFunction(targetLocation)

		#print "DEBUG: targetLocation: %s" % targetLocation
		#print "DEBUG: targetLocation: %s" % targetDistance

		while self.vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
			#print "DEBUG: mode: %s" % self.vehicle.mode.name
			remainingDistance=self.get_distance_metres(self.vehicle.location.global_relative_frame, targetLocation)
			print "Distance to target: ", remainingDistance
			if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
				print "Reached target"
				break;
			time.sleep(2)



	"""
	Functions that move the vehicle by specifying the velocity components in each direction.
	The two functions use different MAVLink commands. The main difference is
	that depending on the frame used, the NED velocity can be relative to the vehicle
	orientation.

	The methods include:
	* send_ned_velocity - Sets velocity components using SET_POSITION_TARGET_LOCAL_NED command
	* send_global_velocity - Sets velocity components using SET_POSITION_TARGET_GLOBAL_INT command
	"""


	def triangle(self):
		"""
		Fly a triangular path using the standard Vehicle.simple_goto() method.

		The method is called indirectly via a custom "goto" that allows the target position to be
		specified as a distance in metres (North/East) from the current position, and which reports
		the distance-to-target.
		"""	

		print("Drone: drone controll - Triangle: TRIANGLE path using standard Vehicle.simple_goto()")

		print("Drone: drone controll - Triangle: Set groundspeed to 5m/s.")
		self.vehicle.groundspeed=5

		print("Drone: drone controll - Triangle: Position North 80 West 50")
		self.goto(80, -50)

		print("Drone: drone controll - Triangle: Position North 0 East 100")
		self.goto(0, 100)

		print("Drone: drone controll - Triangle: Position North -80 West 50")
		self.goto(-80, -50)


	def triangle2(self):
		"""
		Fly a triangular path using the SET_POSITION_TARGET_GLOBAL_INT command and specifying
		a target position (rather than controlling movement using velocity vectors). The command is
		called from goto_position_target_global_int() (via `goto`).

		The goto_position_target_global_int method is called indirectly from a custom "goto" that allows 
		the target position to be specified as a distance in metres (North/East) from the current position, 
		and which reports the distance-to-target.

		The code also sets the speed (MAV_CMD_DO_CHANGE_SPEED). In AC3.2.1 Copter will accelerate to this speed 
		near the centre of its journey and then decelerate as it reaches the target. 
		In AC3.3 the speed changes immediately.
		"""

		print("Drone: drone controll - Triangle2: TRIANGLE path using standard SET_POSITION_TARGET_GLOBAL_INT message and with varying speed.")
		print("Drone: drone controll - Triangle2: Position South 100 West 130")

		print("Drone: drone controll - Triangle2: Set groundspeed to 5m/s.")
		self.vehicle.groundspeed = 5
		self.goto(-100, -130, self.goto_position_target_global_int)

		print("Drone: drone controll - Triangle2: Set groundspeed to 15m/s (max).")
		self.vehicle.groundspeed = 15
		print("Drone: drone controll - Triangle2: Position South 0 East 200")
		self.goto(0, 260, self.goto_position_target_global_int)

		print("Drone: drone controll - Triangle2: Set airspeed to 10m/s (max).")
		self.vehicle.airspeed = 10

		print("Drone: drone controll - Triangle2: Position North 100 West 130")
		self.goto(100, -130, self.goto_position_target_global_int)


	def square(self):
		"""
		Fly the vehicle in a 50m square path, using the SET_POSITION_TARGET_LOCAL_NED command 
		and specifying a target position (rather than controlling movement using velocity vectors). 
		The command is called from goto_position_target_local_ned() (via `goto`).

		The position is specified in terms of the NED (North East Down) relative to the Home location.

		WARNING: The "D" in NED means "Down". Using a positive D value will drive the vehicle into the ground!

		The code sleeps for a time (DURATION) to give the vehicle time to reach each position (rather than 
		sending commands based on proximity).

		The code also sets the region of interest (MAV_CMD_DO_SET_ROI) via the `set_roi()` method. This points the 
		camera gimbal at the the selected location (in this case it aligns the whole vehicle to point at the ROI).
		"""	

		print("Drone: drone controll - Square: SQUARE path using SET_POSITION_TARGET_LOCAL_NED and position parameters")
		self.DURATION = 20 #Set duration for each segment.

		print("Drone: drone controll - Square: North 50m, East 0m, 10m altitude for %s seconds" % self.DURATION)
		self.goto_position_target_local_ned(50,0,-10)
		print("Drone: drone controll - Square: Point ROI at current location (home position)") 
		# NOTE that this has to be called after the goto command as first "move" command of a particular type
		# "resets" ROI/YAW commands
		self.set_roi(self.vehicle.location.global_relative_frame)
		time.sleep(self.DURATION)

		print("Drone: drone controll - Square: North 50m, East 50m, 10m altitude")
		self.goto_position_target_local_ned(50,50,-10)
		time.sleep(self.DURATION)

		print("Drone: drone controll - Square: Point ROI at current location")
		self.set_roi(self.vehicle.location.global_relative_frame)

		print("Drone: drone controll - Square: North 0m, East 50m, 10m altitude")
		self.goto_position_target_local_ned(0,50,-10)
		time.sleep(self.DURATION)

		print("Drone: drone controll - Square: North 0m, East 0m, 10m altitude")
		self.goto_position_target_local_ned(0,0,-10)
		time.sleep(self.DURATION)

	def square2(self):
		"""
		Fly the vehicle in a SQUARE path using velocity vectors (the underlying code calls the 
		SET_POSITION_TARGET_LOCAL_NED command with the velocity parameters enabled).

		The thread sleeps for a time (DURATION) which defines the distance that will be travelled.

		The code also sets the yaw (MAV_CMD_CONDITION_YAW) using the `set_yaw()` method in each segment
		so that the front of the vehicle points in the direction of travel
		"""

		print("Drone: drone controll - Square2: SQUARE path using SET_POSITION_TARGET_LOCAL_NED and position parameters")
		self.DURATION = 20 #Set duration for each segment.

		#Set up velocity vector to map to each direction.
		# vx > 0 => fly North
		# vx < 0 => fly South
		self.NORTH = 2
		self.SOUTH = -2

		# Note for vy:
		# vy > 0 => fly East
		# vy < 0 => fly West
		self.EAST = 2
		self.WEST = -2

		# Note for vz: 
		# vz < 0 => ascend
		# vz > 0 => descend
		self.UP = -0.5
		self.DOWN = 0.5


		# Square path using velocity
		print("Drone: drone controll - Square2: SQUARE path using SET_POSITION_TARGET_LOCAL_NED and velocity parameters")

		print("Drone: drone controll - Square2: Yaw 180 absolute (South)")
		self.condition_yaw(180)

		print("Drone: drone controll - Square2: Velocity South & up")
		self.send_ned_velocity(self.SOUTH,0,self.UP,self.DURATION)
		self.send_ned_velocity(0,0,0,1)


		print("Drone: drone controll - Square2: Yaw 270 absolute (West)")
		self.condition_yaw(270)

		print("Drone: drone controll - Square2: Velocity West & down")
		self.send_ned_velocity(0,self.WEST,self.DOWN,self.DURATION)
		self.send_ned_velocity(0,0,0,1)


		print("Drone: drone controll - Square2: Yaw 0 absolute (North)")
		self.condition_yaw(0)

		print("Drone: drone controll - Square2: Velocity North")
		self.send_ned_velocity(self.NORTH,0,0,self.DURATION)
		self.send_ned_velocity(0,0,0,1)


		print("Drone: drone controll - Square2: Yaw 90 absolute (East)")
		self.condition_yaw(90)

		print("Drone: drone controll - Square2: Velocity East")
		self.send_ned_velocity(0,self.EAST,0,self.DURATION)
		self.send_ned_velocity(0,0,0,1)


	def diamond(self):
		"""
		Fly the vehicle in a DIAMOND path using velocity vectors (the underlying code calls the 
		SET_POSITION_TARGET_GLOBAL_INT command with the velocity parameters enabled).

		The thread sleeps for a time (DURATION) which defines the distance that will be travelled.

		The code sets the yaw (MAV_CMD_CONDITION_YAW) using the `set_yaw()` method using relative headings
		so that the front of the vehicle points in the direction of travel.

		At the end of the second segment the code sets a new home location to the current point.
		"""
		
		print("Drone: drone controll - Diamond: SQUARE path using SET_POSITION_TARGET_LOCAL_NED and position parameters")
		self.DURATION = 20 #Set duration for each segment.

		#Set up velocity vector to map to each direction.
		# vx > 0 => fly North
		# vx < 0 => fly South
		self.NORTH = 2
		self.SOUTH = -2

		# Note for vy:
		# vy > 0 => fly East
		# vy < 0 => fly West
		self.EAST = 2
		self.WEST = -2

		# Note for vz: 
		# vz < 0 => ascend
		# vz > 0 => descend
		self.UP = -0.5
		self.DOWN = 0.5

		print("Drone: drone controll - Diamond: DIAMOND path using SET_POSITION_TARGET_GLOBAL_INT and velocity parameters")
		# vx, vy are parallel to North and East (independent of the vehicle orientation)

		print("Drone: drone controll - Diamond: Yaw 225 absolute")
		self.condition_yaw(225)

		print("Drone: drone controll - Diamond: Velocity South, West and Up")
		self.send_global_velocity(self.SOUTH,self.WEST,self.UP,self.DURATION)
		self.send_global_velocity(0,0,0,1)

		print("Drone: drone controll - Diamond: Yaw 90 relative (to previous yaw heading)")
		self.condition_yaw(90,relative=True)

		print("Drone: drone controll - Diamond: Velocity North, West and Down")
		self.send_global_velocity(self.NORTH,self.WEST,self.DOWN,self.DURATION)
		self.send_global_velocity(0,0,0,1)

		print("Drone: drone controll - Diamond: Set new home location to current location")
		self.vehicle.home_location=self.vehicle.location.global_frame
		print "Drone: drone controll - Diamond: Get new home location"
		#This reloads the home location in DroneKit and GCSs
		cmds = self.vehicle.commands
		cmds.download()
		cmds.wait_ready()
		print "Drone: drone controll - Diamond: Home Location: %s" % self.vehicle.home_location


		print("Drone: drone controll - Diamond: Yaw 90 relative (to previous yaw heading)")
		self.condition_yaw(90,relative=True)

		print("Drone: drone controll - Diamond: Velocity North and East")
		self.send_global_velocity(self.NORTH,self.EAST,0,self.DURATION)
		self.send_global_velocity(0,0,0,1)


		print("Drone: drone controll - Diamond: Yaw 90 relative (to previous yaw heading)")
		self.condition_yaw(90,relative=True)

		print("Drone: drone controll - Diamond: Velocity South and East")
		self.send_global_velocity(self.SOUTH,self.EAST,0,self.DURATION)
		self.send_global_velocity(0,0,0,1)


	"""
	Convenience functions for sending immediate/guided mode commands to control the Copter.

	The set of commands demonstrated here include:
	* MAV_CMD_CONDITION_YAW - set direction of the front of the Copter (latitude, longitude)
	* MAV_CMD_DO_SET_ROI - set direction where the camera gimbal is aimed (latitude, longitude, altitude)
	* MAV_CMD_DO_CHANGE_SPEED - set target speed in metres/second.


	The full set of available commands are listed here:
	http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/
	"""

