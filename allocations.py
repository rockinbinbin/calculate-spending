import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import copy
import model
import timeline


# Note: without this, each income event thinks it has contributed to every other bill (even previous ones)
seen_income_indices = []
def update_alloc(bill, index, events, amount):
	if index not in seen_income_indices:
		seen_income_indices.append(index)
		events[index].sources = []
	events[index].sources.append({'name': bill.name, 'date': bill.date, 'amount': amount})
	return events

def apply_allocations(tl):
	secondary = []
	primary = []

	for i, event in enumerate(tl.events):
		if event.income_type == 2:  #'amount' = (event.amount - event.spending) if calculating spending before allocations.
			secondary.append({'index': i,'name': event.name, 'amount': event.amount, 'date': event.date})
		elif event.income_type == 1: 
			primary.append({'index': i,'name': event.name, 'amount': event.amount, 'date': event.date})
		else: #bill
			event, primary, secondary = allocate(event, primary, secondary, tl.events)
			tl.events[i] = event
	return primary, secondary

def allocate(bill, primary, secondary, events):
	all_sources = []
	sources = []
	initial_expense = bill.amount
	carved_expense = -bill.amount

	secondary, carved_expense, events, sources, bill = find_income_sources(secondary, carved_expense, events, sources, bill)
	all_sources.append(sources)
	all_sources = [item for sublist in all_sources for item in sublist]

	if carved_expense > 0: # if dipping into one source isn't enough, dip into the next!
		primary, carved_expense, events, sources, bill = find_income_sources(primary, carved_expense, events, sources, bill)
		all_sources.append(sources)
		all_sources = [item for sublist in all_sources for item in sublist]

	if carved_expense > 0:
		print({'error': 'Insolvent'})

	bill.amount = initial_expense
	bill.sources = all_sources
	return bill, primary, secondary

def find_income_sources(income_source, carved_expense, events, sources, bill):
	income_source.reverse()
	for i, income in enumerate(income_source):
		if bill.amount == 0:
			carved_expense = 0
			break 
		elif income['amount'] > carved_expense: # income source satisfies bill
			sources.append({'name': income['name'], 'date': income['date'], 'amount': carved_expense})
			events = update_alloc(bill, income['index'], events, carved_expense)
			income['amount'] -= carved_expense
			bill.amount = 0
			carved_expense = 0
			break
		else: # if income source is not enough
			sources.append({'name': income['name'], 'date': income['date'], 'amount': income['amount']})
			events = update_alloc(bill, income['index'], events, income['amount'])
			carved_expense -= income['amount']
			income['amount'] = 0
			del income_source[i]
	income_source.reverse()
	return income_source, carved_expense, events, sources, bill

def assemble_timeline(tl, primary, secondary):
	income_sources = primary + secondary
	income_sources.sort(key=lambda item:item['date'], reverse=False)

	for index, item in enumerate(income_sources):
		item['net_days'] = net_days(index, income_sources)
		item['evened_rate'] = item['amount'] / item['net_days'] # spending per day value
	return income_sources

def flow_money(tl, income_sources):
	count = 0
	while (True):
		for i, income in enumerate(income_sources):
			later_incomes = income_sources[i+1:]

			candidates = find_candidates(later_incomes, income)
			evened_rate = find_average_candidates(candidates)
			income['evened_rate'] = evened_rate

			for candidate in candidates:
				index = income_sources.index(candidate)
				income_sources[index]['evened_rate'] = evened_rate
		count += 1
		if count == 10:
			break
	return tl

#helper
def find_candidates(later_incomes, income):
	candidates = []
	candidates.append(income)
	for j, item in enumerate(later_incomes):
		if item['evened_rate'] < income['evened_rate']: #Question: < or <=?
			candidates.append(item)
		else:
			break
	return candidates

def find_average_candidates(candidates):
	total_spending = 0
	total_days = 0
	for item in candidates:
		total_spending += (item['evened_rate'] * item['net_days'])
		total_days += item['net_days']
	return total_spending / total_days

def net_days(index, income_sources):
	income = income_sources[index]
	dividing_factor = 1 # num of days til next paychunk
	if index == (len(income_sources) - 1): # is last paychunk
		dividing_factor = timeline.Timeline.default_end - income['date']
	else:
		dividing_factor = income_sources[index+1]['date'] - income['date']
	days = dividing_factor.days
	if days == 0:
		# Combine events on the same day?
		days = 1
	return days

def reassign_spending_per_period(tl, income_sources):
	for item in income_sources:
		item['evened_spending'] = item['evened_rate'] * item['net_days']
		tl.events[item['index']].spendable = item['evened_spending']

# Exposed Module Method
def calculate_spendings(tl, primary, secondary):
	income_sources = assemble_timeline(tl, primary, secondary)
	flow_money(tl, income_sources)
	reassign_spending_per_period(tl, income_sources)
	#no_flow(tl, income_sources)

def no_flow(tl, income_sources):
	for income in income_sources:
		tl.events[income['index']].spendable = income['amount']
