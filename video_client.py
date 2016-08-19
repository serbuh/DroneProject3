from datetime import datetime

import socket
import cv2
import numpy
import copy
from  Queue import Queue
import threading
import time
import errno
from time import sleep
from scipy import ndimage


HOST = ''
PORT = 3333


class Video_Client:
	def __init__(self,Port , Host = ''):
		self.port = Port
		self.host = Host
		self.socket =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.socket.bind((HOST,PORT))
		self.socket.settimeout(5)
		self.close_event = threading.Event()
		self.hist = [0,0,0,0] 
		self.frameQueue = Queue() 
		self.getVideoThread = threading.Thread(target=self.getVideo, args=[])
		self.getVideoThread.start()
		self.showVideoThread = threading.Thread(target=self.showVideo, args=[])
		self.showVideoThread.start()
		self.frame_num = None

	def getVideo(self):
		time_prev = datetime.now()
		while not self.close_event.is_set():
			try:
				data = self.socket.recv(65000)
				#print str(datetime.now())
				data = eval(data)
				if self.frame_num == None:
					self.frame_num = data[0]
				time_now = datetime.now()
				time_delta = time_now - time_prev
				print str(time_now) +" Delta: " + str(time_delta) + ": Frame: " + str(data[0]) +" Chunk: " + str(data[1])
				time_prev = time_now
				self.frameQueue.put(data)
				if data[1] == 3:
					time.sleep(0.005)
				#self.showImage("Client", frame)
			except socket.timeout:
				print "No data on network!"
				self.close_event.set()
				print self.hist
				break
			except KeyboardInterrupt:
				print "KeyboardInterrupt"
				self.close_event.set()
				#self.showVideoThread.join()
				#cv2.destroyAllWindows()
				print "Closed Video Feed"
				



	def showVideo(self):
		while not self.close_event.is_set():
			try:
				i = 0
				if not self.frameQueue.empty():
					data = self.frameQueue.get()
					self.hist[data[1]] += 1
				else:
					time.sleep(0.1)
				#if data[0] > (self.frame_num + 100):
					#print self.hist
					#raise KeyboardInterrupt
				#if self.frame_num == None and data[0] != 0:
				#	continue
				#elif self.frame_num == None and data[0] == 0:
				#	self.frame_num = data[2]
				#elif 
				#self.frame_dict[data[0]] =  data[1]
				#tmp_frame = numpy.fromstring(data, dtype=numpy.uint8)
				#frame = numpy.reshape(tmp_frame, (120,160,3))
				#frame = ndimage.rotate(frame, -90)
				#frame = cv2.resize(frame,(480,640))
				#cv2.imshow("Client", frame)
				#if cv2.waitKey(1)&0xff == ord('q'):
           	 	#		raise KeyboardInterrupt
				#self.showFrame("Client",frame)
			except(KeyboardInterrupt):
				print self.hist
				self.close_event.set()
				self.getVideoThread.join()
				cv2.destroyAllWindows()
				print "Closed Video Feed"

	def showFrame(self , title , frame , wait = False ):	
		cv2.imshow(title, frame)
    		if wait:
        		while True:
           			if cv2.waitKey(0)&0xff==ord('q'):
              				break
        		cv2.destroyAllWindows()
    		else:
        		if cv2.waitKey(1)&0xff == ord('q'):
           	 			raise KeyboardInterrupt

   	def closeVideoClient(self):
   		#print "Closing Video Feed..."
   		self.close_event.set()

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
		try:
			data = s.recv(60000)
			#print "Got packet!"
			data = eval(data)
			queue.put(data)
		except(KeyboardInterrupt):
			print "Thread interupt..."
			close_event.set()
	print "Recieve Thread Closed"

if __name__ == "__main__":
	print "Start Video Thread!"
	video_client = Video_Client(3333)
	#while not video_client.close_event.is_set():
	#	try:
#			time.sleep(1)
#		except(KeyboardInterrupt):
#			video_client.closeVideoClient()
#			print video_client.hist
#
#			break
	

	'''s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind((HOST,PORT))
	s.settimeout(2)
	while True:
		try:
			data = s.recv(60000)
			tmp_frame = numpy.fromstring(data, dtype=numpy.uint8)
			frame = numpy.reshape(tmp_frame, (120,160,3))
			frame = ndimage.rotate(frame, -90)
			frame = cv2.resize(frame,(480,640))
			showImage("Client", frame)
		except socket.timeout:
			print "No data on network!"
		except (KeyboardInterrupt):
			print "Exiting video client..."
			break

	if __name__ == "__main__":
	i = 0
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind((HOST,PORT))
	q = Queue()
	print q.empty()
	run_event = threading.Event()
	close_event = threading.Event()
	run_event.set() 

	recieveThread = threading.Thread(target=recieveAndQueue, args=[q,run_event])
	print "Start Recieve Thread!"
	recieveThread.start()
	full_data = ''
	last_packet_num = -1
	while not close_event.is_set():
		try:
			if not q.empty():
				data = q.get()
				#print data[0]
				if data[0] == 0:
					full_data = data[1]
					last_packet_num = 0
					print "Reset frame!"
				elif data[0] == (last_packet_num + 1):
				#	print "Added packet"
				#	last_packet_num  = last_packet_num + 1
					full_data = ''.join([full_data,data[1]])
				print len(full_data),len(data[1]),data[0]
				if(len(full_data) == 921600 and last_packet_num == 63):
					print "SHOWING FRAME: {}".format(i)
					#i = i +1
					tmp_frame = numpy.fromstring(full_data, dtype=numpy.uint8)
					frame = numpy.reshape(tmp_frame, (480,640,3))
					showImage("Client", frame)
					full_data = ''
				
 		except(KeyboardInterrupt):
			print "Main loop interupt..."
			run_event.clear()
			print "Joining..."
			recieveThread.join()
			print "Dead..."
			cv2.destroyAllWindows()
			break

	if close_event.is_set():
		cv2.destroyAllWindows()
'''