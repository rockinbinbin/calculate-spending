from __future__ import division, print_function
import datetime as dt
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange
import solvency
import timeline
import model

#Exposed
def calculate_evened_spending(tl):
	Period.assign_objects(tl)
	flow_money(tl)
	Period.reassign_spending_per_period()

	for i, period in enumerate(tl.periodic_events):
		evened_spending = Period.all_periods[i].evened_spending
		for event in period:
			if event.income_type == model.Income_Type.PRIMARY:
				event.spendable = evened_spending
				break
	return tl.periodic_events

	# for period in Period.all_periods:
	# 	Period.print_period(period)

def flow_money(tl):
	count = 0
	while (True):
		for i, period in enumerate(Period.all_periods):
			later_periods = Period.all_periods[i+1:]

			candidates = Period.find_candidates(later_periods, period)
			evened_rate = find_average_candidates(candidates)
			period.evened_rate = evened_rate

			for candidate in candidates:
				index = Period.all_periods.index(candidate)
				Period.all_periods[index].evened_rate = evened_rate
		count += 1
		if count == 10:
			break
	return tl

#Internal class to help calculate evened_spending
class Period(object):
	all_periods = [] 
	def __init__(self, net_total=0, values=[], evened_rate=0, income_event=0, initial_rate=0, net_days=1, evened_spending=0, carry_over=0):
		self.net_total = net_total #net income after bills
		self.values = values # Events in this chunk.
		self.income_event = income_event # Income event that allows money provisioned in this chunk.
		self.initial_rate = initial_rate # initial daily spending. debug purposes
		self.net_days = net_days # days until next income
		self.evened_rate = initial_rate #trickled average
		self.evened_spending = evened_spending #final 
		self.carry_over = carry_over

	@classmethod
	def assign_objects(self, tl):

		for period in tl.periodic_events:
			#net_total = solvency.total_from_events(period)   #REDO NET TOTAL CALCULATION HEREEEE
			#net_total = Period.assign_nets()
			new_period = Period(values=period, income_event=period[0])
			Period.all_periods.append(new_period)
		Period.assign_nets()
		Period.assign_net_spending_values()

	@classmethod
	def assign_net_spending_values(self):
		for i, period in enumerate(Period.all_periods):
			period.net_days = Period.net_days(i)
			period.initial_rate = period.net_total / period.net_days
			period.evened_rate = period.initial_rate

	@classmethod
	def net_days(self, index):
		period = Period.all_periods[index]
		dividing_factor = 1 # num of days til next paychunk
		if index == (len(Period.all_periods) - 1): # is last paychunk
			dividing_factor = timeline.Timeline.default_end - period.income_event.date
		else:
			dividing_factor = Period.all_periods[index+1].income_event.date - period.income_event.date
		days = dividing_factor.days
		if days == 0:
			# Combine events on the same day?
			days = 1
		return days

	@classmethod
	def assign_nets(self):
		# first add up each period's first day incomes.
		# sum with rest of expenses (if income comes up, sum together to assign next period's carry_over value.)
		# loop through all periods, sum carry-over + first-day incomes + rest of expenses
		for i, period in enumerate(Period.all_periods):
			net_amount = 0
			carry_over_amount = 0
			for j, event in enumerate(period.values):
				if event.date == period.income_event.date and event.amount > 0: # income & on first day
					net_amount += event.amount
				else:
					if event.amount < 0:
						net_amount += event.amount
					else:
						carry_over_amount += event.amount
			period.net_total = net_amount
			if i != (len(Period.all_periods)-1): # not last element
				Period.all_periods[i+1].carry_over = carry_over_amount
			else:
				period.carry_over = carry_over_amount # last element

		for i, period in enumerate(Period.all_periods):
			period.net_total += period.carry_over



	@classmethod
	def find_candidates(self, later_periods, period):
		candidates = []
		candidates.append(period)
		for j, chunk in enumerate(later_periods):
			if chunk.evened_rate < period.evened_rate: #Question: < or <=?
				candidates.append(chunk)
			else:
				break
		return candidates

	@classmethod
	def reassign_spending_per_period(self):
		for period in Period.all_periods:
			period.evened_spending = period.evened_rate * period.net_days
			Period.print_period(period)

	@classmethod
	def print_period(self, period):
		net_total = str(Decimal(period.net_total).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
		initial_rate = str(Decimal(period.initial_rate).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
		evened_rate = str(Decimal(period.evened_rate).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) # final $ per day
		evened_spending = str(Decimal(period.evened_spending).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)) # final $ per chunk (income event)
		print("initial_net_total:", net_total, "net_days:", period.net_days, "initial_rate:", initial_rate, "evened_rate:", evened_rate, "evened_spending:", evened_spending)

	@classmethod
	def print_transaction_amounts(self):
		for period in Period.all_periods:
			for event in period:
				print(event.amount)

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

