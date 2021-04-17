import numpy as np
import h5py

class Precomputed:
	def __init__(self, path_to_dataset, exchange_name, symbol_name):

		try:
			self.dataset = h5py.File(path_to_dataset)
			self.event_windows = self.get_event_windows(exchange_name, symbol_name)
			self.dataset.close()

		except FileNotFoundError as e:
			self.failed = True
			raise e

		except KeyError as e:
			self.failed = True
			raise e

	def get_event_windows(self, exchange_name, symbol_name):
		data = self.dataset["precomputed"]["exchange"][exchange_name]["symbols"][symbol_name]
		return {"window_data": np.array(data["window_data"], dtype=np.float64), "true_minima_offset": np.array(data["true_minima_offset"], dtype=np.uint32)}

