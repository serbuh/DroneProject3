import socket
import cv2
import numpy
from threading import Thread
import json

HOST = ''
#PORT_VIDEO = 3333
PORT_TELEM = 3334

socket_telem = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#socket_video = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

socket_telem.bind((HOST,PORT_TELEM))
#socket_video.bind((HOST,PORT_VIDEO))

def getTelem():
	while 1:
		data_json = socket_telem.recv(60000)
		data_dict = json.loads(data_json)
		print data_dict

getTelemThread = Thread(target=getTelem, args=())
getTelemThread.start()

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
