import flycapture2 as fc2
import numpy as np
import cv2


class Camera:
	# init camera instance and start capture
	def __init__(self):
		self.camera = fc2.Context()
		self.camera.connect(*(self.camera).get_camera_from_index(0))
		self.camera.set_video_mode_and_frame_rate(fc2.VIDEOMODE_1280x960Y16,fc2.FRAMERATE_7_5)
		self.camera.start_capture()

	# get color frame from camera as numpy array
	def getFrame(self,iscolor):
		frame = fc2.Image()
    		self.camera.retrieve_buffer(frame)
    		a = np.array(frame)
		#cv2.imshow("1",a)
		#while max(a.shape) > 1000:
        	#	a = cv2.pyrDown(a)
		
		if iscolor:
			return cv2.resize((cv2.cvtColor(a, cv2.COLOR_BayerGR2BGR)),(300, 240))
		else:
			return a

	
