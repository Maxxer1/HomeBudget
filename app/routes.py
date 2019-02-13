from app import app, db
from flask import render_template, url_for, request, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, UserLogin, Category, Expense, Income, Account
from datetime import timedelta
from error_messages import ErrorMessage
from helpers import calculate_total_balance, lower_balance, increment_balance, convert_balance, convert_total_balance, get_currency_rate_date
from account_types import account_types
from currencies import currencies


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and user.check_password(request.form.get('password')):
            login_user(user, remember=request.form.get(
                'remember-me'), duration=timedelta(seconds=15))
            city, country = UserLogin.get_user_location()
            user_login_data = UserLogin(
                ip=request.remote_addr, city=city, country=country, user=user)
            db.session.add(user_login_data)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('login.html', error_message=ErrorMessage.LOGIN_CREDENTIALS_INVALID.value)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_exists = User.query.filter_by(
            username=request.form.get('username')).first()
        email_exists = User.query.filter_by(
            email=request.form.get('email')).first()
        if username_exists:
            return render_template('register.html', error_message=ErrorMessage.USERNAME_ALREADY_EXISTS.value)
        elif email_exists:
            return render_template('register.html', error_message=ErrorMessage.EMAIL_ALREADY_EXISTS.value)
        elif request.form.get('password') != request.form.get('confirm_password'):
            return render_template('register.html', error_message=ErrorMessage.PASSWORD_DONT_MATCH.value)
        user = User(username=request.form.get('username'),
                    email=request.form.get('email'))
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    accounts = Account.query.filter_by(user=current_user)
    if request.method == 'POST':
        account = Account.query.filter_by(user=current_user,
                                          name=request.form.get('name')).first()
        if account is not None:
            return render_template('accounts.html', error_message=ErrorMessage.ACCOUNT_ALREADY_EXISTS.value,
                                   account_types=account_types, accounts=enumerate(accounts, start=1),
                                   currencies=currencies, currency_rate_date=get_currency_rate_date())
        account = Account(name=request.form.get('name'), balance=request.form.get('balance'),
                          description=request.form.get('description'), currency=request.form.get('currency'),
                          account_type=request.form.get('account_type'), user=current_user)
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('accounts'))
    return render_template('accounts.html', account_types=account_types, accounts=enumerate(accounts, start=1),
                           currencies=currencies, currency_rate_date=get_currency_rate_date())


@app.route('/change_currency', methods=['POST'])
def change_currency():
    if request.method == 'POST':
        if request.form.get('reset'):
            return redirect(url_for('accounts'))
        accounts = Account.query.filter_by(user=current_user)
        total_balance = convert_total_balance(
            accounts, request.form.get('currency'))
        for account in accounts:
            account.currency = request.form.get('currency')
        return render_template('accounts.html', account_types=account_types, accounts=enumerate(accounts, start=1),
                               total_balance=total_balance, currencies=currencies, 
                               total_balance_currency=request.form.get('currency'), currency_rate_date=get_currency_rate_date())


@app.route('/delete_account', methods=['POST'])
def delete_account():
    account_to_delete = Account.query.filter_by(user=current_user,
                                                name=request.form.get('account')).first()
    db.session.delete(account_to_delete)
    db.session.commit()
    return redirect(url_for('accounts'))


@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    categories = enumerate(Category.query.filter_by(user=current_user).order_by(
        Category.is_expense.desc()).all(), start=1)
    if request.method == 'POST':
        category = Category.query.filter_by(user=current_user,
                                            name=request.form.get('name')).first()
        if category is not None:
            return render_template('categories.html', error_message=ErrorMessage.CATEGORY_ALREADY_EXISTS.value,
                                   categories=categories)
        category = Category(name=request.form.get('name'), is_expense=bool(int(request.form.get('expense-or-income'))),
                            description=request.form.get('description'), user=current_user)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('categories.html', categories=categories)


@app.route('/delete_category', methods=['POST'])
def delete_category():
    category_to_delete = Category.query.filter_by(user=current_user,
                                                  name=request.form.get('category')).first()
    db.session.delete(category_to_delete)
    db.session.commit()
    return redirect(url_for('categories'))


@app.route('/incomes', methods=['GET', 'POST'])
@login_required
def incomes():
    categories = Category.query.filter_by(user=current_user, is_expense=False)
    accounts = Account.query.filter_by(user=current_user)
    incomes = enumerate(Income.query.filter_by(user=current_user).order_by(
        Income.date.desc()).all(), start=1)
    if request.method == 'POST':
        category = Category.query.filter_by(user=current_user,
                                            name=request.form.get('category')).first()
        account = Account.query.filter_by(user=current_user,
                                          name=request.form.get('account')).first()
        income = Income(date=request.form.get(
            'date'), name=request.form.get('name'), ammout=request.form.get('ammout'),
            description=request.form.get('description'), category=category, user=current_user, account=account)
        increment_balance(account, income)
        db.session.add(income, account)
        db.session.commit()
        return redirect(url_for('incomes'))
    return render_template('incomes.html', categories=categories, incomes=incomes, accounts=accounts)


@app.route('/delete_income', methods=['POST'])
def delete_income():
    account = Account.query.filter_by(user=current_user, name=request.form.get('account')).first()
    income_to_delete = Income.query.filter_by(user=current_user,
                                              name=request.form.get('income')).first()
    lower_balance(account, income_to_delete)
    db.session.delete(income_to_delete)
    db.session.commit()
    return redirect(url_for('incomes'))


@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    categories = Category.query.filter_by(user=current_user, is_expense=True)
    accounts = Account.query.filter_by(user=current_user)
    expenses = enumerate(Expense.query.filter_by(user=current_user).order_by(
        Expense.date.desc()).all(), start=1)
    if request.method == 'POST':
        category = Category.query.filter_by(user=current_user,
                                            name=request.form.get('category')).first()
        account = Account.query.filter_by(user=current_user,
                                          name=request.form.get('account')).first()
        expense = Expense(date=request.form.get(
            'date'), name=request.form.get('name'), ammout=request.form.get('ammout'),
            description=request.form.get('description'), category=category, user=current_user, account=account)
        lower_balance(account, expense)
        db.session.add(account, expense)
        db.session.commit()
        return redirect(url_for('expenses'))
    return render_template('expenses.html', categories=categories, expenses=expenses, accounts=accounts)


@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    expense_to_delete = Expense.query.filter_by(user=current_user,
                                                name=request.form.get('expense')).first()
    db.session.delete(expense_to_delete)
    db.session.commit()
    return redirect(url_for('expenses'))
