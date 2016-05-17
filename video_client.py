import socket
import cv2
import numpy
import copy
import ball_tracking_2

HOST = ''
PORT = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

while True:
	try:
		#data = ""
		#n = 1000
		#frame = []
		#for i in range(0,n):
		data = s.recv(66000)
		frame = numpy.fromstring(data, dtype=numpy.uint8)
		frame = numpy.reshape(frame, (120,180,3))
		z = copy.deepcopy(frame)
		z = cv2.resize(z,(640,480))
		#print z.shape
		cv2.imshow("Client", z)
		if cv2.waitKey(1)&0xff == ord('q'):
 				raise KeyboardInterrupt()
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		break
