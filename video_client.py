import socket
import cv2
import numpy
import copy


HOST = ''
PORT = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))

while True:
	try:
		print "Waiting for video..."
		data = s.recv(66000)
		tmp_frame = numpy.fromstring(data, dtype=numpy.uint8)
		tmp_frame = numpy.reshape(tmp_frame, (120,180,3))
		frame = copy.deepcopy(tmp_frame)
		frame = cv2.resize(frame,(640,480))
		cv2.imshow("Client", frame)
		if cv2.waitKey(1)&0xff == ord('q'):
 				raise KeyboardInterrupt()
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		break
