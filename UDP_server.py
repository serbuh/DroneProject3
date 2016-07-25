import UDP_class as UDP
import traceback

if __name__ == "__main__":
	try:
		UDP_server = UDP.UDP(1, "0.0.0.0", 5000, "255.255.255.255", 6001)
		#UDP_server.receive_loop_msg_thread()
		UDP_server.receive_loop_telem_thread(None)
		msg = raw_input("Enter msg:")
		while msg != 'q':
			UDP_server.send_telem(msg)
			msg = raw_input("Enter msg:")

	except KeyboardInterrupt:
		print ":)"
	finally:
		#traceback.print_exc()
		UDP_server.close_UDP()
