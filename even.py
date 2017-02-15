import json
import pprint
from decimal import Decimal, ROUND_HALF_UP
import model
import timeline
import allocations
import unittests

# Requires: model, timeline, allocations, and unittests modules.
# Modifies: Transaction, Event, and Timeline classes.
# Effects: Models data into Transactions, builds timeline of Events,
# checks solvency, allocates income/expense sources, & computes spendable
# amounts.


def main():
    '''handles program flow, outputs JSON 
    '''
    transactions = model.get_transaction_data()
    tl = timeline.Timeline.create_timeline(transactions)

    if timeline.is_solvent(tl.events):
        primary, secondary = allocations.apply_allocations(tl)
        allocations.calculate_spendings(tl, primary, secondary)
        tl.output_timeline()

        unittests.sound_calculations_overall(tl)
        unittests.timely_allocations(tl)

if __name__ == '__main__':
    main()
