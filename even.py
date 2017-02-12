import sys
import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import model
import timeline
import solvency
import calculations
import period

#Requires: Model, Timeline, Solvency, & Calculations modules.
#Modifies: Transaction, Event, and Paychunk classes.
#Effects: Models data into Transactions, builds timeline of Events, checks solvency, and computes spendable amounts by Paychunk.

#Todo: take timeline of Events, and assign "spendable" value to each income Event.
# - do this by assigning indices of paychunk objects to income events in timeline.
#Todo: Assign "allocations" to income events and "sources" to expense events. (Get those clarified? Wouldn't you only have one source per expense event?)


def run_with_events():
	all_transactions = model.get_transaction_data(sys.argv[1])
	tl = timeline.Timeline.create_timeline(all_transactions)

	if solvency.is_solvent_from_events(tl.events):

		# USE FOR ALL INCOME BASED CHUNKING
		#----------------------------------------
		# calculations.Paychunk.create_chunks(events)
		# calculations.trickle_down()
		# calculations.Paychunk.reassign_spending_per_paychunk()
		#----------------------------------------

		#USE FOR PERIODIC // PRIMARY INCOME BASED CHUNKING
		#----------------------------------------
		tl.print_periods()
		#----------------------------------------
		#output_from_paychunks()

def output_from_paychunks():
	data = {}
	events = []
	for chunk in calculations.Paychunk.all_paychunks:
		for event in chunk.values:
			one_event = dict()
			one_event["name"] = event.transaction.name
			one_event["date"] = event.date.strftime("%Y-%m-%d")
			if event.transaction.amount > 0:
				one_event["type"] = "income"
				# How do systems handle fractional cents?
				one_event["spendable"] = str(Decimal(chunk.evened_spending).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
			else:
				one_event["type"] = "expense"
			events.append(one_event)
	data['events'] = events
	pprint.pprint(data)

def main():
	run_with_events()

if __name__ == '__main__':
	main()