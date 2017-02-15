import sys
import json
import datetime as dt

# Requires: Nothing
# Modifies: Transaction objects
# Effects: Creates Transaction objects from input data

# Exposed Module Methods


def get_transaction_data():
    """ returns list of income & expense transaction instances 
    """
    data = parse_json()
    income_instances = create_transactions(data['incomes'])
    expense_instances = create_transactions(data['expenses'])
    for expense in expense_instances:
        expense.amount = -(expense.amount)
    transactions = income_instances + expense_instances
    return transactions


def parse_json():
    """ returns data from input file JSON 
    """
    parsed = None
    try:
        path = sys.argv[1]
    except IndexError as idx_err:
        print('Please add an input file command line arg!', idx_err)
    else:
        try:
            with open(path, 'r') as data:
                return json.load(data)
        except ValueError as val_err:
            print('json deserialization error, handle with fallbacks', val_err)


def create_transactions(data):
    """ returns list of transaction instances 
    """
    transaction_instances = []
    for item in data:
        income_type = Income_Type.UNKNOWN
        if 'type' in item:
            income_type = Income_Type.map_income_type(item['type'])
        transaction_instances.append(Transaction(
            item['name'], item['amount'], item['schedule'], income_type))
    return transaction_instances


class Frequency(object):
    MONTHLY = 0
    INTERVAL = 1
    ONE_TIME = 2

    @classmethod
    def map_frequency(cls, frequency_str):
        """ returns transaction frequency 
        """
        if frequency_str == 'MONTHLY':
            return cls.MONTHLY
        elif frequency_str == 'INTERVAL':
            return cls.INTERVAL
        elif frequency_str == 'ONE_TIME':
            return cls.ONE_TIME
        else:
            raise Exception('Frequency data error')


class Income_Type(object):
    UNKNOWN = 0
    PRIMARY = 1
    SECONDARY = 2

    @classmethod
    def map_income_type(cls, income_type_str):
        """ returns income_type 
        """
        if income_type_str == 'PRIMARY':
            return cls.PRIMARY
        elif income_type_str == 'SECONDARY':
            return cls.SECONDARY
        else:
            return cls.UNKNOWN  # expense


class Schedule(object):

    def __init__(self, schedule_data):
        self.frequency = Frequency.map_frequency(schedule_data.get('type'))
        self.start = schedule_data.get('start', 0)
        if self.start != 0:
            self.start = str_to_date(self.start)
        self.period = schedule_data.get('period', 0)
        self.days = schedule_data.get('days', 0)


class Transaction(object):

    def __init__(self, name, amount, schedule_json, income_type=Income_Type.UNKNOWN):
        self.name = name
        self.amount = amount
        self.schedule = Schedule(schedule_json)
        self.income_type = income_type

    def get_start_date(self):
        return self.schedule.start

    def get_frequency(self):
        return self.schedule.frequency

# helpers


def str_to_date(str_input):
    """ returns date object from formatted string 
    """
    date = str_input.split('-')
    return dt.date(int(date[0]), int(date[1]), int(date[2]))
