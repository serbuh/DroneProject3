from datetime import datetime
from sys import maxint
import socket
import time
import cv2
from camera import *
import numpy as np
from Queue import Queue
from ball_tracking_2 import *
from time import sleep
import threading
import traceback

HOST = '192.168.12.95'
PORT = 3333



class Video_Server:
	def __init__(self,Port , Host):
		self.port = Port
		self.host = Host
		self.socket =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		print "Waiting for the camera"
		self.camera = Camera()
		print "Camera found, starting thread"
		self.close_event = threading.Event()
		#self.getVideoThread = threading.Thread(target=self.getVideo , args=()) 
		self.sendVideoThread = threading.Thread(target=self.sendVideo, args=())
		self.sendVideoThread.start()
		#self.getVideoThread.start()
		#self.queue = 
		self.frame_num = -1

	def sendVideo(self):
		time_prev = datetime.now()
		while not self.close_event.is_set():
			try:
				frame = self.camera.getFrame(True)
				#frame = cv2.resize(redBallTracking(frame),(160, 120))	
				self.frame_num += 1
				frame = cv2.resize(frame,(160,120))
				frame = frame.flatten()
				data = frame.tostring()
				data_list = list(self.chunkString(data,14400))
				for i in range(0,len(data_list)):
					#print "Sending: Frame index = {} , Chunk index = {}".format(self.frame_num,i)
					self.socket.sendto(str((self.frame_num,i,data_list[i])),(HOST,PORT))
					time_now = datetime.now()
					time_delta = time_now - time_prev
					print str(time_now) + ": delta: " + str(time_delta) + " Frame: {} , Chunk: {}".format(self.frame_num,i)
					time_prev = time_now
				if self.frame_num == 100:
					self.time_first = time_now
				if self.frame_num == 300:
					self.time_second = time_now
					self.closeVideoServer()		
			except (KeyboardInterrupt):
				print "Exiting video server..."
				break
			except:
				traceback.print_exc()		
		print "Closed Video Feed"
		print str(self.time_second - self.time_first)

	def showImage(self,title , frame , wait = False ):	
		cv2.imshow(title, frame)
	    	if wait:
	        	while True:
	           		if cv2.waitKey(0)&0xff==ord('q'):
	              			break
	        	cv2.destroyAllWindows()
	    	else:
	        	if cv2.waitKey(1)&0xff == ord('q'):
	            		raise KeyboardInterrupt

	def closeVideoServer(self):
		print "Closing Video Feed..."
   		self.close_event.set()
   		#threading.enumerate()
		#self.sendVideoThread.join()
   		#threading.enumerate()
		print "Send Thread Killed"
		self.camera.disconnect()
		print "Camera Disconected"


	def chunkString(self ,string, length):
    		return (string[0+i:length+i] for i in range(0, len(string), length))

def chunk(frame_queue,chunks_queue, run_event):
	try:
		while run_event.is_set():
			if not frame_queue.empty():
				data = frame_queue.get()
				data = list(chunkstring(data,14400))
				for i in range(0,64):
					chunks_queue.put(data[i])
					#l = l + len(data[i])
					#s.sendto(pack,(HOST,PORT))
					#print len(pack),i
				print "sent: " + str(datetime.now())

				#print l , i
	except KeyboardInterrupt:
		print "Thread interupt..."	
		close_event.set()	
	print "Chunk Thread Close"
		
def send(chunks_queue,socket, run_event):
	try:
		while run_event.is_set():
			if not chunks_queue.empty():
				for i in range(0,64):
					pack = chunks_queue.get()
					pack = str((i,pack))
					socket.sendto(pack,(HOST,PORT))
				#print "sent: " + str(datetime.now())
				#print l , i
	except KeyboardInterrupt:
		print "Thread interupt..."	
		close_event.set()	
	print "Send Thread Close"
	
if __name__ == "__main__":
	print "Video Send Main Loop Start "
	try:
		video_server = Video_Server(3333,'192.168.12.95')
		while True:
			time.sleep(1)
	except (KeyboardInterrupt):
		video_server.closeVideoServer()

	except:
		traceback.print_exc()
	print "Video Main Loop Ended"
			
		
