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


def redBallTracking(frame):
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

	a = frame.shape
	if center != None:
		if center[0] < (a[1])/2 :
			s = "Left"
		else:
			s = "Right"

		if center[1] < (a[0])/2 :
			print "Upper " + s + " corner"
		else:
			print "Lower " + s + " corner"
	return frame
	
