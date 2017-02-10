import json
import datetime as dt

#Requires: sys.arg[1] input filename
#Modifies: Transaction objects
#Effects: get_transaction_data

#TODO: Figure out how to reference methods in init for Classes. (@property? class method decorators?)
#TODO: Google Generators. 
#TODO: Handle bad input data.
#TODO: Error handling.

#Question: Does supporting a variety of schedules mean data might be different from complex.input?
#Question: Is the simple input's output in the ReadMe?

#Exposed Module Methods
def get_transaction_data(filename):
	data = parse_json(filename)

	income_instances = create_transactions(data['incomes'], "income")
	expense_instances = create_transactions(data['expenses'], "expense")

	for expense in expense_instances:
		expense.amount = -(expense.amount)

	all_transactions = income_instances + expense_instances
	Transaction.all_transactions = all_transactions
	return all_transactions

def parse_json(path):
	with open(path,'r') as data_file:
		data = json.load(data_file)
	return data

def create_transactions(data, event_type):
	transaction_instances = []
	for item in data:
		transaction_instances.append(Transaction(event_type, item['name'], item['amount'], item['schedule']))
	return transaction_instances

class Frequency(object):
	MONTHLY = 0
	INTERVAL = 1
	ONE_TIME = 2

	@classmethod
	def assign_frequency(self, frequency_str):
		if frequency_str == 'MONTHLY':
			return Frequency.MONTHLY
		elif frequency_str == 'INTERVAL':
			return Frequency.INTERVAL
		elif frequency_str == 'ONE_TIME':
			return Frequency.ONE_TIME
		else:
			raise Exception('Frequency data error')

class Schedule(object):
	def __init__(self, frequency, start=0, period=0, days=0):
		self.frequency = Frequency.assign_frequency(frequency)
		if start != 0:
			self.start = Schedule.str_to_date(start)
		else:
			self.start = start
		self.period = period
		self.days = days

	@classmethod
	def str_to_date(self, str_input):
		date = str_input.split('-')
		return dt.date(int(date[0]), int(date[1]), int(date[2]))

	# TODO: Handle malformed json more elegantly.
	@classmethod
	def create_schedule(self, schedule_data):
		if schedule_data['type'] == 'INTERVAL':
			return Schedule('INTERVAL', start=schedule_data['start'], period=schedule_data['period'])
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

class Transaction(object):
	all_transactions = []
	def __init__(self, event_type, name, amount, schedule):
		self.event_type = event_type
		self.name = name
		self.amount = amount
		self.schedule = Schedule.create_schedule(schedule)

	def get_start_date(self):
		return self.schedule.start

	def get_frequency(self):
		return self.schedule.frequency