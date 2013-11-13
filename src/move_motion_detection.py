import psmove
import looper
import time

class MotionDetector(looper.Looper):
	def __init__(self, move, delay=0.05):
		self.move = move
		self.detectors = []
		self.delay = delay

		looper.Looper.__init__(self, name="Motion Detector")

	def add_detector(self, detector):
		self.detectors.append(detector)

	def remove_detector(self, detector):
		self.detector.remove(detector)

	def detect(self):
		if move.poll():
			acceleromter = move.get_accelerometer_frame(psmove.Frame_SecondHalf)
			magnetometer = move.get_magnetometer_vector(psmove.Frame_SecondHalf)
			gyroscope    = move.get_gyroscope_frame(psmove.Frame_SecondHalf)
			buttons      = move.get_buttons()

			for detector in detectors:
				if detector(self, acceleromter, magnetometer, gyroscope, buttons):
					self.callback(self, acceleromter, magnetometer, gyroscope, buttons)

	def callback(self, *args):
		pass

	def loop(self):
		self.detect()
		time.sleep(self.delay)


