'''
UDP class.
See use exapmle in the main.
'''

import socket
import sys
import time
import threading


class UDP():
	def __init__(self, is_server, host, port_send, host_sendto, port_sendto):
		self.is_server = is_server
		if (is_server == 1):
			self.UDP_type = "UDP Server"
		else:
			self.UDP_type = "UDP Client"

		self.host = host
		self.port_send = port_send
		self.port_receive = port_send + 1

		self.event_stop_send = threading.Event()
		self.event_stop_receive = threading.Event()

		self.sock_send = self.sock_create(self.host, self.port_send)
		self.sock_receive = self.sock_create(self.host, self.port_receive)
		
		self.receive_loop_thread()
		self.send_loop_thread(host_sendto,port_sendto)

	def sock_create(self, host, port):
		print self.UDP_type + ": Open Socket. Host: " + str(host) + " Port: " + str(port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.setblocking(False)
		sock.bind((host, port))
		return sock


	def send_loop(self, host, port, event_stop_send):
		addr_send = (host, port)
		counter = 0
		while not event_stop_send.is_set():
			data_send = str(counter)
			counter = counter + 1
			self.sock_send.sendto(data_send, addr_send)
			print self.UDP_type + ": Sent to: " + str(addr_send) + " Message: " + str(data_send)
			time.sleep(1)

	def send_loop_thread(self, host, port):
		print self.UDP_type + ": Start send thread. Sending to: " + str(host) + ":" + str(port)
		self.send_thread = threading.Thread(target=self.send_loop, args=(host, port, self.event_stop_send))
		#self.send_thread.daemon = True
		self.send_thread.start()

	def send_once(self, host, port):
		addr_send = (host, port)
		data_send = "Yo!"
		self.sock_send.sendto(data_send, addr_send)
		print self.UDP_type + ": Sent to: " + str(addr_send) + " Message: " + str(data_send)


	def receive_loop(self, stop_receive_event):
		while not stop_receive_event.is_set():
			try:
				data_receive, addr = self.sock_receive.recvfrom(1024)
				print self.UDP_type + ": Received from: " + str(addr) + " Message: " + str(data_receive)
			except:
				time.sleep(0.5) # no message to receive

	def receive_loop_thread(self):
		print self.UDP_type + ": Start receive thread. Listening to: " + str(self.port_receive)
		#self.receive_thread = threading.Thread(target=self.receive_loop)
		self.receive_thread = threading.Thread(target=self.receive_loop, args=(self.event_stop_receive,))
		#self.receive_thread.daemon = True
		self.receive_thread.start()

	def receive_once(self):
		data_receive, addr = self.sock_receive.recvfrom(1024)
		print self.UDP_type + ": Received from: " + str(addr) + " Message: " + str(data_receive)


	def send_loop_thread_stop(self):
		self.event_stop_send.set()
		print self.UDP_type + ": Close UDP. Send loop: Event sent, wait for a stop."
		self.send_thread.join()
		print self.UDP_type + ": Close UDP. Send loop: Stoped."

	def receive_loop_thread_stop(self):
		self.event_stop_receive.set()
		print self.UDP_type + ": Close UDP. Receive loop: Event sent, wait for loop to stop."
		self.receive_thread.join()
		print self.UDP_type + ": Close UDP. Receive loop: Stoped."

	def close_UDP(self):
		self.send_loop_thread_stop()
		self.receive_loop_thread_stop()
		self.sock_send.close()
		self.sock_receive.close()
		print self.UDP_type + ": Close UDP. Sockets closed: Send port: " + str(self.port_send) + " Receive port: " + str(self.port_receive)

if __name__ == '__main__':
	print "UDP: WARNING. You ran the UDP class as a main. For test purposes only."
	UDP_server = UDP(1, "0.0.0.0", 5000)
	UDP_server.receive_loop_thread()
	UDP_server.send_loop_thread("255.255.255.255", 6001)

	UDP_client = UDP(0, "0.0.0.0", 6000)
	UDP_client.receive_loop_thread()
	UDP_client.send_loop_thread("255.255.255.255", 5001)

	UDP_server.close_sockets()
	UDP_client.close_sockets()
