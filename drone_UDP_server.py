import socket
import time
import cv2
from camera import *
import numpy as np
from drone_FCU_utils import *

PORT_VIDEO = 3333

socket_video = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


def showImage(title , frame , wait = False ):	
	cv2.imshow(title, frame)
    	if wait:
        	while True:
           		if cv2.waitKey(0)&0xff==ord('q'):
              			break
        	cv2.destroyAllWindows()
    	else:
        	if cv2.waitKey(1)&0xff == ord('q'):
            		raise KeyboardInterrupt()

if __name__ == "__main__":
	camera = Camera()
	vehicle = connect2FCU()
	vehicle.add_attribute_listener('*', wildcard_callback)
	while True:
		frame = camera.getFrame(True)
		while max(frame.shape[:2]) > 310:
       			frame = cv2.pyrDown(frame)
		try:
			showImage("Server",frame)
			frame = frame.flatten()
			data = frame.tostring()
			print "SENT FRAME!"
			socket_video.sendto(data,(HOST,PORT_VIDEO))
		except KeyboardInterrupt:
			vehicle.remove_attribute_listener('*', wildcard_callback)
			print "\nClose vehicle object"
			vehicle.close()
			cv2.waitKey(0)
			c.stop_capture()
			c.disconnect()
			break
