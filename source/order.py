import numpy as np
from enums.enums import OrderType, OrderOp, OrderConditionType
from typing import NamedTuple
import types

class OrderCondition():
	def __init__(self, condition_type, max_frame)
		self.condition_type = condition_type
		self.max_frame = max_frame

class Order(NamedTuple):
	order_op: 	OrderOp
    order_type: OrderType
    amount: 	np.float64
    callback: 	types.FunctionType
    condition:	OrderCondition

    
