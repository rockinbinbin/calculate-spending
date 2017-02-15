import allocations
import timeline
import model
import datetime as dt


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


def timely_allocations(tl):
    for event in tl.events:
        if event.amount > 0:
            for source in event.sources:
                assert model.str_to_date(source.get('date')) >= event.date
        else:
            for source in event.sources:
                assert model.str_to_date(source.get('date')) <= event.date

