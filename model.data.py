from __future__ import division, print_function
import numpy as np
import json
from pprint import pprint
import datetime as dt
import sys
import string
import operator
from collections import defaultdict

#TODO: Consolidate naming for Classes, functions, and variables.
#TODO: Figure out how to reference methods in init for Classes. (@property? class method decorators?)
#TODO: Google Generators. 
#TODO: Handle bad input data.
#TODO: Remove unnecessary import statements.
#TODO: Error handling.

class Frequency(object):
	MONTHLY = 0
	INTERVAL = 1
	ONE_TIME = 2

#TODO: Reference from inside class.
def assign_frequency(frequency_str):
	if frequency_str == 'MONTHLY':
		return Frequency.MONTHLY
	elif frequency_str == 'INTERVAL':
		return Frequency.INTERVAL
	elif frequency_str == 'ONE_TIME':
		return Frequency.ONE_TIME
	else:
		#TODO: throw error
		print("Frequency data error")

class Schedule(object):
	def __init__(self, frequency, start=0, period=0, days=0):
		self.frequency = assign_frequency(frequency)
		if start != 0:
			self.start = strToDate(start)
		else:
			self.start = start
		self.period = period
		self.days = days

#TODO: Reference from inside a class.
def strToDate(str_input):
	date = str_input.split('-')
	return dt.date(int(date[0]), int(date[1]), int(date[2]))

class Transaction(object):
	numTransactions = 0
	def __init__(self, name, amount, schedule):
		self.name = name
		self.amount = amount
		self.schedule = create_schedule(schedule)
		Transaction.numTransactions += 1

	def displayCount(self):
		print("Total Transactions: ", Transaction.numTransactions)

	def displayTransaction(self):
		print("Name : ", self.name, ", Amount: ", self.amount)


# TODO: Reference from inside a class.
# TODO: Handle malformed json more elegantly.
def create_schedule(schedule_data):
	if schedule_data['type'] == 'INTERVAL':
		if 'start' in schedule_data:
			return Schedule('INTERVAL', start=schedule_data['start'])
		else:
			return Schedule('INTERVAL')
	elif schedule_data['type'] == 'MONTHLY':
		if 'start' in schedule_data:
			return Schedule('MONTHLY', start=schedule_data['start'], days=schedule_data['days'])
		else:
			return Schedule(schedule_data['type'], days=schedule_data['days'])
	elif schedule_data['type'] == 'ONE_TIME':
		return Schedule('ONE_TIME', start=schedule_data['start'])
	else:
		#throw Error -- unknown schedule frequency type. 
		return Schedule(schedule_data['type'])

def parse_json(path):
	with open(path,'r') as data_file:
		data = json.load(data_file)
	return data

def createTransactions(data):
	transaction_instances = []
	for item in data:
		transaction_instances.append(Transaction(item['name'], item['amount'], item['schedule']))
	return transaction_instances

def main():
	data = parse_json(sys.argv[1])
	expense_instances = createTransactions(data['expenses'])
	income_instances = createTransactions(data['incomes'])
	print(income_instances[0].schedule.start)

if __name__ == '__main__':
	main()