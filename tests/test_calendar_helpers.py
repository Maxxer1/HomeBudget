import calendar_helpers
import pytest
import random
from calendar import Calendar
from app.models import Expense


def test_get_years():
    helpers_years = []
    test_years = []
    start = random.randint(2000, 2050)
    end = random.randint(2051, 2100)
    (test_years.append(year) for year in range(start, end))
    (helpers_years.append(year)
     for year in calendar_helpers.get_years(start, end))
    assert helpers_years == test_years


def prepare_month_dates(year, month):
    calendar = Calendar()
    dates = calendar.itermonthdates(year, month)
    month_dates = []
    for date in dates:
        if date.month == month:
            month_dates.append(date)
    return month_dates


def test_get_dates():
    year = random.randint(2000, 2100)
    month = random.randint(1, 12)
    test_dates = prepare_month_dates(year=year, month=month)
    dates = calendar_helpers.get_dates(year=year, month=month)
    returned_dates = []
    for date in dates:
        returned_dates.append(date)
    assert test_dates == returned_dates