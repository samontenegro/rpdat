import numpy as np
import collections
from order import OrderCondition, Order
from enums.enums import OrderOp, OrderType, SimOrderQueueAction

class SimOrderQueue:
	def __init__(self):
		# array of orders to be finalized on some condition
		self.orders_to_finalize = []

		# map for determining handlers
		self.order_handler_map = {
			SimOrderQueueAction.EXECUTE: {
				OrderType.MARKET: 		self.execute_market_order,
				OrderType.STOP: 		self.execute_stop_order,
				OrderType.LIMIT: 		self.execute_limit_order,
				OrderType.STOP_LIMIT: 	self.execute_stop_limit_order
			},
			SimOrderQueueAction.FINALIZE: {
				OrderType.STOP: 		self.finalize_stop_order,
				OrderType.LIMIT: 		self.finalize_limit_order,
				OrderType.STOP_LIMIT: 	self.finalize_stop_limit_order
			}
		}

	def execute_order(order):
		

	def finalize_orders(self):
		pass

	def get_order_type_handler(self, action, type):
		pass

	# handlers per OrderType
	def execute_market_order(self):
		pass

	def execute_stop_order(self):
		pass

	def execute_limit_order(self):
		pass

	def execute_stop_limit_order(self):
		pass

	def finalize_stop_order(self):
		pass

	def finalize_limit_order(self):
		pass

	def finalize_stop_limit_order(self):
		pass