import socket
import cv2
import numpy

HOST = '192.168.159.133'
PORT = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

while True:
	try:
		data = s.recv(66000)
		frame = numpy.fromstring(data, dtype=numpy.uint8)
		frame = numpy.reshape(frame, (120,160,3))
		cv2.imshow("Client", frame)
		if cv2.waitKey(1)&0xff == ord('q'):
 				raise KeyboardInterrupt()
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		break
