from calendar import Calendar
from datetime import date

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

calendar = Calendar()

def get_month_dates(month_number):
    dates = []
    month_dates = calendar.itermonthdates(2019,month_number)
    for date in month_dates:
        if date.month is month_number:
            dates.append(date)
    return dates


def filter_expenses_by_month(expenses, dates):
    filtered = []
    for expense in expenses:
        for date in dates:
            if expense.date == date:
                filtered.append(expense)
    return filtered


