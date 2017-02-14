import sys
import json
import datetime as dt

#Requires: Nothing
#Modifies: Transaction objects
#Effects: Creates Transaction objects from input data

#Exposed Module Methods
def get_transaction_data():
	data = parse_json()
	income_instances = create_transactions(data['incomes'])
	expense_instances = create_transactions(data['expenses'])
	for expense in expense_instances:
		expense.amount = -(expense.amount)
	transactions = income_instances + expense_instances
	return transactions

def parse_json():
	parsed = None
	try:
		path = sys.argv[1]
	except IndexError as idx_err:
		print('Please add an input file command line arg!', idx_err)
	else:
		try:
			with open(path, 'r') as data:
				return json.load(data)
		except ValueError as val_err:
			print('json deserialization error, handle with fallbacks', val_err)

def create_transactions(data):
	transaction_instances = []
	for item in data:
		income_type = Income_Type.UNKNOWN
		if 'type' in item:
			income_type = Income_Type.assign_income_type(item['type'])
		transaction_instances.append(Transaction(item['name'], item['amount'], item['schedule'], income_type))
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

class Income_Type(object):
	UNKNOWN = 0
	PRIMARY = 1
	SECONDARY = 2

	@classmethod
	def assign_income_type(self, income_type_str):
		if income_type_str == 'PRIMARY':
			return Income_Type.PRIMARY
		elif income_type_str == 'SECONDARY':
			return Income_Type.SECONDARY
		else:
			return Income_Type.UNKNOWN

class Schedule(object):
	def __init__(self, frequency, start=0, period=0, days=0):
		self.frequency = Frequency.assign_frequency(frequency)
		if start != 0:
			self.start = str_to_date(start)
		else:
			self.start = start
		self.period = period
		self.days = days

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
	def __init__(self, name, amount, schedule, income_type=Income_Type.UNKNOWN):
		self.name = name
		self.amount = amount
		self.schedule = Schedule.create_schedule(schedule)
		self.income_type = income_type

	def get_start_date(self):
		return self.schedule.start

	def get_frequency(self):
		return self.schedule.frequency

#helpers
def str_to_date(str_input):
	date = str_input.split('-')
	return dt.date(int(date[0]), int(date[1]), int(date[2]))