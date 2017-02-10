from __future__ import division, print_function
import datetime as dt
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange
import solvency
import timeline

#Even Algorithm Module.
#Requires: Input Array of ints (for all transaction values).
#Modifies: Input Array of ints.
#Effects: Groups subarrays of ints based on payday into Paychunk objects with associated averages.

#TODO: handle events that occur on the same day

#Exposed Module Method:
def trickle_down():
	count = 0
	while (True):
		for i, paychunk in enumerate(Paychunk.all_paychunks):
			forward_paychunks = Paychunk.all_paychunks[i+1:]

			contendors = Paychunk.find_contendors(forward_paychunks, paychunk)

			#contendor_totals = Paychunk.totals_from_contendors(contendors)
			average = find_average_contendors(contendors)
			paychunk.average = average

			for contendor in contendors:
				index = Paychunk.all_paychunks.index(contendor)
				Paychunk.all_paychunks[index].average = average
		count += 1
		if count == 100:
			break
	return Paychunk.all_paychunks

class Paychunk(object):
	chunked_transactions = [] #list split into subarrays by amount. Event objects. Ex: [(Event: {+350}, Event: {-200}, Event:{-50}), (Event: {+200}, Event:{-50}, Event:{-100})...]
	all_paychunks = [] #list of all Paychunk objects
	def __init__(self, total=0, values=[], average=0, income_event=0, daily_spending=0, net_days=1, final_average=0):
		self.total = total #net value
		self.values = values
		self.income_event = income_event
		self.daily_spending = daily_spending
		self.net_days = net_days
		self.average = daily_spending #trickled average
		self.final_average = final_average

		#remember: daily_spending * net_days at the end for "spending" key per income event.

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
			total = solvency.total_from_events(chunk)
			paychunk = Paychunk(total=total, values=chunk, income_event=chunk[0])
			Paychunk.all_paychunks.append(paychunk)
		Paychunk.assign_net_spending_values()

	@classmethod
	def net_days(self, index):
		current_paychunk = Paychunk.all_paychunks[index]
		dividing_factor = 1 # num of days til next paychunk
		if index == (len(Paychunk.all_paychunks) - 1): # is last paychunk
			dividing_factor = timeline.Event.default_end - current_paychunk.income_event.date
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
			paychunk.daily_spending = paychunk.total / paychunk.net_days
			paychunk.average = paychunk.daily_spending

	@classmethod
	def find_contendors(self, forward_paychunks, prev_paychunk):
		contendors = []
		contendors.append(prev_paychunk)
		for j, chunk in enumerate(forward_paychunks):
			if chunk.average < prev_paychunk.average: #Question: < or <=?
				contendors.append(chunk)
			else:
				break
		return contendors

	# @classmethod
	# def totals_from_contendors(self, contendors):
	# 	return [contendor.average for contendor in contendors]

	# @classmethod
	# def totals_from_paychunks(self, all_paychunks):
	# 	return [paychunk.total for paychunk in all_paychunks]

	@classmethod
	def reassign_spending_per_paychunk(self):
		for paychunk in Paychunk.all_paychunks:
			paychunk.final_average = paychunk.average * paychunk.net_days
			Paychunk.print_paychunk(paychunk)

	@classmethod
	def print_paychunk(self, paychunk):
		net_total = str(Decimal(paychunk.total).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
		initial_rate = str(Decimal(paychunk.daily_spending).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
		evened_rate = str(Decimal(paychunk.average).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) # final $ per day
		evened_spending = str(Decimal(paychunk.final_average).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) # final $ per chunk (income event)
		print("initial_net_total:", net_total, "net_days:", paychunk.net_days, "initial_rate:", initial_rate, "evened_rate:", evened_rate, "evened_spending:", evened_spending)

	@classmethod
	def print_transaction_amounts(self):
		for chunk in Paychunk.chunked_transactions:
			for item in chunk:
				print(item.transaction.amount)

#helper
def find_average_contendors(contendors):
	total_avg = 0
	num_candidates = 0
	for chunk in contendors:
		total_avg += chunk.average
		num_candidates += 1
	return total_avg / num_candidates


def find_average(inputs):
	total = solvency.calculate_total(inputs)
	total /= len(inputs)
	return total
