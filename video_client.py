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
from PIL import Image
from PIL import ImageTk

HOST = ''
PORT = 3333


class Video_Client:
	def __init__(self,ShowVideo,Port , lbl_video = None ,Host = ''):
		print "Video Client - Start Video init"
		self.port = Port
		self.host = Host
		self.showVideo = ShowVideo
		self.lbl_video = lbl_video
		self.socket =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.socket.bind((HOST,PORT))
		self.socket.settimeout(2)
		self.close_event = threading.Event() 
		self.getVideoThread = threading.Thread(target=self.getVideo, args=[])
		self.getVideoThread.start()
		print "Video Client - Finish Video init"


	def getVideo(self):
		while not self.close_event.is_set():
			try:
				#print "Getting Frame"
				data = self.socket.recv(60000)
				tmp_frame = numpy.fromstring(data, dtype=numpy.uint8)
				frame = numpy.reshape(tmp_frame, (60,80,3))
				frame = ndimage.rotate(frame, -90)
				frame = cv2.resize(frame,(240,320))
				image = Image.fromarray(frame)
				image = ImageTk.PhotoImage(image)
				self.lbl_video.imgtk = image 
				self.lbl_video.configure(image=image)
				if self.showVideo:
					self.showImage("Client", frame)
			except socket.timeout:
				print "Video Client - No data on network!"
			except (KeyboardInterrupt):
				print "Video Client - Exiting video client..."
				break
		cv2.destroyAllWindows()
		print "Video Client - Closed Video Feed"


	def showImage(self , title , frame , wait = False ):	
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
   		print "Video Client - Close event set! Waiting for video feed to close..."
   		self.getVideoThread.join()

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
	video_client = Video_Client(True,3333)
	

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