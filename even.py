import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import model
import timeline
import allocations
import unittests

#Requires: Model, Timeline, Solvency, & Allocation modules.
#Modifies: Transaction, Event, and Paychunk classes.
#Effects: Models data into Transactions, builds timeline of Events, checks solvency, and computes spendable amounts by Paychunk.

def run_with_events():
	transactions = model.get_transaction_data()
	tl = timeline.Timeline.create_timeline(transactions)

	if timeline.is_solvent(tl.events):
		primary, secondary = allocations.apply_allocations(tl)

		allocations.calculate_spendings(tl, primary, secondary)

		tl.output_timeline()

		unittests.sound_income_allocations(tl)

def main():
	run_with_events()

if __name__ == '__main__':
	main()