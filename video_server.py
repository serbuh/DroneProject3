import socket
import time
import cv2
from camera import *
import numpy as np
from Queue import Queue
<<<<<<< HEAD
from ball_tracking_2 import *
=======
from ball_tracking_2 import *
>>>>>>> 209b8c7a5d616c9f12ac1948adbfe5b422c64784
from time import sleep
import threading


HOST = '127.0.0.1'
PORT = 3333

close_event = threading.Event()	


def showImage(title , frame , wait = False ):	
	cv2.imshow(title, frame)
    	if wait:
        	while True:
           		if cv2.waitKey(0)&0xff==ord('q'):
              			break
        	cv2.destroyAllWindows()
    	else:
        	if cv2.waitKey(1)&0xff == ord('q'):
            		close_event.set()

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def chunkAndSend(queue,socket,run_event):
	while run_event.is_set():
		data = queue.get()
		print len(data)
		data = list(chunkstring(data,14400))
		for i in range(0,64):
			pack = str((i,data[i]))
			#l = l + len(data[i])
<<<<<<< HEAD
			s.sendto(pack,(HOST,PORT))
=======
			s.sendto(pack,(HOST,PORT))
>>>>>>> 209b8c7a5d616c9f12ac1948adbfe5b422c64784
			#print "SENT!"
		#print l , i
	print "Send Thread Close"
			
if __name__ == "__main__":
	camera = Camera()
	q = Queue()	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	run_event = threading.Event()
	#run_event.set() 	
	
	sendThread = threading.Thread(target=chunkAndSend, args=[q,s,run_event])	
	#cap = cv2.VideoCapture(0)
	while True:
		frame = camera.getFrame(True)
		#ret, frame = cap.read()
		#frame = cv2.resize(redBallTracking(frame),(180, 120))		
<<<<<<< HEAD
		frame = cv2.resize(redBallTracking(frame),(640, 480))
=======
		frame = cv2.resize(redBallTracking(frame),(640, 480))
>>>>>>> 209b8c7a5d616c9f12ac1948adbfe5b422c64784
		frame = cv2.resize(frame,(640,480))
		#showImage("Server",frame)		
		try:
			#showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			q.put(data)			
			if run_event.is_set() == False and q.empty() == False:
				run_event.set()
				print "Start Recieve Thread!"
				sendThread.start()		
			#if cv2.waitKey(1) & 0xFF == ord('q'):
			if close_event.is_set():						
				break
		except KeyboardInterrupt:
			cv2.waitKey(0)			
			run_event.clear()			
			cv2.destroyAllWindows()			
			s.close()
			break

	cv2.waitKey(0)			
	run_event.clear()			
	cv2.destroyAllWindows()			
	s.close()
<<<<<<< HEAD
=======
>>>>>>> 209b8c7a5d616c9f12ac1948adbfe5b422c64784
