from __future__ import division, print_function
import numpy as np
import json
from pprint import pprint
import datetime as dt
import sys
import string
import operator
from collections import defaultdict
import solvency
import timeline

#Even Algorithm Module.
#Requires: Input Array of ints (for all transaction values).
#Modifies: Input Array of ints.
#Effects: Groups subarrays of ints based on payday into Paychunk objects with associated averages.
#TODO: Take average of each paychunk, and calculate spendable money / transaction.

# group array by first positive val
def create_chunks(inputs):
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
	return grouped_inputs

def find_average(inputs):
	total = solvency.calculate_total(inputs)
	total /= len(inputs)
	return total

#model data by assigning an average value to each chunk.
class Paychunk(object):
	def __init__(self, total=0, values=[], average=0):
		self.total = total # net value
		self.values = values
		self.average = total # trickled average, init to total

#look ahead to find values smaller than current paychunk.total
# if any exist, find average
# iterate to next 

#TODO: skip over contendors that have been averaged.

def find_contendors(forward_paychunks, prev_paychunk):
	contendors = []
	contendors.append(prev_paychunk)
	for j, chunk in enumerate(forward_paychunks):
		#print(chunk.total)
		if chunk.average < prev_paychunk.average:
			contendors.append(chunk)
		else:
			break
	# print(contendors)
	return contendors

def totals_from_contendors(contendors):
	totals = []
	for contendor in contendors:
		totals.append(contendor.average)
	#print(totals)
	return totals

# def __eq__(self, other):
# 	return self.Value == other.Value

def totals_from_paychunks(all_paychunks):
	totals = []
	for paychunk in all_paychunks:
		totals.append(paychunk.total)
	return totals

# Modifies all_paychunks
def trickle_down(all_paychunks):
	count = 0
	while (True):
		for i, paychunk in enumerate(all_paychunks):

			#if i != (len(all_paychunks) + 1):
			forward_paychunks = all_paychunks[i+1:]
			contendors = find_contendors(forward_paychunks, paychunk)

			contendor_totals = totals_from_contendors(contendors)
			average = find_average(contendor_totals)
			paychunk.average = average

			for contendor in contendors:
				index = all_paychunks.index(contendor)
				all_paychunks[index].average = average
		count += 1
		if count == 1:
			break
			#print(index, all_paychunks[index].average, all_paychunks[index].total)

	return all_paychunks

def assign_spendables(inputs):
	grouped_chunks = create_chunks(inputs)

	all_paychunks = []
	for chunk in grouped_chunks:
		total = solvency.calculate_total(chunk)
		paychunk = Paychunk(total, chunk)
		all_paychunks.append(paychunk)

	new_paychunks = trickle_down(all_paychunks)

	test_total_spendings(inputs, new_paychunks) #comment out in production

def test_total_spendings(inputs, new_paychunks):
	first_total = 0
	for num in inputs:
		first_total += num

	second_total = 0
	for paychunk in new_paychunks:
		second_total += paychunk.average

	if int(first_total) == int(second_total):
		print("calculations add up!")
	else:
		print(first_total, second_total)

	for paychunk in new_paychunks:
		print(paychunk.average, paychunk.total)

def main():
	#inputs = [380, -250, -50, 500, -400, -50, 800, -100, 800, -300, -50, 500, -900, 500, -300]

	grouped_chunks = create_chunks(inputs)

	all_paychunks = []
	for chunk in grouped_chunks:
		total = solvency.calculate_total(chunk)
		paychunk = Paychunk(total, chunk)
		all_paychunks.append(paychunk)

	new_paychunks = trickle_down(all_paychunks)

	for paychunk in new_paychunks:
		print(paychunk.average)

if __name__ == '__main__':
	main()