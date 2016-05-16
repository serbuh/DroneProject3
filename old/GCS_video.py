'''
Executed from as main.
UDP client that invokes GUI
'''
import socket
import sys
#import cv2
#import numpy
import threading
import json
import time

def get_telem(run_event):
	while run_event.is_set():
		data_json = socket_telem.recv(60000)
		#data_dict = json.loads(data_json)		
		print data_json

def get_video(run_event):
	pass

def run_GUI(run_event):
	import GCS_GUI

if __name__ == "__main__":
	try:
		try:
			print("Creating UDP socket ...")
			socket_telem = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			#socket_video = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		except socket.error:
			print("Failed to create socket")
			sys.exit()

		try:
			HOST = 'localhost'
			PORT_TELEM = 3334
			#PORT_VIDEO = 3333
			
			print("Binding socket to host {} and port {} ...".format(HOST,PORT_TELEM))
			socket_telem.bind((HOST,PORT_TELEM))
			#socket_video.bind((HOST,PORT_VIDEO))
		except socket.error , msg:
			print 'Socket bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		
		run_event = threading.Event()
		run_event.set()

		print("Start GET_TELEM Thread")
		get_telem_thread = threading.Thread(target=get_telem, args=[run_event])
		get_telem_thread.start()
		print("Start GET_VIDEO Thread")
		get_video_thread = threading.Thread(target=get_video, args=[run_event])
		get_video_thread.start()
		print("Start GUI Thread")
		run_GUI_thread = threading.Thread(target=run_GUI, args=[run_event])
		run_GUI_thread.start()
		
		while True:
			time.sleep(1)

	except (KeyboardInterrupt, SystemExit):
		print("Send event to all running threads to close")
		run_event.clear()
		# Wait for threads to die
		get_telem_thread.join()
		print("GET_TELEM dead")
		get_video_thread.join()
		print("GET_VIDEO dead")
		run_GUI_thread.join()
		print("GUI dead")
		socket_telem.close()
		print("Socket closed")
else:
	print("You are running GCS_client.py not as a main?")





'''
while True:
	try:
		data = socket_video.recv(60000)
		frame = numpy.fromstring(data, dtype=numpy.uint8)
		frame = numpy.reshape(frame, (120,160,3))
		#print "Recieved data:" + data
		cv2.imshow("Client", frame)
		if cv2.waitKey(1)&0xff == ord('q'):
 				raise KeyboardInterrupt()
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		break
'''
