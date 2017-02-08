from __future__ import division, print_function
import solvency

#Even Algorithm Module.
#Requires: Input Array of ints (for all transaction values).
#Modifies: Input Array of ints.
#Effects: Groups subarrays of ints based on payday into Paychunk objects with associated averages.
#TODO: Take average of each paychunk, and calculate spendable money / transaction.

#Exposed Module Method:
#Todo: fix while loop if iterative method is chosen.
def trickle_down():
	count = 0
	while (True):
		for i, paychunk in enumerate(Paychunk.all_paychunks):
			forward_paychunks = Paychunk.all_paychunks[i+1:]
			contendors = Paychunk.find_contendors(forward_paychunks, paychunk)

			contendor_totals = Paychunk.totals_from_contendors(contendors)
			average = find_average(contendor_totals)
			paychunk.average = average

			for contendor in contendors:
				index = Paychunk.all_paychunks.index(contendor)
				Paychunk.all_paychunks[index].average = average
		count += 1
		if count == 1:
			break
	return Paychunk.all_paychunks


class Paychunk(object):
	chunked_transactions = [] #array split into subarrays by amount. Ex: [(+350, -200, -50), (+200, -50, -100)...]
	all_paychunks = [] #array of Paychunk objects
	def __init__(self, total=0, values=[], average=0):
		self.total = total #net value
		self.values = values
		self.average = total #trickled average

	@classmethod
	def create_chunks(self, events):
		grouped_inputs = []
		new_chunk = list()
		for i, event in enumerate(events):
			if event.transaction.amount > 0: #is paycheck
				new_chunk.append(event)
			else: #is bill
				if len(new_chunk) != 0: # chunk not empty
					new_chunk.append(event)
				if i == (len(events) - 1) or events[i+1] > 0: # if i is last element or next is positive
					grouped_inputs.append(new_chunk)
					new_chunk = list()
		Paychunk.chunked_transactions = grouped_inputs
		for chunk in Paychunk.chunked_transactions:
			if len(chunk) >= 1:
				print(chunk[0].transaction.amount)
			else:
				print(chunk)
		Paychunk.assign_objects()

	@classmethod
	def create_num_chunks(self, inputs):
		grouped_inputs = []
		new_chunk = list()
		for i, num in enumerate(inputs):
			if num > 0: #is paycheck
				new_chunk.append(num)
			else: #is bill
				if len(new_chunk) != 0: # chunk not empty
					new_chunk.append(num)
				if i == (len(inputs) - 1) or inputs[i+1] > 0: # if i is last element or next is positive
					grouped_inputs.append(new_chunk)
					new_chunk = list()
		Paychunk.chunked_transactions = grouped_inputs
		print(grouped_inputs)
		Paychunk.assign_objects()

	@classmethod
	def assign_objects(self):
		all_paychunks = []
		for chunk in Paychunk.chunked_transactions:
			total = solvency.calculate_total(chunk)
			paychunk = Paychunk(total, chunk)
			all_paychunks.append(paychunk)
		Paychunk.all_paychunks = all_paychunks

	@classmethod
	def find_contendors(self, forward_paychunks, prev_paychunk):
		contendors = []
		contendors.append(prev_paychunk)
		for j, chunk in enumerate(forward_paychunks):
			if chunk.average < prev_paychunk.average:
				contendors.append(chunk)
			else:
				break
		return contendors

	@classmethod
	def totals_from_contendors(self, contendors):
		totals = []
		for contendor in contendors:
			totals.append(contendor.average)
		return totals

	@classmethod
	def totals_from_paychunks(self, all_paychunks):
		totals = []
		for paychunk in all_paychunks:
			totals.append(paychunk.total)
		return totals

def find_average(inputs):
	total = solvency.calculate_total(inputs)
	total /= len(inputs)
	return total
