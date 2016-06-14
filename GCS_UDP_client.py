'''
UDP client class.
Can connect to the socket
and to receive data
'''

import socket
import sys

MAX_BUFF_SIZE = 60000

class GCS_UDP_client:
	def __init__(self):
		self.my_socket = None

	def connect(self,host,port):
		print "UDP: Creating UDP socket ..."
		try:		
			self.my_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		except socket.error:
			print("UDP: Failed to create socket")
			sys.exit()

		print("UDP: Binding socket to host {} and port {} ...".format(host,port))
		try:
			self.my_socket.bind((host,port))
		except socket.error , msg:
			print 'UDP: Socket bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

	def close_client(self):
		print "UDP: Closing socket ..."
		self.my_socket.close()

	def receive(self):
		return self.my_socket.recv(MAX_BUFF_SIZE)

