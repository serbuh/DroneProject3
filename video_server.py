from datetime import datetime

import socket
import time
import cv2
from camera import *
import numpy as np
from Queue import Queue
#from ball_tracking_2 import *
from time import sleep
import threading


HOST = '192.168.12.95'
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
            		raise KeyboardInterrupt

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def chunkAndSend(queue,socket,run_event):
	try:
		while run_event.is_set():
			if not queue.empty():
				data = queue.get()
				data = list(chunkstring(data,14400))
				for i in range(0,64):
					pack = str((i,data[i]))
					#l = l + len(data[i])
					s.sendto(pack,(HOST,PORT))
					#print len(pack),i
				print "sent: " + str(datetime.now())

				#print l , i
	except KeyboardInterrupt:
		print "Thread interupt..."	
		close_event.set()	
	print "Send Thread Close"
			
if __name__ == "__main__":
	camera = Camera()
	q = Queue()	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	run_event = threading.Event()
	#run_event.set() 	
	
	sendThread = threading.Thread(target=chunkAndSend, args=[q,s,run_event])	
	#cap = cv2.VideoCapture(0)
	run_event.set()	
	print "Start Send Thread!"
	sendThread.start()	
	while not close_event.is_set():
		try:
			frame = camera.getFrame(True)
			#ret, frame = cap.read()
			#frame = cv2.resize(redBallTracking(frame),(640, 480))
			frame = cv2.resize(frame,(640,480))		
			#showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			q.put(data)
			#sleep(0.1)
			#print "main!"			
					
		except KeyboardInterrupt:
			print "MAIN LOOP INTERUPT!"
			run_event.clear()
			print "joining..."
			sendThread.join()
			print "dead.."
			break			
			cv2.destroyAllWindows()			
			
	if close_event.is_set():
		print "Cleaning..."
		cv2.destroyAllWindows()
