#!/usr/bin/env python

from time import sleep
from threading import Thread, Timer

import pygame as pg
from pygame.locals import *
import midi

import psmove

class ControllerThread(Thread):
	def __init__(self, move, **kwargs):
		self.move = move
		self.running = False
		Thread.__init__(self)

	def run(self):
		self.running = True
		while self.running:
			self.loop()

	def loop(self):
		pass

	def stop(self):
		self.running = False
		Thread.stop(self)

class WhackDetector(ControllerThread):
	def __init__(self, move, threshold=5):
		self.threshold = threshold
		self.p0 = (0, 0, 0)
		self._whack = False
		self.running = True
		self.orientation_vector = (0, 0, 0)
		ControllerThread.__init__(self, move)

	def loop(self):
		if move.poll():
			p1 = move.get_accelerometer_frame(psmove.Frame_SecondHalf)
			self._whack = self.distance_squared(self.p0, p1) <= -self.threshold
			if (self._whack):
				print "WHACK!"
			self.p0 = p1

	def distance_squared(self, p1, p2):
		x1, y1, z1 = p1
		x2, y2, z2 = p2

		dx = x2 - x1
		dy = y2 - y1
		dz = z2 - z1

		self.orientation_vector = (dx, dy, dz)

		return dz

class Tracker(ControllerThread):
	def __init__(self, move):
		ControllerThread.__init__(self, move)
		self.position = (0, 0, 0)

		self.tracker = psmove.PSMoveTracker()

		result = -1
		while result != psmove.Tracker_CALIBRATED:
			print "Calibrating controller"
			result = self.tracker.enable(self.move)

	def loop(self):
		#print "Updating tracker"
		self.tracker.update()
		#print "Updating image"
		self.tracker.update_image()
		#print "Updating position"
		self.position = self.tracker.get_position(self.move)
		#print self.position
		#sleep(.1)


def rumble(move, intensity=120, time=.2):
	move.set_rumble(intensity)

	def unrumble():
		move.set_rumble(0)

	Timer(.2, unrumble).start()

if __name__ == '__main__':
	connected_moves = psmove.count_connected()

	print connected_moves, "moves detected"

	move = psmove.PSMove(0)

	if not move.has_calibration():
		print "Controller 0 is not calibrated"

	mout = midi.MidiController(2, 13)
	mout.start()

	whacker = WhackDetector(move, 1.5)
	whacker.start()

	tracker = Tracker(move)
	tracker.start()

	#screen = pg.display.set_mode((640, 480), DOUBLEBUF)
	#circle = pg.image.load('../res/circle.jpg')

	

	while True:
		if whacker._whack:
			rumble(move)
			mout.play(60, 0.5)
		
		#screen.fill((0, 0, 0))

		#x, y, r = tracker.position
		#screen.blit(circle, (640 - x, y))
		#pg.display.flip()
 
		sleep(1/60.0)

	whacker.running = False