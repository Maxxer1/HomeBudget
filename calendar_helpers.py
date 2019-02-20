from calendar import Calendar
from datetime import date

calendar = Calendar()


def get_dates(year, month):
    '''Returns dates in given month from 1st to last day

    Keyword arguments:
    month -- month as int
    year -- years as int
    '''

    month_dates = calendar.itermonthdates(year, month)
    for date in month_dates:
        if date.month is month:
            yield date


def filter_expenses_by_month_year(expenses, dates):
    '''Yileds expense filtered by given dates in month

    Keyword arguments:
    expenses -- list of Expense object
    dates -- dates in month as list of date object
    '''

    for expense in expenses:
        for date in dates:
            if expense.date.month != date.month:
                break
            if expense.date.month == date.month and expense.date.year == date.year:
                yield expense
                break


def filter_incomes_by_month_year(incomes, dates):
    '''Yields incomes filtered by given dates in month

    Keyword arguments:
    incomes -- list of Income object
    dates -- dates in month as list of date object
    '''

    for income in incomes:
        for date in dates:
            if income.date.month != date.month:
                break
            if income.date.month == date.month and income.date.year == date.year:
                yield income
                break


def get_years(start, end):
    '''Returns list of years between ranges

    Keyword arguments:
    start -- date from where to iterate as int
    end -- date at which stop the iteration as int
    ''' 

    years = []
    if start > end:
        raise ValueError('End is bigger than start')
    for year in range(start, end):
        years.append(year)
    return years


months = {'January': 1,
          'February': 2,
          'March': 3,
          'April': 4,
          'May': 5,
          'June': 6,
          'July': 7,
          'August': 8,
          'September': 9,
          'October': 10,
          'November': 11,
          'December': 12}

years = get_years(start=2010, end=2030)
