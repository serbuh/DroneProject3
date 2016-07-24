import UDP_class as UDP

if __name__ == "__main__":
	UDP_server = UDP.UDP(1, "0.0.0.0", 5000)
	
	UDP_server.receive_loop_thread()
	#UDP_server.send_loop_thread("127.0.0.1", 6001)
	UDP_server.send_loop_thread("255.255.255.255", 6001)


	UDP_server.close_sockets()
