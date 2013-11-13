#!/usr/bin/env python

import psmove
import midi
import move_tracker

import signal

def dump_event(self, *args):
	print args

def signal_handler(s, stack_frame):
	if s == signal.SIG_INT:
		shutdown()
	
connected_moves = psmove.count_connected()

print connected_moves, "moves detected"

move = psmove.PSMove(0)

tracker = move_tracker.MoveTracker()
tracker.add_move(move, dump_event)
tracker.start()

if not move.has_calibration():
		print "Controller 0 is not calibrated"

mout = midi.MidiController(2, 13)
mout.start()

running = False

def shutdown():
	tracker.stop()
	mout.stop()
	running = False

if __name__ == '__main__':
	from time import sleep

	while running:
		sleep(10)

	