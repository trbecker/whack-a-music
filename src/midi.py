from pygame import midi
from threading import Thread
from time import sleep


class MidiController(Thread):
	def __init__(self, device=0, instrument=0):
		Thread.__init__(self)
		midi.init()
		self.mout = midi.Output(device)
		self.mout.set_instrument(instrument, 1)
		self.queue = []
		self.current_time = 0

	def loop(self):
		for event in self.queue:
			(time, tone, volume) = event
			if time <= self.current_time:
				self.queue.remove(event)
				if type(tone) == list:
					for n in tone:
						self.mout.note_off(n, volume, 1)
				else:
					self.mout.note_off(tone, volume, 1)

		sleep(0.1)
		self.current_time += 0.1

	def run(self):
		while True:
			self.loop()

	def play(self, note, duration, volume=127):
		print "playing", note, "for", duration
		self.queue.append((self.current_time + duration, note, volume))
		if type(note) == list:
			for n in note:
				self.mout.note_on(n, volume, 1)		
		else:
			self.mout.note_on(note, volume, 1)
