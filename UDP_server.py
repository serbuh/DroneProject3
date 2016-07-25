import UDP_class as UDP

if __name__ == "__main__":
	UDP_server = UDP.UDP(1, "0.0.0.0", 5000, "255.255.255.255", 6001)
	
	raw_input( "lets close sockets and threads" )
	
	UDP_server.close_UDP()
