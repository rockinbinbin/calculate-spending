import sys
import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import model
import timeline
import solvency
import calculations

#Requires: Model, Timeline, Solvency, & Calculations modules.
#Modifies: Transaction, Event, and Paychunk classes.
#Effects: Models data into Transactions, builds timeline of Events, checks solvency, and computes spendable amounts by Paychunk.

#Todo: take timeline of Events, and assign "spendable" value to each income Event.
# - do this by assigning indices of paychunk objects to income events in timeline.
#Todo: Assign "allocations" to income events and "sources" to expense events. (Get those clarified? Wouldn't you only have one source per expense event?)


def run_with_ints():
	all_transactions = model.get_transaction_data(sys.argv[1])
	totals = timeline.extract_totals(all_transactions)
	timeline.Event.print_timeline()
	if solvency.is_solvent(totals):
		calculations.Paychunk.create_num_chunks(totals)
		calculations.trickle_down()
		for paychunk in calculations.Paychunk.all_paychunks:
			print(paychunk.average)	

def run_with_events():
	all_transactions = model.get_transaction_data(sys.argv[1])
	events = timeline.extract_events(all_transactions)
	#timeline.Event.print_timeline()

	if solvency.is_solvent_from_events(events):
		calculations.Paychunk.create_chunks(events)

		calculations.trickle_down()
		calculations.Paychunk.reassign_spending_per_paychunk()

		#output_from_paychunks()

def run_with_whiteboard_inputs():
	inputs = [380, -250, -50, 500, -400, -50, 800, -100, 800, -300, -50, 500, -900, 500, -300]	
	timeline.Event.print_timeline()
	if solvency.is_solvent(inputs):
		calculations.Paychunk.create_num_chunks(inputs)
		calculations.trickle_down()
		for paychunk in calculations.Paychunk.all_paychunks:
			print(paychunk.average)

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
				one_event["spendable"] = str(Decimal(chunk.final_average).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
			else:
				one_event["type"] = "expense"
			events.append(one_event)
	data['events'] = events
	pprint.pprint(data)

def main():
	#run_with_whiteboard_inputs()
	#run_with_ints()
	run_with_events()

if __name__ == '__main__':
	main()