from __future__ import division, print_function
import json
import model
import timeline

#Solvency Module
#Requires: Input array of ints
#Modifies: Nothing.
#Effects: Outputs JSON if Insolvent.

#edge case: if you're overall solvent, but that's because you have a net negative for each bill (can't pay them) and then make a large sum of money at the end of the year.

def total_from_events(events):
	running_total = 0
	for event in events:
		running_total += event.transaction.amount
	return running_total

def is_solvent_from_events(events):
	if total_from_events(events) > 0:
		return True
	else:
		data = {}
		data['error'] = 'Insolvent'
		json_data = json.dumps(data)
		print(json_data)
		return False


#remove below methods once event logic works

def calculate_total(inputs):
	running_total = 0
	for val in inputs:
		running_total += val
	return running_total

def is_solvent(inputs):
	if calculate_total(inputs) > 0:
		return True
	else:
		data = {}
		data['error'] = 'Insolvent'
		json_data = json.dumps(data)
		print(json_data)
		return False