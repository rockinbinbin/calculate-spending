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
	return sum(event.transaction.amount for event in events)

def is_solvent_from_events(events):
	if total_from_events(events) > 0:
		return True
	else:
		# typically would raise instead of print error, but need to return false
		print({'error': 'Insolvent'})
		return False

#remove below methods once event logic works
def calculate_total(inputs):
	return sum(value for value in inputs)

def is_solvent(inputs):
	if calculate_total(inputs) > 0:
		return True
	else:
		# typically would raise instead of print error, but need to return false
		print({'error': 'Insolvent'})
		return False