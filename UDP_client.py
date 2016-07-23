'''
UDP Client.
'''
import socket
import sys
import time

class UDP_client():
	def __init__(self, host_client, port_client):
		self.sock_send = self.sock_create(host_client, port_client)
		self.sock_receive = self.sock_create(host_client, port_client + 1)
		print "UDP Client: Started."

	def sock_create(self, host, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		
		# Explicit bind. Not neccesary. An automatic bind() will take place on the first 
		# send()/sendto()/recv()/recvfrom() using a system-assigned local port number.
		# MY_HOST, MY_PORT = "127.0.0.1", 5001
		# s.bind((MY_HOST, MY_PORT))
		sock.bind((host, port))
		return sock

	def receive_and_send(self, host_server, port_server_receive):
		addr_send = (host_server, port_server_receive)
		data_send = raw_input("->")
		while data_send != 'q':
			self.sock_send.sendto(data_send, addr_send)
			data_receive, addr = self.sock_receive.recvfrom(1024)
			print "UDP Client: Received from: " + str(addr_send) + " Message: " + str(data_receive)
			send_data = raw_input("->")

	def receive_loop(self):
		while True:
			data_receive, addr = self.sock_receive.recvfrom(1024)
			print "UDP Client: Recieved from: " + str(addr) + " Message: " + str(data_receive)

	def send_loop(self, host_server, port_server_receive):
		addr_send = (host_server, port_server_receive)
		counter = 0
		while True:
			data_send = str(counter)
			counter = counter + 1
			self.sock_send.sendto(data_send, addr_send)
			print "UDP Client: Sent to: " + str(addr_send) + " Message: " + str(data_send)
			time.sleep(1)

	def send_once(self, host_server, port_server_receive):
		addr_send = (host_server, port_server_receive)
		data_send = "Yo!"
		self.sock_send.sendto(data_send, addr_send)
		print "UDP Client: Sent to: " + str(addr_send) + " Message: " + str(data_send)


	def close_sockets(self):
		self.sock_send.close()
		self.sock_receive.close()
		print "UDP client: Close socket."

if __name__ == '__main__':
	UDP_client = UDP_client("0.0.0.0", 6000)
	#UDP_client.send_loop("127.0.0.1", 5001)
	#UDP_client.send_once("127.0.0.1", 5001)
	UDP_client.receive_loop()
	UDP_client.close_sockets()

