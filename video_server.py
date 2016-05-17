import socket
import time
import cv2
from camera import *
import numpy as np

HOST = "192.168.150.1"
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
		while max(frame.shape[:2]) > 310:
       			frame = cv2.pyrDown(frame)
		try:
			#cv2.imshow("Server", frame)
			#if cv2.waitKey(1)&0xff == ord('q'):
            		#	raise KeyboardInterrupt()
			showImage("Server",frame)
			#print frame.shape
			frame = frame.flatten()
			data = frame.tostring()
			#print "Sent Frame! Length {}".format(len(data))
			print "SENT!"
			s.sendto(data,(HOST,PORT))
		except KeyboardInterrupt:
			cv2.waitKey(0)
			c.stop_capture()
			c.disconnect()
			break

