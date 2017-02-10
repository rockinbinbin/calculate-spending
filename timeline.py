import datetime as dt
from datetime import datetime, timedelta
from calendar import monthrange
import operator
import model

#Requires: all_transactions array of Transaction input objects (incomes and expenses)
#Modifies: Event class
#Effects: extract_events: timeline of Event objects
#Effects: extract_totals: for testing purposes, timeline of ints

#Exposed Module Methods
def extract_events(all_transactions):
	Event.all_transactions = all_transactions
	Event.create_all_events()
	return Event.all_events

def extract_totals(all_transactions):
	Event.all_transactions = all_transactions
	Event.create_all_events()
	totals_from_events = []
	for event in Event.all_events:
		totals_from_events.append(event.transaction.amount)
	return totals_from_events


class Event(object):
	all_events = []
	all_transactions = []

	default_start = dt.date(2016, 01, 01)
	default_end = dt.date(2017, 01, 01) #update date for different test cases!!!!!!

	def __init__(self, transaction, date, spendable=0, sources=[]):
		#self.event_type = event_type #if income, "allocations" in output. else "sources"
		self.transaction = transaction
		self.date = date
		self.spendable = spendable
		self.sources = sources

	@classmethod
	def print_timeline(self):
		for event in Event.all_events:
			print(str(event.date), str(event.transaction.amount), str(event.transaction.name))

	#Source: http://stackoverflow.com/questions/4039879/best-way-to-find-the-months-between-two-dates
	@classmethod
	def months_between(self, start, end):
		months = []
		cursor = start
		while cursor <= end:
			if cursor.month not in months:
				months.append(cursor.month)
			cursor += timedelta(weeks=1)
		return months

	@classmethod
	def create_monthly_events(self):
		for transaction in Event.all_transactions:
			months = []
			if transaction.schedule.start != 0:
				months = Event.months_between(transaction.schedule.start, Event.default_end)
			else:
				months = Event.months_between(Event.default_start, Event.default_end)

			if transaction.get_frequency() == model.Frequency.MONTHLY:
				for month in months:
					for day in transaction.schedule.days:
						date = dt.date(2016, month, day)
						new_event = Event(transaction, date)
						Event.all_events.append(new_event)

	@classmethod
	def create_interval_events(self):
		for transaction in Event.all_transactions:
			if transaction.get_frequency() == model.Frequency.INTERVAL:
				current_date = transaction.schedule.start
				while (current_date < Event.default_end):
					new_event = Event(transaction, current_date)
					Event.all_events.append(new_event)
					current_date += timedelta(days=transaction.schedule.period)

	@classmethod
	def create_onetime_events(self):
		for transaction in Event.all_transactions:
			if transaction.get_frequency() == model.Frequency.ONE_TIME:
				new_event = Event(transaction, transaction.schedule.start)
				Event.all_events.append(new_event)

	@classmethod
	def create_all_events(self):
		Event.create_monthly_events()
		Event.create_interval_events()
		Event.create_onetime_events()
		# TODO: Try reduce. Tuple allows secondary sort (paychecks above bills)
		Event.all_events.sort(key=operator.attrgetter("date"))