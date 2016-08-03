import UDP_class as UDP
import traceback

if __name__ == "__main__":
	try:
		print "UDP Server: Open socket for generic UDP"
		UDP_server = UDP.UDP(1, "Generic", "0.0.0.0", 5000, "255.255.255.255", 6001)
		print "UDP Server: Start receive thread (Generic)"
		UDP_server.receive_loop_generic_thread()
		msg = raw_input("Enter msg:")
		while msg != 'q':
			UDP_server.send_generic(msg)
			msg = raw_input("Enter msg:")

	except KeyboardInterrupt:
		print ":)"
	finally:
		#traceback.print_exc()
		UDP_server.close_UDP()
