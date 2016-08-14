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


HOST = '192.168.12.95'
PORT = 3333



class Video_Server:
	def __init__(self,Port , Host):
		self.port = Port
		self.host = Host
		self.socket =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.camera = Camera()
		self.close_event = threading.Event() 
		self.sendVideoThread = threading.Thread(target=self.sendVideo, args=())
		self.sendVideoThread.start()


	def sendVideo(self):
		while not self.close_event.is_set():
			try:
				frame = self.camera.getFrame(True)
				#frame = cv2.resize(redBallTracking(frame),(160, 120))	
				frame = cv2.resize(frame,(160,120))
				frame = frame.flatten()
				data = frame.tostring()
				self.socket.sendto(data,(HOST,PORT))
						
			except (KeyboardInterrupt):
				print "Exiting video server..."
				break
			except:
            	traceback.print_exc()
            	break
				
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
   		self.sendVideoThread.join()
   		self.camera.disconnect()


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
	video_server = Video_Server(3333,'192.168.12.95')
	'''camera = Camera()
	#frame_queue = Queue()
	#chunks_queue = Queue()	
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	#run_event = threading.Event()
	#run_event.set() 	
	
	#chunkThread = threading.Thread(target=chunk, args=[frame_queue,chunks_queue,run_event])
	#sendThread = threading.Thread(target=send, args=[chunks_queue,s,run_event])
	#cap = cv2.VideoCapture(0)
	#run_event.set()	
	#print "Start Chunk Thread!"
	#chunkThread.start()	
	#print "Start Send Thread!"
	#sendThread.start()	
	while True:
		try:
			frame = camera.getFrame(True)
			#ret, frame = cap.read()
			frame = cv2.resize(redBallTracking(frame),(160, 120))
			#frame = cv2.resize(frame,(160,120))	
			#showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			#frame_queue.put(data)
			#sleep(0.1)
			s.sendto(data,(HOST,PORT))
			#print "main!"			
					
		except KeyboardInterrupt:
			print "closing video server..."
			break
			rint "MAIN LOOP INTERUPT!"
			run_event.clear()
			print "joining chunking..."
			chunkThread.join()
			print "dead.."
			print "joining sending..."
			sendThread.join()
			print "dead.."
			break		
			#cv2.destroyAllWindows()			
			
	#if close_event.is_set():
	#	print "Cleaning..."
	#	cv2.destroyAllWindows()
	'''
