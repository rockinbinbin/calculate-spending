import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import copy
import model
import timeline
import solvency
import calculations
import period


def add_to_income_source(income_source, event, index):
	income_source.append({"index": index,"name": event.name, "amount": event.amount, "date": event.date})
	return income_source

def update_event_sources(bill, events, bill_index):
	events[bill_index] = bill
	return events

# Note: without this, each income event thinks it has contributed to every other bill (even previous ones)
seen_income_indices = []
def update_alloc(bill, index, events, amount):
	if index not in seen_income_indices:
		seen_income_indices.append(index)
		events[index].sources = []
	events[index].sources.append({"name": bill.name, "date": bill.date, "amount": amount})
	return events

def start(tl):
	secondary = []
	primary = []

	for i, event in enumerate(tl.events):
		if event.income_type == 2: 
			secondary = add_to_income_source(secondary, event, i)
		elif event.income_type == 1: 
			primary = add_to_income_source(primary, event, i)
		else: #bill
			event, primary, secondary = allocate(event, primary, secondary, tl.events)
			tl.events = update_event_sources(event, tl.events, i)

def allocate(bill, primary, secondary, events):
	sources = []
	initial_expense = bill.amount
	carved_expense = -bill.amount

	secondary, carved_expense, events, sources, bill = find_income_sources(secondary, carved_expense, events, sources, bill)

	if carved_expense > 0: # if dipping into one source isn't enough, dip into the next!
		primary, carved_expense, events, sources, bill = find_income_sources(primary, carved_expense, events, sources, bill)

	if carved_expense > 0:
		print('Insolvent for this bill')
	bill.amount = initial_expense
	bill.sources = sources
	return bill, primary, secondary

def find_income_sources(income_source, carved_expense, events, sources, bill):
	for i, income in enumerate(income_source):
		if bill.amount == 0:
			break 
		elif income['amount'] > carved_expense: # income source satisfies bill
			sources.append({"name": income['name'], "date": income['date'], "amount": carved_expense})
			events = update_alloc(bill, income['index'], events, carved_expense)
			income['amount'] -= carved_expense
			bill.amount = 0
			carved_expense = 0
			break
		else: # if income source is not enough
			sources.append({"name": income['name'], "date": income['date'], "amount": income['amount']})
			events = update_alloc(bill, income['index'], events, income['amount'])
			carved_expense -= income['amount']
			del income_source[i]	
	return income_source, carved_expense, events, sources, bill

def calculate_spendings(tl):
	#chunk by primary income, calculate net spendings, and subtract net spending from primary income.
	# assign a net spending value to each primary income.
	# run allocation algorithm.




