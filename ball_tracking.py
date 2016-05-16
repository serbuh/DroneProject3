from camera import *
import numpy as np
import cv2


camera = Camera()

while 1:
	frame = camera.getFrame(True)
	cv2.medianBlur(frame,3,frame)

	hsv_frame = None
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_red_hue_range = None
	upper_red_hue_range = None
	lower = np.array([0, 100, 100])
	upper = np.array([10, 255, 255])
	lower_red_hue_range = cv2.inRange(hsv_frame,lower,upper)
	lower = np.array([160, 100, 100])
	upper = np.array([179, 255, 255])
	upper_red_hue_range = cv2.inRange(hsv_frame,lower,upper)

	red_hue_image = None
	red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)

	red_hue_image = cv2.GaussianBlur(red_hue_image,(9,9), 2, 2);
	tmp = red_hue_image.shape[0]
	#circles = cv2.HoughCircles(red_hue_image,cv2.HOUGH_GRADIENT,1,tmp/8, 100, 20)

	radius = 0
	index = 0
	flag = 0
	circles = None
	if circles != None:
		flag = 1		
		for i in range(0,len(circles)):
			#center = (int(round(circles[0][i][0],0)),int(round(circles[0][i][1],0)))
			 if radius < int(round(circles[0][i][2])):
				radius = int(round(circles[0][i][2]))
				index = i
			#cv2.circle(frame, center, radius, (0, 255, 0), 5)
	if flag == 1:
		radius = int(round(circles[0][index][2]))
		center = (int(round(circles[0][index][0],0)),int(round(circles[0][index][1],0)))
		cv2.circle(frame, center, radius, (0, 255, 0), 5)
	#cv2.imshow("Threshold lower image", lower_red_hue_range);
	#cv2.imshow("Threshold upper image", upper_red_hue_range);
	#cv2.imshow("Combined threshold images", red_hue_image);
	cv2.imshow("Detected red circles on the input image", frame);
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
