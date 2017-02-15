import allocations
import timeline
import model
import datetime as dt
from datetime import timedelta

# Note: Since most of these tests run through tl.events or income_sources,
# it might be efficient to run one iteration and create multiple
# assertions instead of doing them sequentially.


def run_tests(tl, income_sources):
    """ Runs all unit tests
    """
    sound_calculations_overall(tl)
    timely_allocations(tl)
    increasing_evened_rates(tl)
    timeline_is_ordered(tl)
    allocations_less_than_income(tl)
    sources_satisfy_expenses(tl)
    sound_daily_spending(income_sources)
    correct_net_days(income_sources)


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
    """ Asserts timely allocations and sources
    """
    for event in tl.events:
        if event.amount > 0:
            for source in event.sources:  # bills must come after income
                assert model.str_to_date(source.get(
                    'date')) >= event.date, "BILLS PAID WITH LATER INCOME"
        else:
            for source in event.sources:  # incomes must come before bills
                assert model.str_to_date(source.get(
                    'date')) <= event.date, "INCOME ALLOCATED FOR EARLIER BILL"


def increasing_evened_rates(tl):
    """ Asserts step-wise increasing spending rates (note: rate = spending / day)
    """
    for i, event in enumerate(tl.events):
        if event.amount > 0 and (i != len(tl.events) - 1):
            assert event.evened_rate <= tl.events[
                i + 1].evened_rate, "STEP-WISE AVERAGE NOT INCREASING"


def timeline_is_ordered(tl):
    """ Asserts ordered timeline ordered with earliest to latest events
    """
    for i, event in enumerate(tl.events):
        if (i != len(tl.events) - 1):
            assert event.date <= tl.events[i + 1].date, "TIMELINE NOT ORDERED"


def allocations_less_than_income(tl):
    """ Asserts that you're not allocating more money than you get on an income event
    """
    for i, event in enumerate(tl.events):
        allocations = 0
        if event.amount > 0:
            for source in event.sources:
                allocations += source.get('amount')
            assert allocations <= event.amount, "ALLOCATED MORE THAN INCOME AMOUNT"


def sources_satisfy_expenses(tl):
    """ Asserts that expense sources add up to bill amount
    """
    for i, event in enumerate(tl.events):
        source_total = 0
        if event.amount < 0:
            for source in event.sources:
                source_total += source.get('amount')
            assert source_total == abs(
                event.amount), "BILL NOT COVERED %a" % source_total


def sound_daily_spending(income_sources):
    """ Asserts evened_rate = evened_spending / net_days
        evened_rate is the $ daily spending 
        evened_spending is the $ spendable until next income
        net_days is the num of days until next income
    """
    for i, event in enumerate(income_sources):
        assert event.get('evened_rate') == (event.get(
            'evened_spending') / event.get('net_days')), "DAILY SPENDING RATES NOT SOUND"


def correct_net_days(income_sources):
    """ Asserts net_days is days until next income
    """
    for i, event in enumerate(income_sources):
        calculated_days = 0
        if i != (len(income_sources) - 1):
            calculated_days = abs(model.str_to_date(
                event.get('date')) - model.str_to_date(income_sources[i + 1].get('date'))).days
        else:
            calculated_days = abs(
                (model.str_to_date(event.get('date')) - timeline.Timeline.default_end).days)
        assert event.get(
            'net_days') == calculated_days, "INCORRECT DAYS TIL NEXT INCOME %d" % calculated_days
