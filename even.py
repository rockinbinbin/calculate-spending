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

        income_sources = allocations.income_source_timeline(
            tl, primary, secondary)
        allocations.flow_money(income_sources)
        allocations.reassign_spending(tl, income_sources)

        tl.output_timeline()
        unittests.run_unit_tests(tl, income_sources)

if __name__ == '__main__':
    main()
