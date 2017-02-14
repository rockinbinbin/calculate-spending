import os, types
import datetime as dt
from datetime import timedelta
import pprint
from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange
import operator
import model

#Requires: all_transactions array of Transaction input objects (incomes and expenses)
#Modifies: Event, Timeline classes
#Effects: Timeline.create_timeline() creates a timeline of events, and periodic_events.

class Event(object): 
	def __init__(self, name, amount, date, income_type=model.Income_Type.UNKNOWN, sources=[], spendable=0, evened_rate=0):
		self.name = name
		self.amount = amount
		self.date = date
		self.income_type = income_type
		self.sources = sources 
		self.spendable = spendable # only for primary income events
		self.evened_rate = evened_rate # only for primary income events

	def print_event(self):
		print(self.name, str(self.amount), str(self.date), self.spendable)
		for source in self.sources:
			print('source:')
			print(source['name'], source['date'], source['amount'])
		print('\n')

def total(events):
	return sum(event.amount for event in events)

def is_solvent(events):
	if total(events) > 0:
		return True
	else:
		# typically would raise instead of print error, but need to return false
		print({'error': 'Insolvent'})
		return False

class Timeline(object):
	default_start=dt.date(2016, 01, 01)
	default_end=dt.date(2017, 01, 01)

	def __init__(self, events=[], periodic_events=[]):
		self.events = events
		self.periodic_events = periodic_events

	@classmethod
	def create_monthly_events(self, all_transactions, events):
		for transaction in all_transactions:
			months = []
			if transaction.schedule.start != 0:
				months = months_between(transaction.schedule.start, Timeline.default_end)
			else:
				months = months_between(Timeline.default_start, Timeline.default_end)

			if transaction.get_frequency() == model.Frequency.MONTHLY:
				for month in months:
					for day in transaction.schedule.days:
						date = dt.date(2016, month, day)
						new_event = Event(transaction.name, transaction.amount, date, income_type=transaction.income_type)
						events.append(new_event)
		return events

	@classmethod
	def create_interval_events(self, all_transactions, events):
		for transaction in all_transactions:
			if transaction.get_frequency() == model.Frequency.INTERVAL:
				current_date = transaction.schedule.start
				while (current_date < Timeline.default_end):
					new_event = Event(transaction.name, transaction.amount, current_date, income_type=transaction.income_type)
					events.append(new_event)
					current_date += timedelta(days=transaction.schedule.period)
		return events

	@classmethod
	def create_onetime_events(self, all_transactions, events):
		for transaction in all_transactions:
			if transaction.get_frequency() == model.Frequency.ONE_TIME:
				new_event = Event(transaction.name, transaction.amount, transaction.schedule.start, income_type=transaction.income_type)
				events.append(new_event)
		return events

	@classmethod
	def assemble_events(self, all_transactions):
		events = []
		events = Timeline.create_monthly_events(all_transactions, events)
		events = Timeline.create_interval_events(all_transactions, events)
		events = Timeline.create_onetime_events(all_transactions, events)
		# TODO: Try reduce. Tuple allows secondary sort (paychecks above bills)
		events.sort(key=operator.attrgetter('date'))
		return events

	@classmethod
	def create_periods(self, events):
		new_group = []
		periodic_events = []
		for i, event in enumerate(events):
			if event.income_type == model.Income_Type.PRIMARY:
				new_group.append(event)
			else: 
				if len(new_group) != 0:
					new_group.append(event)
				if i == (len(events) - 1) or events[i+1].income_type == model.Income_Type.PRIMARY:
					periodic_events.append(new_group)
					new_group = []
		return periodic_events

	@classmethod
	def create_timeline(self, all_transactions):
		events = Timeline.assemble_events(all_transactions)

		#not necessary for new allocations methods
		#keep if you want to create periods by primary income
		periodic_events = Timeline.create_periods(events) 
		timeline = Timeline(events, periodic_events)
		return timeline 

	def print_timeline(self):
		for event in self.events:
			event.print_event()

	def output_timeline(self):
		data = {}
		events = []
		for event in self.events:
			one_event = dict()
			one_event['name'] = event.name
			one_event['date'] = event.date.strftime('%Y-%m-%d')
			if event.amount > 0:
				one_event['type'] = 'income'
				if event.spendable > 0:
					one_event['spendable'] = str(Decimal(event.spendable).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
				one_event['allocations'] = event.sources
			else:
				one_event['type'] = 'expense'
				one_event['sources'] = event.sources
			events.append(one_event)
		data['events'] = events
		pprint.pprint(data)

	def print_periods(self):
		for period in self.periodic_events:
			for event in period:
				event.print_event()
			print('\n')

#helpers
#Source: http://stackoverflow.com/questions/4039879/best-way-to-find-the-months-between-two-dates
def months_between(start, end):
	months = []
	cursor = start
	while cursor <= end:
		if cursor.month not in months:
			months.append(cursor.month)
		cursor += timedelta(weeks=1)
	return months
