import socket
import time
import cv2
from camera import *
import numpy as np
from ball_tracking_2 import *
from time import sleep


HOST = '127.0.0.1'
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

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))



if __name__ == "__main__":
	camera = Camera()
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	cap = cv2.VideoCapture(0)
	while True:
		frame = camera.getFrame(True)
		#ret, frame = cap.read()
		l = 0
		#frame = cv2.resize(redBallTracking(frame),(180, 120))		
		frame = cv2.resize(redBallTracking(frame),(640, 480))		
		try:
			showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			#print len(data)
			data = list(chunkstring(data,14400))
			#print "data: " + str(len(data))
			for i in range(0,64):
				#if i == 0:
				#	pack = str((i,len(data)+1))
				#else:
				pack = str((i,data[i]))
				l = l + len(data[i])
				#print len(pack)
				s.sendto(pack,(HOST,PORT))
			print l , i
			if cv2.waitKey(1) & 0xFF == ord('q'):
				raise KeyboardInterrupt()
		except KeyboardInterrupt:
			cv2.waitKey(0)
			s.close()
			break

