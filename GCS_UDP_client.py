'''
UDP client class.
Can connect to the socket
and to receive data
'''

import socket

MAX_BUFF_SIZE = 60000

class GCS_UDP_client:
	def __init__(self):
		self.my_socket = None

	def connect(self,host,port):
		print "Creating UDP socket ...",
		try:		
			self.my_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		except socket.error:
			print("Failed to create socket")
			sys.exit()
		print "Done!"

		print("Binding socket to host {} and port {} ...".format(host,port)),
		try:
			self.my_socket.bind((host,port))
		except socket.error , msg:
			print 'Socket bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		print "Done!"

	def close_client(self):
		print "Closing socket ...",
		self.my_socket.close()
		print "Done!"

	def receive(self):
		return self.my_socket.recv(MAX_BUFF_SIZE)

