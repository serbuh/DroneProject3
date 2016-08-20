from datetime import datetime
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
	def __init__(self,Vehicle_Control,Port,Host):
		self.port = int(Port)
		self.host = Host
		self.vehicle_control = Vehicle_Control
		self.socket =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.camera = Camera()
		self.close_event = threading.Event() 
		self.sendVideoThread = threading.Thread(target=self.sendVideo, args=())
		self.sendVideoThread.start()


	def sendVideo(self):
		while not self.close_event.is_set():
			try:
				if self.vehicle_control.video_on:
					frame = self.camera.getFrame(True)
					if self.vehicle_control.rb_tracking_on:
						frame = cv2.resize(redBallTracking(self.vehicle_control,frame),(80,60))
					else:	
						frame = cv2.resize(frame,(80,60))
					frame = frame.flatten()
					data = frame.tostring()
					self.socket.sendto(data,(self.host,self.port))
				else:
					time.sleep(1)		
			except (KeyboardInterrupt):
				print "Exiting video server..."
				break
			except:
				traceback.print_exc()		
		print "Closed Video Feed"

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
		self.sendVideoThread.join()
   		#threading.enumerate()
		print "Send Thread Killed"
		self.camera.disconnect()
		print "Camera Disconected"


def chunkstring(string, length):
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
		video_server = Video_Server(None,3333,'192.168.24.251')
		while True:
			time.sleep(1)
	except (KeyboardInterrupt):
		video_server.closeVideoServer()

	except:
		traceback.print_exc()
	print "Video Main Loop Ended"
			
		
