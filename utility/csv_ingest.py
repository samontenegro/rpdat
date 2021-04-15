import numpy as np
import pandas as pd
import h5py

def load_csv(file_path):
	return pd.read_csv(file_path)

def ingest(file_ref, exchange_name, symbol_name, data, timestamps):
	if file_ref != None:
		data_path = "data/exchange/" + exchange_name + "/symbols/" + symbol_name

		# attempt to create new field
		try:
			symbol_ref = file_ref.create_group(data_path)
		except ValueError as e:
			raise e
			return

		if len(data) != len(timestamps):
			print("Warning: data and timestamp array sizes are different!")

		symbol_ref.create_dataset("price_data", data=data)
		symbol_ref.create_dataset("timestamps", data=timestamps)


if __name__ == '__main__':
	pass