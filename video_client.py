import socket
import cv2
import numpy

HOST = ''
PORT = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

while True:
	try:
		data = ""
		for i in range(0,n-1):
			data = data + s.recv(1000)
		frame = numpy.fromstring(data, dtype=numpy.uint8)
		frame = numpy.reshape(frame, (120,160,3))
		cv2.imshow("Client", frame)
		if cv2.waitKey(1)&0xff == ord('q'):
 				raise KeyboardInterrupt()
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		break
