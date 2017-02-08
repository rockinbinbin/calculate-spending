import calculations
import model
import timeline
#test methods

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

def create_inputs():
	all_transactions = model.get_transaction_data(sys.argv[1])
	totals = timeline.extract_totals(all_transactions)
	#totals = [380, -250, -50, 500, -400, -50, 800, -100, 800, -300, -50, 500, -900, 500, -300]
	return totals

def main():
	inputs = create_inputs()
	if solvency.is_solvent(totals):
		calculations.Paychunk.create_chunks()
		calculations.assign_spendables(totals)
		test_total_spendings(inputs, new_paychunks)

if __name__ == '__main__':
	main()