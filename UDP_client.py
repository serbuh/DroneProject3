import UDP_class as UDP

if __name__ == "__main__":
	UDP_client = UDP.UDP(0, "0.0.0.0", 6000, "255.255.255.255", 5001)

	raw_input( "lets close sockets and threads" )

	UDP_client.close_UDP()
