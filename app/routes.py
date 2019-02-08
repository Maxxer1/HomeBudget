from app import app, db
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, UserLogin, Category, Expense, Income
from datetime import timedelta
from error_messages import ErrorMessage
from helpers import get_user_location


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
            city, country = get_user_location()
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


@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    categories = enumerate(Category.query.all(), start=1)
    if request.method == 'POST':
        category = Category.query.filter_by(name=request.form.get('name')).first()
        if category is not None:
            return render_template('categories.html', error_message=ErrorMessage.CATEGORY_ALREADY_EXISTS.value)
        category = Category(name=request.form.get('name'), is_expense=bool(int(request.form.get('expense-or-income'))),
                            description=request.form.get('description'))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('categories.html', categories=categories)


@app.route('/incomes', methods=['GET', 'POST'])
@login_required
def incomes():
        categories = Category.query.filter_by(is_expense=False)
        incomes = enumerate(Income.query.all(), start=1)
        if request.method == 'POST':
            category = Category.query.filter_by(name=request.form.get('category')).first()
            income = Income(date=request.form.get(
            'date'), name=request.form.get('name'), ammout=request.form.get('ammout'),
            description=request.form.get('description'), category=category)
            db.session.add(income)
            db.session.commit()
            return redirect(url_for('incomes'))
        return render_template('incomes.html', categories=categories, incomes=incomes)


@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    categories = Category.query.filter_by(is_expense=True)
    expenses = enumerate(Expense.query.all(), start=1)
    if request.method == 'POST':
        category  = Category.query.filter_by(name=request.form.get('category')).first()
        expense = Expense(date=request.form.get(
            'date'), name=request.form.get('name'), ammout=request.form.get('ammout'),
            description=request.form.get('description'), category=category)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('expenses'))
    return render_template('expenses.html', categories=categories, expenses=expenses)
