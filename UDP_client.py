import UDP_class as UDP
import traceback

if __name__ == "__main__":
	try:
		UDP_client = UDP.UDP(0, "0.0.0.0", 6000, "255.255.255.255", 5001)
		#UDP_client.receive_loop_msg_thread()
		UDP_client.receive_loop_telem_thread(None)
		msg = raw_input("Enter msg:")
		while msg != 'q':
			UDP_client.send_telem(msg)
			msg = raw_input("Enter msg:")

	except KeyboardInterrupt:
		pass
	finally:
		#traceback.print_exc()
		UDP_client.close_UDP()
