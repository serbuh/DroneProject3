import socket

MAX_BUFF_SIZE = 60000

class GCS_UDP_client:
	def __init__(self):
		self.my_socket = None

	def connect(self,host,port):
		self.my_socket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
		self.my_socket.bind((host,port))		
		print "Connected!"

	def receive(self):
		return self.my_socket.recv(MAX_BUFF_SIZE) 
