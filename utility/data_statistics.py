import numpy as np
import scipy as sp
from scipy import stats

def reverse_peak_test(data, result, index, center_index, edge_index, min_height_perc):
	if index > 0 and min_height_perc > 0:

		# safety checks
		max_index = len(data) - 1
		if center_index > max_index or edge_index > max_index:
			return False

		# compute values
		first_value 	= data[index]
		center_value 	= data[center_index]
		edge_value 		= data[edge_index]

		height_diff		=  1 - (2*center_value/(first_value + edge_value)) # height difference in percents

		# perform test
		if first_value > center_value and edge_value > center_value and height_diff > min_height_perc:
			result[center_index] = center_value
			return True
		else:
			return False
	else:
		return False

# given a time-value series, compute the estimated location of the reverse-peaks
def get_reverse_peaks(data, window_size=30, min_height_perc=0.01):
	
	proc_array = np.zeros(data.size, dtype=np.float64)
	isEvent = False

	print("", end="\r", flush=True)
	for index in range(data.size):
		print("get_reverse_peaks::index -> ", index, end="\r", flush=True)

		# compute sampling indices
		center_index 	= index + window_size // 2
		edge_index 		= index + window_size
		result = reverse_peak_test(data, proc_array, index, center_index, edge_index, min_height_perc)

	print("", end="\n", flush=True)
	return proc_array

# given a series for reverse-peaks (value of 0. for non-peaks, value > 0 for reverse-peaks)
# take a sample of the data of size sample_size before the peak starts, and log frame position of true minimum
def compute_pre_peak_windows(data, reverse_peak_data, sample_size=30):

	# control and storage vars
	event_windows = {"window_data": [], "true_minima_offset": []}
	is_event = False
	event_start_index = None

	# peak data
	local_minima = None
	minima_frame_offset = None

	# data buffer
	event_data = None

	# ensure time increases as frame number increases!
	# you may need to flip arrays before processing!

	print("", end="\r", flush=True)
	for index in range(reverse_peak_data.size):

		print("compute_pre_peak_windows::index -> ", index, " max -> ", reverse_peak_data.size, end="\r", flush=True)

		# boundary check
		if index + 1 > sample_size:
			if not is_event:
				# small constant comparison for detecting 0.
				if reverse_peak_data[index] < 1e-12:
					continue
				else:
					is_event = True
					event_start_index = index
					event_data = rescale_vector(np.array(data[index-sample_size:index])) # index gymnastics: last sample_size frames, *including* index
					event_windows["window_data"].append(event_data)

					# init values for event pass
					local_minima = data[index]
					minima_frame_offset = 0
			else:
				if reverse_peak_data[index] > 1e-12:
					if data[index] <= local_minima:
						local_minima = data[index]
						minima_frame_offset = index - event_start_index
				else:
					event_windows["true_minima_offset"].append(minima_frame_offset)
					is_event = False
					local_minima = None

	if len(event_windows["window_data"]) != len(event_windows["true_minima_offset"]):
		raise IndexError
	else:
		event_windows["window_data"] = np.array(event_windows["window_data"], dtype=np.float64)
		event_windows["true_minima_offset"] = np.array(event_windows["true_minima_offset"], dtype=np.uint32)

	print("", end="\n", flush=True)
	return event_windows

def compute_correlations(event_windows, candidate_window):
	
	# pre-arrange arrays
	num_windows = len(event_windows["window_data"])
	correlations = np.zeros(num_windows)

	# safety check to ensure individual windows are of same width
	if event_windows["window_data"][0].size != candidate_window.size:
		raise ValueError
		return

	for index in range(num_windows):
		correlations[index], p_value = stats.pearsonr(event_windows["window_data"][index], candidate_window)

	max_correlation_index = np.argmax(correlations)

	return correlations, max_correlation_index


def rescale_vector(v):
	# find maximum value of v
	max_val = v.max()

	# find minimum value of v
	min_val = v.min()

	# rescale to map min -> 0, max -> 1
	if min_val != max_val:
		v = (v - min_val) / (max_val - min_val)
	else:
		np.full(v.size, 0.5, dtype=np.float64)

	return v

def cutoff_weighted_average(data_points, data_values, cutoff=0.0):

	factor_sum = 0
	denominator_sum = 0

	for index in range(len(data_points)):
		point_value = data_points[index]
		data_value = data_values[index]

		if point_value >= cutoff:
			denominator_sum += point_value
			factor_sum += point_value * data_value

	try:
		return factor_sum / denominator_sum
	except ZeroDivisionError as e:
		return 0.0