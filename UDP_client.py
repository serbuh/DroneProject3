import UDP_class as UDP
import traceback

if __name__ == "__main__":
	try:
		print "UDP_Client: Open socket for generic UDP"
		UDP_client = UDP.UDP(0, "Generic", "0.0.0.0", 6000, "255.255.255.255", 5001)
		print "UDP_Client: Start receive thread (Generic)"
		UDP_client.receive_loop_generic_thread()
		msg = raw_input("Enter msg:")
		while msg != 'q':
			UDP_client.send_generic(msg)
			msg = raw_input("Enter msg:")

	except KeyboardInterrupt:
		print ":)"
	finally:
		#traceback.print_exc()
		UDP_client.close_UDP()
