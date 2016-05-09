import socket
import sys
#import cv2
#import numpy
from threading import Thread
import json

def get_telem():
	while True:
		data_json = socket_telem.recv(60000)
		#data_dict = json.loads(data_json)		
		print data_json

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
		
		print("Creating thread to get UDP messages ...")
		#get_telem_thread = Thread(target=get_telem, args=())
		#get_telem_thread.start()
		get_telem()
		print("Done")

	except KeyboardInterrupt:
		socket_telem.close()
		print "\nStoooooop UDP GCS client"
		sys.exit()
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
