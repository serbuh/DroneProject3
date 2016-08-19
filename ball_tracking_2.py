import numpy as np
import argparse
import imutils
import cv2
from camera import *

def findMask(hsv,lower,upper):
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	return mask


def redBallTracking(vehicle_controll, frame):
	frame = imutils.resize(frame, width=500)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# lower mask (0-10)
	lower_red = np.array([0,50,50])
	upper_red = np.array([10,255,255])
	mask0 = findMask(hsv,lower_red,upper_red)

	# upper mask (170-180)
	lower_red = np.array([170,50,50])
	upper_red = np.array([180,255,255])
	mask1 = findMask(hsv,lower_red,upper_red)	

	mask = mask1 + mask0
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	frame_size = frame.shape

	# center[0] 	- x ; center[1] 	- y
	# frame_size[1]	- x ; frame_size[0] 	- y
	# offset scale: 0 ... 50 ... 100

	if center != None:
		center = (center[0], frame_size[0] - center[1])
		#print "Center x-1: "+ str(center[1]) + " Frame x-0: " + str(frame_size[0])
		#print "Center y-0: "+ str(center[0]) + " Frame y-1: " + str(frame_size[1])
		x_offset = int((float(center[1])/frame_size[0]) * 100)
		y_offset = int((float(center[0])/frame_size[1]) * 100)

		print "X offset: " + str(x_offset) + "% , Y offset: " + str(y_offset) + "%"
		decide_moving(vehicle_controll, x_offset, y_offset)
	else:
		print "X offset is None, Y offset is None"

	return frame

def decide_moving(vehicle_controll, x_offset, y_offset):
	if (40 < x_offset < 60):
		print "Stay"		
		#vehicle_controll.move_left(1)
	elif x_offset < 40:
		print "Must move left"
	elif x_offset > 60:
		print "Must move right"		
		#vehicle_controll.move_right(1)

	'''if center != None:
		if center[0] < (frame_size[1])/2 :
			s = "Left"
		else:
			s = "Right"

		if center[1] < (frame_size[0])/2 :
			print "Upper " + s + " corner"
		else:
			print "Lower " + s + " corner"
	'''
	
