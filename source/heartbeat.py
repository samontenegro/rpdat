import threading
import time

class Heartbeat:
	def __init__(self, period):
		self.is_timing = False
		self.listeners = {}
		self.set_timer_period(period)

	def start_timer(self):
		if self.is_timing == False:
			t = threading.Thread(target=self.timing, args=(self.dispatch_listeners,))
			self.is_timing = True
			t.start()
		else:
			print("Heartbeat::start_timer There's already a timer running on this instance")

	def stop_timer(self):
		self.is_timing = False
		print("Heartbeat::stop_timer timer halt requested")

	def timing(self, timing_callback):
		while self.is_timing:
			time.sleep(self.timer_period)

			# re-check in case this changes while sleeping the thread
			if self.is_timing:
				timing_callback()
		print("Heartbeat::timing timer execution ended")

	def dispatch_listeners(self):
		if self.is_timing:
			for key in self.listeners:
				if callable(self.listeners[key]):
					try:
						listener = self.listeners[key]
						listener()
					except Exception as e:
						# exceptions are being ignored... for now
						raise e

	def unregister_listener(self, listener_id):
		if listener_id in self.listeners:
			self.listeners.pop(listener_id)

	def register_listener(self, listener_id, callback):
		if listener_id not in self.listeners:
			self.listeners[listener_id] = callback
		else:
			raise ValueError

	def set_timer_period(self, period):
		if not self.is_timing:
			# safety check
			if period > 1e-2:
				self.timer_period = period # timer_period per second
			else:
				self.timer_period = 1
		else:
			print("Heartbeat::set_timer_period period can't be changed while timing")