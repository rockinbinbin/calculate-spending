import calculations
import model
import timeline
#test methods


# ensure that allocations + spendable = income event


# run after output
def total_averages_do_equal_nets():
	total_net_total = 0
	total_average = 0
	for paychunk in Paychunk.all_paychunks:
		total_net_total += paychunk.net_total
		total_average += paychunk.evened_rate
	if total_net_total == total_average:
		return True
	else:
		return False

