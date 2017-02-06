from __future__ import division, print_function
import numpy as np
import json
from pprint import pprint
import datetime as dt
import sys
import string
import operator
from collections import defaultdict
import 'model.data.py'

def calculate_total(inputs):
	running_total = 0
	for val in inputs:
		running_total += val
	return running_total

def is_solvent(inputs):
	if calculate_total(inputs):
		return True
	else:
		return False

def create_chunks(inputs):
	chunks = dict()

def main():
	# inputs = [380, -250, -50, 500, -400, -50, 800, -100, 800, -300, -50, 500, -900, 500, -300]
	# #smaller_inputs = [50, -50, 20]
	# if not is_solvent(inputs):
	# 	# StdOut JSON error: "Insolvent"
	# 	print("insolvent")
	# else:
	# 	print("solvent")

if __name__ == '__main__':
	main()