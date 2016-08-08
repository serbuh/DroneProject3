import UDP_class as UDP
import traceback
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='GCS module')
	parser.add_argument('--drone_ip')
	args = parser.parse_args()
	if not args.drone_ip:
		drone_ip = "255.255.255.255"
	else:
		drone_ip = args.drone_ip
	print "UDP_Client: Open socket for generic UDP"
	UDP_client = UDP.UDP(0, "Generic", "0.0.0.0", 6000, drone_ip, 5001)
	print "UDP_Client: Start receive thread (Generic)"
	UDP_client.receive_loop_generic_thread()	

	try:
		msg = raw_input("Enter msg:")
		while msg != 'q':
			UDP_client.send_generic(msg)
			msg = raw_input("Enter msg:")

	except KeyboardInterrupt:
		print ":)"
	finally:
		#traceback.print_exc()
		UDP_client.close_UDP()
