from looper import Looper
from time import sleep
import psmove

class MoveTracker(Looper):
	def __init__(self, delay=0.05):
		Looper.__init__(self, name="Move Tracker")
		self.position = (0, 0, 0)

		self.tracker = psmove.PSMoveTracker()

		self.moves = []
		self.delay = delay

	def add_move(self, move, callback):
		result = -1
		while result != psmove.Tracker_CALIBRATED:
			print "Calibrating controller"
			result = self.tracker.enable(move)

		self.moves.append((move, callback))

	def loop(self):
		self.tracker.update()
		self.tracker.update_image()
		for (move, callback) in self.moves:
			callback(self, self.tracker.get_position(move))

		sleep(self.delay)
