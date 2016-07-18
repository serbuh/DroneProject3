import socket
import cv2
import numpy
import copy
from  Queue import Queue
import threading
import time


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

def reciveAndQueue(queue,socket,run_event):
	flag = 0
	while run_event.is_set():
		print "Recive!"
		packet = socket.recv(60000)
    	print "Recive1!"
    	data = eval(packet)
    	queue.put(data)

def readAndShow(queue,run_event):
	full_data = ''
	while run_event.is_set():
		try:
			data = queue.get()
			full_data = ''.join([full_data,data])
			if(len(full_data) == 921600):
				tmp_frame = numpy.fromstring(full_data, dtype=numpy.uint8)
				frame = numpy.reshape(tmp_frame, (480,640,3))
				showImage("Client", frame)
				full_data = ''
				if cv2.waitKey(1) & 0xFF == ord('q'):
					raise KeyboardInterrupt()
 		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind((HOST,PORT))
	q = Queue()
	run_event = threading.Event()
	run_event.set() 

	showThread = threading.Thread(target=readAndShow, args=[q,run_event])
	print "Start Show Thread!"
	showThread.start()

	flag = 0
	while True:
		try:
			data = s.recv(60000)
			data = eval(data)
			if data[0] == 0:
				q.put(data[1])
				for i in range(0,63):
					data = s.recv(60000)
					data = eval(data)
					q.put(data[1])
 		except(KeyboardInterrupt , SystemExit):
			run_event.clear()
			showThread.join()
			s.close()
