from __future__ import division, print_function
import numpy as np
import json
from pprint import pprint
import datetime as dt
import sys
import string
import operator
from collections import defaultdict
import calculations
import timeline

#Solvency Module
#Requires: Input array of ints
#Modifies: Nothing.
#Effects: Outputs JSON if Insolvent. Else, runs Even Algorithm on Inputs.

def calculate_total(inputs):
	running_total = 0
	for val in inputs:
		running_total += val
	return running_total

def is_solvent(inputs):
	if calculate_total(inputs) > 0:
		return True
	else:
		return False

def main():
	#inputs = [380, -250, -50, 500, -400, -50, 800, -100, 800, -300, -50, 500, -900, 500, -300]
	if not is_solvent(inputs):
		data = {}
		data['error'] = 'Insolvent'
		json_data = json.dumps(data)
		print(json_data)
	else:
		# Run Even Algorithm
		print("Solvent")
		calculations.main()

if __name__ == '__main__':
	main()