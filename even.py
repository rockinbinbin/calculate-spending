from __future__ import division, print_function
import numpy as np
import json
from pprint import pprint
import datetime as dt
import sys
import string
import operator
from collections import defaultdict
import model
import timeline
import solvency
import calculations

def 

def main():
	incomes, expenses = model.get_transaction_data()
	all_transactions = incomes + expenses

	totals = timeline.extract_totals(all_transactions)
	#print(totals)

	#totals = [380, -250, -50, 500, -400, -50, 800, -100, 800, -300, -50, 500, -900, 500, -300]

	if not solvency.is_solvent(totals):
		data = {}
		data['error'] = 'Insolvent'
		json_data = json.dumps(data)
		print(json_data)
	else:
		# Run Even Algorithm
		print("Solvent")

		#Requires: input: array of ints
		#Modifies: input: array of ints
		#Effects: chunks input into subgroups by income (Paychunk object), and assigns a spending value.

		#Todo: fix while loop if iterative method is chosen.
		#Todo: take timeline of Events, and assign "spendable" value to each income Event.
		# - do this by assigning indices of paychunk objects to income events in timeline.
		#Todo: Assign "allocations" to income events and "sources" to expense events. (Get those clarified? Wouldn't you only have one source per expense event?)
		calculations.assign_spendables(totals)



if __name__ == '__main__':
	main()
