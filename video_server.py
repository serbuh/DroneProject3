import socket
import time
import cv2
from camera import *
import numpy as np
from ball_tracking_2 import *


HOST = '192.168.150.1'
PORT = 3333

def showImage(title , frame , wait = False ):	
	cv2.imshow(title, frame)
    	if wait:
        	while True:
           		if cv2.waitKey(0)&0xff==ord('q'):
              			break
        	cv2.destroyAllWindows()
    	else:
        	if cv2.waitKey(1)&0xff == ord('q'):
            		raise KeyboardInterrupt()


if __name__ == "__main__":
	camera = Camera()
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	while True:
		frame = camera.getFrame(True)
		frame = cv2.resize(redBallTracking(frame),(180, 120))		
		try:
			showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			print "SENT " + str(len(data))	+ "b"
			s.sendto(data,(HOST,PORT))
			if cv2.waitKey(1)&0xff == ord('q'):
            			raise KeyboardInterrupt()
		except KeyboardInterrupt:
			cv2.waitKey(0)
			s.close()
			break

