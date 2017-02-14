import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import model
import timeline
import solvency
import calculations
import allocations

#Requires: Model, Timeline, Solvency, & Calculations modules.
#Modifies: Transaction, Event, and Paychunk classes.
#Effects: Models data into Transactions, builds timeline of Events, checks solvency, and computes spendable amounts by Paychunk.

#Todo: take timeline of Events, and assign "spendable" value to each income Event.
# - do this by assigning indices of paychunk objects to income events in timeline.
#Todo: Assign "allocations" to income events and "sources" to expense events. (Get those clarified? Wouldn't you only have one source per expense event?)


def run_with_events():
	transactions = model.get_transaction_data()
	tl = timeline.Timeline.create_timeline(transactions)
	if solvency.is_solvent_from_events(tl.events):
		# USE FOR ALL INCOME BASED CHUNKING
		#----------------------------------------
		# calculations.Paychunk.create_chunks(events)
		# calculations.trickle_down()
		# calculations.Paychunk.reassign_spending_per_paychunk()
		#----------------------------------------

		#USE FOR PERIODIC // PRIMARY INCOME BASED CHUNKING
		#----------------------------------------
		#tl.print_periods()



		allocations.start(tl)
		tl.output_timeline()



		
		# tl.print_timeline()
		#----------------------------------------
		#output_from_paychunks()

def main():
	run_with_events()

if __name__ == '__main__':
	main()