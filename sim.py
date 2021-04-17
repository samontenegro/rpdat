import numpy as np
import source.heartbeat as hb
import source.atcore as at
import source.precomputed as pc
import h5py
from enums.enums import SimStatus, Constants

class SimBroker:
	# this class simulates an exchange broker, feeding market prices one at a time
	# using validation data, and timed by a Heartbeat timer.

	def __init__(self, validation_data, heartbeat_ref):
		self.market_price = None
		self.orders_dict = [] # orders to be processed by the SimOrderQueue instance
		self.listeners = {}
		self.validation_data = validation_data
		self.simulation_status = SimStatus.BEGIN

		# frame counter marks 0 upon first update
		self.frame_counter = -1

		# reference to heartbeat timer
		self.heartbeat = heartbeat_ref

	def set_order(self, order):
		pass

	def cancel_order(self):
		pass

	def update_orders(self):
		pass

	def update(self):

		#### DEBUG print("SimBroker::update")

		# transition from initial state to actually simulating
		if self.simulation_status == SimStatus.BEGIN:
			self.simulation_status = SimStatus.ACTIVE

		# perform update instructions
		if self.simulation_status == SimStatus.ACTIVE:

			# update counter
			self.frame_counter += 1
			
			# check for end of validation data
			self.check_simulation()

			#### DEBUG print("SimBroker::update simulation status", self.simulation_status, self.frame_counter)

			# do update ops
			self.update_orders()
			self.update_market_price()

	def check_simulation(self):
		if self.frame_counter >= len(self.validation_data):
			self.simulation_status = SimStatus.STOP
			self.heartbeat.stop_timer()

	def update_market_price(self):
		if self.simulation_status == SimStatus.ACTIVE:
			self.market_price = self.validation_data[self.frame_counter]
			self.dispatch_listeners(self.market_price)

	def get_market_price(self):
		return self.market_price

	# Dispatch system; maybe use module "interface" in the future to not repeat this code? It's already implemented in heartbeat.py
	def dispatch_listeners(self, data):
		for key in self.listeners:
			if callable(self.listeners[key]):
				try:
					listener = self.listeners[key]
					#### DEBUG print("SimBroker::dispatch_listeners dispatching ", key)
					listener(data)
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

# Main excecution
if __name__ == "__main__":

	g_update_period = 0.5
	g_window_size = 30
	g_path_to_dataset = "precomputed/event_windows.hdf5"
	g_path_to_validation = "data/validation.hdf5"
	g_exchange_name = "gemini"
	g_symbol_name = "ethusd"
	initial_funds = {"eth": 0.05, "usd": 200}


	# load validation data; lets NOT hardcode this huh
	f = h5py.File(g_path_to_validation)

	# data comes reversed (new-to-old), we have to flip it!
	validation_data = np.array(f["data/exchange/gemini/symbols/ethusd/price_data"], dtype=np.float64)[::-1]
	f.close()

	# load precomputed instance
	prec = pc.Precomputed(g_path_to_dataset, g_exchange_name, g_symbol_name)

	# create heartbeat instance
	heartbeat = hb.Heartbeat(g_update_period)
	broker = SimBroker(validation_data, heartbeat)

	# create autotrader instance and initialize
	trader = at.Autotrader(initial_funds, g_symbol_name, g_window_size, prec, heartbeat)

	# cross register instances
	broker.register_listener("trader_update", trader.update_buffer)
	heartbeat.register_listener("sim_broker", broker.update)

	# start instance
	heartbeat.start_timer()