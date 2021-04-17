import numpy as np
import utility.data_statistics as ds
from enums.enums import ScoreCategory, Constants, TraderStatus


class Autotrader:
	
	# self.funds (dictionary for holding values in each token)
	# self.data_buffer np array of window_size for computing pearson correlation against precomputed windows

	def __init__(self, funds_dict, symbol, buffer_size, precomputed, heartbeat_ref):

		self.frame_counter = 0
		self.symbol = symbol
		self.buffer_size = buffer_size
		self.trader_status = TraderStatus.NONE

		# instance of Precomputed class
		self.precomputed = precomputed

		# instantiate buffer
		self.data_buffer = np.zeros(self.buffer_size)

		# initialize funds dictionary
		if len(funds_dict) > 0 and isinstance(funds_dict, dict):
			self.funds = funds_dict

		# placeholder for broker
		self.broker_ref = None
		self.heartbeat = heartbeat_ref

	def update_funds(self, fund_key, delta):
		if fund_key in self.funds:
			self.funds[fund_key] += delta

		self.check_funds()

	def check_funds(self):
		# find some way to check if funds are completely zero
		pass

	def open_trade(self, order_op, ):
		if self.trader_status == TraderStatus.NONE and self.broker_ref != None:
			# TODO: self.broker_ref.set_order()


	def close_trade(self):
		pass

	def update_trade(self):
		pass

	def register_broker(self, broker_ref):
		pass

	def is_ready(self):
		return self.frame_counter > self.buffer_size

	def update_buffer(self, new_value):

		self.data_buffer[0:self.buffer_size - 1] = self.data_buffer[1:self.buffer_size] # shift values right
		self.data_buffer[self.buffer_size - 1] = new_value # set new value
		self.frame_counter += 1 # update frame counter

		#### DEBUG print("Autotrader::update_buffer", new_value, self.is_ready())

		if self.is_ready():
			self.evaluate_window()

	def evaluate_window(self):
		
		# this method evaluates how similar the (rescaled) current data_buffer is to previous values
		rescaled_buffer = ds.rescale_vector(self.data_buffer)
		correlations, max_correlation_index = ds.compute_correlations(self.precomputed.event_windows, rescaled_buffer)

		# determine score category
		score_category = ScoreCategory.ACCEPTABLE if (correlations[max_correlation_index] >= Constants.THRESHOLD.value) else ScoreCategory.UNACCEPTABLE

		if score_category == ScoreCategory.ACCEPTABLE:
			estimated_frame_delay = ds.cutoff_weighted_average(correlations, self.precomputed.event_windows["true_minima_offset"], Constants.THRESHOLD.value)

			print("Autotrader::evaluate_window correlation score acceptable!", correlations[max_correlation_index], estimated_frame_delay, self.data_buffer[self.buffer_size - 1])
			pass
			# place order with broker using estimated true_minima_position