import calendar_helpers
import pytest
import random
from calendar import Calendar
from app.models.user import User
from app.models.expense import Expense
from app.models.account import Account
from app.models.category import Category
from app.models.income import Income
from account_types import account_types
from currencies import currencies
import uuid
from datetime import date


def test_get_years():
    helpers_years = []
    test_years = []
    start = random.randint(2000, 2050)
    end = random.randint(2051, 2100)
    (test_years.append(year) for year in range(start, end))
    (helpers_years.append(year)
     for year in calendar_helpers.get_years(start, end))
    assert test_years == helpers_years


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


@pytest.fixture(scope='package')
def test_user():
    user = User(username='Jimbo', email='jimbo@jimbo.pl', password='jimbo')
    return user


@pytest.fixture(scope='package')
def test_account(test_user):
    account = Account(name='test account', balance=123.33,
                      description='random desc', currency=currencies[1],
                      account_type=account_types[0], user=test_user)
    return account


@pytest.fixture(scope='package')
def test_expense_category(test_user):
    category = Category(name='Food', description='random expense desc',
                        is_expense=True, user=test_user)
    return category


@pytest.fixture(scope='package')
def test_income_category(test_user):
    category = Category(name='Salary', description='random icome desc',
                        is_expense=False, user=test_user)


@pytest.fixture(scope='package')
def test_expeses(test_user, test_expense_category, test_account):
    expenses = []
    for i in range(10):
        day, month, year = random.randint(1, 28), random.randint(
            1, 12), random.randint(2000, 2010)
        expense_date = date(year, month, day)
        ammout = random.uniform(0.1, 100)
        expense = Expense(date=expense_date, name='Random expense-' + str(uuid.uuid4()), ammout=ammout, description='random desc' + str(uuid.uuid4()),
                          category=test_expense_category, user=test_user, account=test_account)
        expenses.append(expense)
    return expenses


@pytest.fixture(scope='package')
def test_incomes(test_user, test_income_category, test_account):
    incomes = []
    for i in range(10):
        day, month, year = random.randint(1, 28), random.randint(
            1, 12), random.randint(2000, 2010)
        income_date = date(year, month, day)
        ammout = random.uniform(0.1, 100)
        income = Income(date=income_date, name='Random income-' + str(uuid.uuid4()), ammout=ammout, description='random desc' + str(uuid.uuid4()),
                        category=test_income_category, user=test_user, account=test_account)
        incomes.append(income)
    return incomes


@pytest.fixture(scope='package')
def test_dates():
    year = random.randint(2000, 2010)
    month = random.randint(1, 12)
    return calendar_helpers.get_dates(year, month)


def test_filter_expenses_by_month_year(test_expeses, test_dates):
    test_fitlered_expenses = []
    filtered_expenses = []
    for test_expense in test_expeses:
        for test_date in test_dates:
            if test_expense.date.month != test_date.month:
                break
            if test_expense.date.month != test_date.month and test_expense.date.year == date.year:
                test_fitlered_expenses.append(test_expense)
    for expense in calendar_helpers.filter_expenses_by_month_year(test_expeses, test_dates):
        filtered_expenses.append(expense)
    assert test_fitlered_expenses == filtered_expenses


def test_filter_incomes_by_month_year(test_incomes, test_dates):
    test_filtered_incomes = []
    filtered_incomes = []
    for test_income in test_incomes:
        for test_date in test_dates:
            if test_income.date.month != test_date.month:
                break
            if test_income.date.month != test_date.month and test_income.date.year == date.year:
                test_filtered_incomes.append(test_income)
    for income in calendar_helpers.filter_incomes_by_month_year(test_incomes, test_dates):
        filtered_incomes.append(income)
    assert test_filtered_incomes == filtered_incomes