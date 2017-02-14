import allocations
import timeline
import even

# run after output
def sound_income_allocations(tl):
	allocations = 0
	spendings = 0
	income_total = 0
	for event in tl.events:
		if event.amount > 0:
			for source in event.sources:
				allocations += source['amount']
			spendings += event.spendable
			income_total += event.amount
	if spendings + allocations == income_total:
		print('sound')
		return True
	else:
		print('not sound')
		return False