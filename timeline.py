import datetime as dt
from datetime import datetime, timedelta
from calendar import monthrange
import operator
import model

#Requires: all_transactions array of Transaction input objects (incomes and expenses)
#Modifies: Event, Timeline classes
#Effects: Timeline.create_timeline() creates a timeline of events, and periodic_events.

class Source(object):
	def __init__(self, name, date, amount):
		self.name = name
		self.date = date
		self.amount = amount

class Event(object): 
	def __init__(self, transaction, date, sources=[], spendable=0):
		self.transaction = transaction
		self.date = date
		self.sources = sources 
		self.spendable = spendable

	def print_event(self):
		print(self.transaction.name, self.transaction.amount, self.date, self.spendable, self.sources)


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
						new_event = Event(transaction, date)
						events.append(new_event)
		return events

	@classmethod
	def create_interval_events(self, all_transactions, events):
		for transaction in all_transactions:
			if transaction.get_frequency() == model.Frequency.INTERVAL:
				current_date = transaction.schedule.start
				while (current_date < Timeline.default_end):
					new_event = Event(transaction, current_date)
					events.append(new_event)
					current_date += timedelta(days=transaction.schedule.period)
		return events

	@classmethod
	def create_onetime_events(self, all_transactions, events):
		for transaction in all_transactions:
			if transaction.get_frequency() == model.Frequency.ONE_TIME:
				new_event = Event(transaction, transaction.schedule.start)
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
			if event.transaction.income_type == model.Income_Type.PRIMARY:
				new_group.append(event)
			else: 
				if len(new_group) != 0:
					new_group.append(event)
				if i == (len(events) - 1) or events[i+1].transaction.income_type == model.Income_Type.PRIMARY:
					periodic_events.append(new_group)
					new_group = []
		return periodic_events

	@classmethod
	def create_timeline(self, all_transactions):
		events = Timeline.assemble_events(all_transactions)
		periodic_events = Timeline.create_periods(events)
		timeline = Timeline(events, periodic_events)
		return timeline 

	def print_timeline(self):
		for event in self.events:
			event.print_event()

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
