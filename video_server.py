import socket
import time
import cv2
from camera import *
import numpy as np
from ball_tracking_2 import *


HOST = 'localhost'
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
		#while max(frame.shape[:2]) > 300:
       		#	frame = cv2.pyrDown(frame)
		frame = cv2.resize(redBallTracking(frame),(180, 120))		
		try:
			#cv2.imshow("Server", frame)
			#if cv2.waitKey(1)&0xff == ord('q'):
            		#	raise KeyboardInterrupt()
			showImage("Server",frame)
			#print len(frame)
			frame = frame.flatten()
			#print frame.shape , len(frame)
			#data = frame.tostring()
			#print len(data)
			#n = 1000
			#l = np.array_split(frame,1000)
			#num = float(len(data))/n
			#l = [ data [i:i + int(num)] for i in range(0, (n-1)*int(num), int(num))]
			#print "Sent Frame! Length {}".format(len(l[0]))
			#for i in range(0,1000):
			#	data = l[i].tostring()
			data = frame.tostring()
			print "SENT " + str(len(data))	+ "b"	
			s.sendto(data,(HOST,PORT))
		except KeyboardInterrupt:
			cv2.waitKey(0)
			s.close()
			break

