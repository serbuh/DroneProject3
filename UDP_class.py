'''
UDP class.
See use exapmle in the main.
'''

import socket
import sys
import time
import threading
import struct
import traceback

class UDP():
### INIT ->
	def __init__(self, is_server, UDP_type, host, port_send, host_sendto, port_sendto):
		self.is_server = is_server
		if (is_server == 1):
			self.UDP_type = "UDP Server (drone) " + str(UDP_type)
		else:
			self.UDP_type = "UDP Client (GCS) " + str(UDP_type)

		self.host = host
		self.port_send = port_send
		self.port_receive = port_send + 1

		self.host_sendto = host_sendto
		self.port_sendto = port_sendto

		self.event_stop_send = threading.Event()
		self.event_stop_receive = threading.Event()

		self.sock_send = self.sock_create(self.host, self.port_send)
		self.sock_receive = self.sock_create(self.host, self.port_receive)
		
		self.send_thread = None
		self.receive_thread = None

		#self.receive_loop_thread()
		#self.send_loop_thread(host_sendto,port_sendto)

	def sock_create(self, host, port):
		print self.UDP_type + ": Open Socket. Host: " + str(host) + " Port: " + str(port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sec     = int(1)
		usec    = int(0 * 1e6)
		timeval = struct.pack('ll', sec, usec)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
		sock.setblocking(True)

		sock.bind((host, port))
		return sock

### -> INIT
### SEND ->

	def send_loop(self, host, port, event_stop_send):
		addr_send = (host, port)
		counter = 0
		while not event_stop_send.is_set():
			data_send = str(counter)
			counter = counter + 1
			self.sock_send.sendto(data_send, addr_send)
			#print self.UDP_type + ": Sent to: " + str(addr_send) + " Message: " + str(data_send)
			time.sleep(1)

	def send_loop_thread(self, host, port):
		print self.UDP_type + ": Start send thread. Sending to: " + str(host) + ":" + str(port)
		self.send_thread = threading.Thread(target=self.send_loop, args=(host, port, self.event_stop_send))
		self.send_thread.start()

	def send_once(self, data):
		addr_send = (self.host_sendto, self.port_sendto)
		self.sock_send.sendto(data, addr_send)
		#print self.UDP_type + ": Sent to: " + str(addr_send) + " Message: " + str(data)

	def send_telem(self, data_dict):
		data_str = str(data_dict)
		addr_send = (self.host_sendto, self.port_sendto)
		self.sock_send.sendto(data_str, addr_send)

	def send_cmd(self, data_list):
		data_str = str(data_list)
		addr_send = (self.host_sendto, self.port_sendto)
		self.sock_send.sendto(data_str, addr_send)
	
	def send_report(self, data):
		data_str = str(data)
		addr_send = (self.host_sendto, self.port_sendto)
		self.sock_send.sendto(data_str, addr_send)

### -> SEND
### RECEIVE ->

	def receive_loop_cmd(self, stop_receive_event, vehicle_controll):
		while not stop_receive_event.is_set():
			try:
				data_receive, addr = self.sock_receive.recvfrom(1024)
				#print self.UDP_type + ": Received from: " + str(addr) + " Message: " + str(data_receive)
				data_list = eval(data_receive)
				#print data_receive, type(data_receive)
				#print data_list, type(data_list)
				vehicle_controll.send_command_list(data_list)
			except socket.error:
				#print self.UDP_type + ": Timeout. No received user commands"
				continue
			except:
				traceback.print_exc()

	def receive_loop_telem(self, stop_receive_event, val_dict):
		while not stop_receive_event.is_set():
			try:
				data_receive, addr = self.sock_receive.recvfrom(1024)
				#print self.UDP_type + ": Received from: " + str(addr) + " Message: " + str(data_receive)
				data_dict = eval(data_receive)
				#print data_dict

				for rec_key, rec_val in data_dict.iteritems():
					if val_dict.has_key(rec_key):
						val_dict[rec_key]['value'] = rec_val
					else:
						print 'GCS WARNING: Trying to update not existing item in val_dict: ' + str(rec_key) + ' Message ' + str(rec_val)
			except socket.error:
				#print self.UDP_type + ": Timeout. No received telem messages"
				continue
			except:
				traceback.print_exc()

	def receive_loop_video(self, stop_receive_event, queue):
		while not stop_receive_event.is_set():
			try:
				data_receive, addr = self.sock_receive.recvfrom(60000)
				data_eval = eval(data_receive)
				queue.put(data_eval)
			except socket.error:
				#print self.UDP_type + ": Timeout. No received video messages"
				continue
			except:
				traceback.print_exc()
	
	def receive_loop_report(self, stop_receive_event):
		while not stop_receive_event.is_set():
			try:
				data_receive, addr = self.sock_receive.recvfrom(1024)
				#print self.UDP_type + ": Received from: " + str(addr) + " Message: " + str(data_receive)
				print self.UDP_type + ": " + str(data_receive)

			except socket.error:
				#print self.UDP_type + ": Timeout. No received report messages"
				continue
			except:
				traceback.print_exc()

	def receive_loop_report_thread(self):
		print self.UDP_type + ": Start receive Drone Reports thread. Listening to: " + str(self.port_receive)
		self.receive_thread = threading.Thread(target=self.receive_loop_report, args=(self.event_stop_receive,))
		self.receive_thread.start()

	def receive_loop_cmd_thread(self, vehicle_controll):
		print self.UDP_type + ": Start receive Commands thread. Listening to: " + str(self.port_receive)
		self.receive_thread = threading.Thread(target=self.receive_loop_cmd, args=(self.event_stop_receive, vehicle_controll))
		self.receive_thread.start()

	def receive_loop_telem_thread(self, val_dict):
		print self.UDP_type + ": Start receive Telemetry thread. Listening to: " + str(self.port_receive)
		self.receive_thread = threading.Thread(target=self.receive_loop_telem, args=(self.event_stop_receive, val_dict))
		self.receive_thread.start()

	def receive_loop_video_thread(self,queue):
		print self.UDP_type + ": Start receive video thread. Listening to: " + str(self.port_receive)	
		self.receive_thread = threading.Thread(target=self.receive_loop_video, args=(self.event_stop_receive, queue))
		self.receive_thread.start()

	def receive_once(self):
		data_receive, addr = self.sock_receive.recvfrom(1024)
		print self.UDP_type + ": Received from: " + str(addr) + " Message: " + str(data_receive)

### -> RECEIVE
### CLOSE ->

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
		if (self.send_thread is not None) and (self.send_thread.is_alive()):
			self.send_loop_thread_stop()
		if (self.receive_thread is not None) and (self.receive_thread.is_alive()):
			self.receive_loop_thread_stop()
		self.sock_send.close()
		self.sock_receive.close()
		print self.UDP_type + ": Close UDP. Sockets closed: Send port: " + str(self.port_send) + " Receive port: " + str(self.port_receive)

### -> CLOSE


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
