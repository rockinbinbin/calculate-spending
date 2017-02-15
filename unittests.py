import allocations
import timeline


def sound_income_allocations(tl):
    """ returns True if overall spendings + allocations == incomes
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
    if spendings + allocations == income_total:
        return True
    else:
        print('not sound')
        return False
