import UDP_class as UDP

if __name__ == "__main__":
	UDP_client = UDP.UDP(0, "0.0.0.0", 6000)

	UDP_client.receive_loop_thread()
	#UDP_client.send_loop_thread("127.0.0.1", 5001)
	UDP_client.send_loop_thread("255.255.255.255", 5001)

	UDP_client.close_sockets()
