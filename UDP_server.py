'''
UDP server.
'''
import socket
import sys
import time

class UDP_server():
	def __init__(self, host_server, port_server_send):
		self.host_server = host_server
		self.port_server_send = port_server_send
		self.port_server_receive = port_server_send + 1
		self.sock_send = self.sock_create(self.host_server, self.port_server_send)
		self.sock_receive = self.sock_create(self.host_server, self.port_server_receive)
		print "UDP Server: Started. Send port: " + str(self.port_server_send) + " Receive port: " + str(self.port_server_receive)

	def sock_create(self, host, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((host, port))
		return sock

	def receive_and_send(self):
		while True:
			data_receive, addr = self.sock_receive.recvfrom(1024)
			print "UDP Server: Received from: " + str(addr) + " Message: " + str(data_receive)
			data_send = str(data_receive).upper()
			self.sock_send.sendto(data_send, addr)
			print "UDP Server: Sent to: " + str(addr) + " Message: " + str(data_send)

	def receive_loop(self):
		while True:
			data_receive, addr = self.sock_receive.recvfrom(1024)
			print "UDP Server: Received from: " + str(addr) + " Message: " + str(data_receive)

	def receive_once(self):
		data_receive, addr = self.sock_receive.recvfrom(1024)
		print "UDP Server: Received from: " + str(addr) + " Message: " + str(data_receive)

	def send_loop(self, host_client, port_client_receive):
		addr_send = (host_client, port_client_receive)
		counter = 0
		while True:
			data_send = str(counter)
			counter = counter + 1
			self.sock_send.sendto(data_send, addr_send)
			print "UDP Server: Sent to: " + str(addr_send) + " Message: " + str(data_send)
			time.sleep(1)

	def close_sockets(self):
		self.sock_send.close()
		self.sock_receive.close()
		print "UDP Server: Close socket. Send port: " + str(self.port_server_send) + " Receive port: " + str(self.port_server_receive)

if __name__ == '__main__':
	UDP_server = UDP_server("0.0.0.0", 5000)
	#UDP_server.receive_loop()
	#UDP_server.receive_once()		
	UDP_server.send_loop("127.0.0.1", 6001)
	UDP_server.close_sockets()
