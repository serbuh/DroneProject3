import socket
import cv2
import numpy
import copy
from  Queue import Queue
import threading
import time


HOST = '192.168.12.1'
PORT = 3333

def showImage(title , frame ,event, wait = False ):	
	cv2.imshow(title, frame)
    	if wait:
        	while True:
           		if cv2.waitKey(0)&0xff==ord('q'):
              			break
        	cv2.destroyAllWindows()
    	else:
        	if cv2.waitKey(1)&0xff == ord('q'):
            		event.clear()

#def reciveAndQueue(queue,socket,run_event):
#	flag = 0
#	while run_event.is_set():
#		print "Recive!"
#		packet = socket.recv(60000)
#   	print "Recive1!"
#    	data = eval(packet)
#    	queue.put(data)

def recieveAndQueue(queue,run_event):
	while run_event.is_set():
		data = s.recv(60000)
		data = eval(data)
		queue.put(data)
	print "Recieve Thread Closed"

if __name__ == "__main__":
	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind((HOST,PORT))
	s.settimeout(0.1)
	q = Queue()
	run_event = threading.Event()
	run_event.set() 

	recieveThread = threading.Thread(target=recieveAndQueue, args=[q,run_event])
	print "Start Recieve Thread!"
	recieveThread.start()
	full_data = ''
	while run_event.is_set():
		try:
			data = q.get()
			#print data[0]
			#if len(full_data) != 0 and data[0] == 0:
			#	full_data = ''
			#	print "Reset frame!"
			#else:
			if data[0] == 0 :
				full_data = data[1]
			else :
				full_data = ''.join([full_data,data[1]])
			#print len(full_data),data[0]
			if(len(full_data) == 921600):
				tmp_frame = numpy.fromstring(full_data, dtype=numpy.uint8)
				frame = numpy.reshape(tmp_frame, (480,640,3))
				showImage("Client", frame)
				full_data = ''
			if cv2.waitKey(1)&0xff == ord('q'):
				raise KeyboardInterrupt
			
 		except(KeyboardInterrupt , SystemExit):
			run_event.clear()
			recieveThread.join()
			s.close()
			cv2.destroyAllWindows()
			break
