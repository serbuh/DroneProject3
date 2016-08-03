import UDP_class as UDP
import traceback
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='GCS module')
	parser.add_argument('gcs_ip')
	args = parser.parse_args()
	if not args.gcs_ip:
		gcs_ip = "255.255.255.255"
	else:
		gcs_ip = args.gcs_ip
	print "UDP Server: Open socket for generic UDP"
	UDP_server = UDP.UDP(1, "Generic", "0.0.0.0", 5000, gcs_ip, 6001)
	print "UDP Server: Start receive thread (Generic)"
	UDP_server.receive_loop_generic_thread()
			
	try:
		msg = raw_input("Enter msg:")
		while msg != 'q':
			UDP_server.send_generic(msg)
			msg = raw_input("Enter msg:")

	except KeyboardInterrupt:
		print ":)"
	finally:
		#traceback.print_exc()
		UDP_server.close_UDP()
