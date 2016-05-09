import socket
#import cv2
#import numpy
from threading import Thread
import json

stop = 0
def get_telem():
	while not stop:
		data_json = socket_telem.recv(60000)
		#data_dict = json.loads(data_json)		
		print data_json

if __name__ == "__main__":
	try:
		HOST = ''
		#PORT_VIDEO = 3333
		PORT_TELEM = 3334

		socket_telem = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		#socket_video = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

		socket_telem.bind((HOST,PORT_TELEM))
		#socket_video.bind((HOST,PORT_VIDEO))


		get_telem_thread = Thread(target=get_telem, args=())
		get_telem_thread.start()

	except KeyboardInterrupt:
		socket_telem.close()
		stop = 1
		print "Stoooooop!"
		get_telem_thread.join()
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
