from enum import Enum

class OrderType(Enum):
	MARKET		= 0
	STOP 		= 1
	LIMIT 		= 2
	STOP_LIMIT 	= 3

class OrderOp(Enum):
	BUY 	= 0
	SELL 	= 1

class OrderConditionType(Enum):
	GOOD_TILL_CANCELLED = 0
	GOOD_TILL_FRAME = 1

class ScoreCategory(Enum):
	ACCEPTABLE = 0
	UNACCEPTABLE = 1

class SimStatus(Enum):
	BEGIN = 0
	ACTIVE = 1
	STOP = 2

class SimOrderQueueAction(Enum):
	EXECUTE = 0
	FINALIZE = 1

class TraderStatus(Enum):
	NONE = 0
	AWAIT_ORDER = 1
	NO_FUNDS = 2

class Constants(Enum):
	THRESHOLD = 0.9750