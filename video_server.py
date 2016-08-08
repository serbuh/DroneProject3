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
            		close_event.set()

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def chunkAndSend(queue,socket,run_event):
	while run_event.is_set():
		data = queue.get()
		#print len(data)
		data = list(chunkstring(data,14400))
		for i in range(0,64):
			pack = str((i,data[i]))
			#l = l + len(data[i])
			s.sendto(pack,(HOST,PORT))
		print "SENT!"
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#print l , i
	print "Send Thread Close"
			
if __name__ == "__main__":
	camera = Camera()
	q = Queue()	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	#run_event = threading.Event()
	#run_event.set() 	
	
	#sendThread = threading.Thread(target=chunkAndSend, args=[q,s,run_event])	
	#cap = cv2.VideoCapture(0)
	while True:
		try:
			frame = camera.getFrame(True)
			#ret, frame = cap.read()
			#frame = cv2.resize(redBallTracking(frame),(180, 120))		
			#frame = cv2.resize(redBallTracking(frame),(640, 480))
			frame = cv2.resize(frame,(320,240))
			#showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			l = len(data)/16
			for i in range(0,16):
				pack = str((i,data[l*i:l*(i+1)]))
				#print len(pack)
				s.sendto(pack,(HOST,PORT))
			#print len(data)
			#q.put(data)			
			'''if run_event.is_set() == False and q.empty() == False:
				run_event.set()
				print "Start Recieve Thread!"
				sendThread.start()'''		
			print "Sent Frame!"
		except KeyboardInterrupt:
			#cv2.waitKey(0)			
			#run_event.clear()
			#sendThread.join()			
			#cv2.destroyAllWindows()			
			s.close()
			break

