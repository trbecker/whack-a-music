from threading import Thread
from time import sleep

class Looper(Thread):
	def __init__(self, name="Looper"):
		Thread.__init__(self, name=name)
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			self.loop()

	def stop(self):
		self.running = False
		#Thread.stop(self)
		self.join()

	def loop(self):
		sleep(10)