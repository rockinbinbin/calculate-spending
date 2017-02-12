from __future__ import division, print_function
import datetime as dt
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange
import solvency
import timeline

#Even Algorithm Module.
#Requires: Timeline events
#Modifies: Timeline events
#Effects: Groups subarrays of Events based on payday into Paychunk objects. Calculates evened_spending.

#TODO: handle events that occur on the same day

#Exposed Module Method:
def trickle_down():
	count = 0
	while (True):
		for i, paychunk in enumerate(Paychunk.all_paychunks):
			forward_paychunks = Paychunk.all_paychunks[i+1:]

			candidates = Paychunk.find_candidates(forward_paychunks, paychunk)

			#contendor_totals = Paychunk.totals_from_contendors(contendors)
			evened_rate = find_average_candidates(candidates)
			paychunk.evened_rate = evened_rate

			for candidate in candidates:
				index = Paychunk.all_paychunks.index(candidate)
				Paychunk.all_paychunks[index].evened_rate = evened_rate
		count += 1
		if count == 100:
			break
	return Paychunk.all_paychunks

class Paychunk(object):
	chunked_transactions = [] #list split into subarrays by amount. Event objects. Ex: [(Event: {+350}, Event: {-200}, Event:{-50}), (Event: {+200}, Event:{-50}, Event:{-100})...]
	all_paychunks = [] #list of all Paychunk objects
	def __init__(self, net_total=0, values=[], evened_rate=0, income_event=0, initial_rate=0, net_days=1, evened_spending=0):
		self.net_total = net_total #net income after bills
		self.values = values # Events in this chunk.
		self.income_event = income_event # Income event that allows money provisioned in this chunk.
		self.initial_rate = initial_rate # initial daily spending. debug purposes
		self.net_days = net_days # days until next income
		self.evened_rate = initial_rate #trickled average
		self.evened_spending = evened_spending #final 

	@classmethod
	def create_chunks(self, events):
		grouped_inputs = []
		new_chunk = []
		for i, event in enumerate(events):
			if event.transaction.amount > 0: #is paycheck
				new_chunk.append(event)
			else: #is bill
				if len(new_chunk) != 0: # chunk not empty
					new_chunk.append(event)
				if i == (len(events) - 1) or events[i+1].transaction.amount > 0: # if i is last element or next is positive
					grouped_inputs.append(new_chunk)
					new_chunk = []

		Paychunk.chunked_transactions = grouped_inputs
		Paychunk.assign_objects()

	@classmethod
	def create_num_chunks(self, inputs):
		grouped_inputs = []
		new_chunk = []
		for i, num in enumerate(inputs):
			if num > 0: #is paycheck
				new_chunk.append(num)
			else: #is bill
				if len(new_chunk) != 0: # chunk not empty
					new_chunk.append(num)
				if i == (len(inputs) - 1) or inputs[i+1] > 0: # if i is last element or next is positive
					grouped_inputs.append(new_chunk)
					new_chunk = []
		Paychunk.chunked_transactions = grouped_inputs
		Paychunk.assign_objects()

	@classmethod
	def assign_objects(self):
		for chunk in Paychunk.chunked_transactions:
			net_total = solvency.total_from_events(chunk)
			paychunk = Paychunk(net_total=net_total, values=chunk, income_event=chunk[0])
			Paychunk.all_paychunks.append(paychunk)
		Paychunk.assign_net_spending_values()

	@classmethod
	def net_days(self, index):
		current_paychunk = Paychunk.all_paychunks[index]
		dividing_factor = 1 # num of days til next paychunk
		if index == (len(Paychunk.all_paychunks) - 1): # is last paychunk
			dividing_factor = timeline.Timeline.default_end - current_paychunk.income_event.date
		else:
			dividing_factor = Paychunk.all_paychunks[index+1].income_event.date - current_paychunk.income_event.date

		days = dividing_factor.days
		if days == 0:
			#print(current_paychunk.income_event.transaction.name, current_paychunk.income_event.date)
			# Combine events on the same day?
			days = 1
		return days

	@classmethod
	def assign_net_spending_values(self):
		for i, paychunk in enumerate(Paychunk.all_paychunks):
			paychunk.net_days = Paychunk.net_days(i)
			paychunk.initial_rate = paychunk.net_total / paychunk.net_days
			paychunk.evened_rate = paychunk.initial_rate

	@classmethod
	def find_candidates(self, forward_paychunks, prev_paychunk):
		candidates = []
		candidates.append(prev_paychunk)
		for j, chunk in enumerate(forward_paychunks):
			if chunk.evened_rate < prev_paychunk.evened_rate: #Question: < or <=?
				candidates.append(chunk)
			else:
				break
		return candidates

	@classmethod
	def reassign_spending_per_paychunk(self):
		for paychunk in Paychunk.all_paychunks:
			paychunk.evened_spending = paychunk.evened_rate * paychunk.net_days
			Paychunk.print_paychunk(paychunk)

	@classmethod
	def print_paychunk(self, paychunk):
		net_total = str(Decimal(paychunk.net_total).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
		initial_rate = str(Decimal(paychunk.initial_rate).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
		evened_rate = str(Decimal(paychunk.evened_rate).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) # final $ per day
		evened_spending = str(Decimal(paychunk.evened_spending).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) # final $ per chunk (income event)
		print("initial_net_total:", net_total, "net_days:", paychunk.net_days, "initial_rate:", initial_rate, "evened_rate:", evened_rate, "evened_spending:", evened_spending)

	@classmethod
	def print_transaction_amounts(self):
		for chunk in Paychunk.chunked_transactions:
			for item in chunk:
				print(item.transaction.amount)


#helper
def find_average_candidates(candidates):
	total_spending = 0
	total_days = 0
	for chunk in candidates:
		total_spending += (chunk.evened_rate * chunk.net_days)
		total_days += chunk.net_days
	return total_spending / total_days

def find_average(inputs):
	total = solvency.calculate_total(inputs)
	total /= len(inputs)
	return total
