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
		#while max(frame.shape[:2]) > 300:
       		#	frame = cv2.pyrDown(frame)
		frame = cv2.resize(frame,(640, 480))
		try:
			#cv2.imshow("Server", frame)
			#if cv2.waitKey(1)&0xff == ord('q'):
            		#	raise KeyboardInterrupt()
			showImage("Server",frame)
			#print frame.shape
			frame = frame.flatten()
			data = frame.tostring()
			n = 1000
			num = float(len(data))/n
			l = [ data [i:i + int(num)] for i in range(0, (n-1)*int(num), int(num))]
			print "Sent Frame! Length {}".format(len(l[0]))
			print "SENT!"
			for i in range(0,n-1):
				s.sendto(l[i],(HOST,PORT))
		except KeyboardInterrupt:
			cv2.waitKey(0)
			s.close()
			break

