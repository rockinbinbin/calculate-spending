from __future__ import division, print_function
import numpy as np
import json
from pprint import pprint
import datetime as dt
from datetime import datetime, timedelta
from calendar import monthrange
import sys
import string
import operator
from collections import defaultdict
import model

#TODO: Take data from model.data, and 

# 1 - create all events from transactions
# 2 - sort events by date (break tie by positive first, otherwise doesn't matter).

default_start = dt.date(2016, 01, 01)
default_end = dt.date(2017, 01, 01)

class Event(object):
	all_events = []
	def __init__(self, transaction, date, spendable=0, sources=[]):
		#self.event_type = event_type #if income, "allocations" in output. else "sources"
		self.transaction = transaction
		self.date = date
		self.spendable = spendable

#Source: http://stackoverflow.com/questions/4039879/best-way-to-find-the-months-between-two-dates
def months_between(start,end):
    months = []
    cursor = start
    while cursor <= end:
        if cursor.month not in months:
            months.append(cursor.month)
        cursor += timedelta(weeks=1)
    return months

# TODO: Account for transaction start dates if exist
def create_monthly_events(all_transactions):
	for transaction in all_transactions:
		months = []
		if transaction.schedule.start != 0:
			months = months_between(transaction.schedule.start, default_end)
		else:
			months = months_between(default_start, default_end)

		if transaction.get_frequency() == model.Frequency.MONTHLY:
			for month in months:
				for day in transaction.schedule.days:
					date = dt.date(2016, month, day)
					new_event = Event(transaction, date)
					Event.all_events.append(new_event)

def create_interval_events(all_transactions):
	# create an event after every period of days
	for transaction in all_transactions:
		if transaction.get_frequency() == model.Frequency.INTERVAL:
			current_date = transaction.schedule.start
			while (current_date < default_end):
				new_event = Event(transaction, current_date)
				Event.all_events.append(new_event)
				current_date += timedelta(days=transaction.schedule.period)

def create_onetime_events(all_transactions):
	for transaction in all_transactions:
		if transaction.get_frequency() == model.Frequency.ONE_TIME:
			new_event = Event(transaction, transaction.schedule.start)
			Event.all_events.append(new_event)

def create_all_events(all_transactions):
	create_monthly_events(all_transactions)
	create_interval_events(all_transactions)
	create_onetime_events(all_transactions)

#if years > 1, find # of years 

def extract_totals(all_transactions):
	# incomes, expenses = model.get_transaction_data()
	# all_transactions = incomes + expenses

	create_all_events(all_transactions)

	# TODO: Try reduce. Tuple allows secondary sort (paychecks above bills)
	Event.all_events.sort(key=operator.attrgetter("date"))

	totals_from_events = []
	for event in Event.all_events:
		totals_from_events.append(event.transaction.amount)
	return totals_from_events

def main():
	incomes, expenses = model.get_transaction_data()
	all_transactions = incomes + expenses

	create_all_events(all_transactions)

	# TODO: Try reduce. Tuple allows secondary sort (paychecks above bills)
	Event.all_events.sort(key=operator.attrgetter("date"))
	



	# count = 0
	# for event in Event.all_events:
	# 	print(event.transaction.name, event.date, event.transaction.amount)
	# 	count+=1
		# if count == 10:
		# 	break

if __name__ == '__main__':
	main()