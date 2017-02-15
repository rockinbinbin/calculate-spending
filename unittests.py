import allocations
import timeline


def sound_calculations_overall(tl):
    """ Asserts overall spendings + allocations == incomes
    """
    allocations = 0
    spendings = 0
    income_total = 0
    for event in tl.events:
        if event.amount > 0:
            for source in event.sources:
                allocations += source['amount']
            spendings += event.spendable
            income_total += event.amount

    assert spendings + allocations == income_total, "NOT SOUND CALCULATIONS"


# def sound_income_allocations(tl):
#     """ Asserts each income allocation + spendable + (net - spendable) == net
#     """
#     for event in tl.events:
#         if event.amount > 0:
#             allocations = 0
#             for source in event.sources:
#                 allocations += source.get('amount')
#             allocated_spendings = event.amount - event.spendable
#             if (allocations + event.spendable + allocated_spendings) != event.amount:
#                 event.print_event()
#             #assert (allocations + event.spendable + allocated_spendings) == event.amount, "NOT SOUND %d" %allocations

# allocations = 340