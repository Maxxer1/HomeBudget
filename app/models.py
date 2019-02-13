from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import requests
from currency_rate_scheduler import rates


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    logins = db.relationship('UserLogin', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')
    incomes = db.relationship('Income', backref='user', lazy='dynamic')
    accounts = db.relationship('Account', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<{} {}>'.format(__class__.__name__, self.username)


class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    ip = db.Column(db.String(16), index=True)
    city = db.Column(db.String(128), index=True)
    country = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # TODO Parametrize function with ip
    @staticmethod
    def get_user_location():
        '''Returns user city and country based on his ip adress'''
        r = requests.get(
            'http://api.ipstack.com/89.64.42.127?access_key=3d7a1cdae74b6991679f35d39484dc8c')
        data = r.json()
        return data['city'], data['country_name']

    def __repr__(self):
        return '{} {}'.format(__class__.__name__, self.ip)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(128), default=None)
    is_expense = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expenses = db.relationship('Expense', backref='category', lazy='dynamic')
    incomes = db.relationship('Income', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<{} {}>'.format(__class__.__name__, self.name)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(128), index=True)
    ammout = db.Column(db.Float(precision=6))
    description = db.Column(db.String(128), index=True, default=None)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return '<{} {}>'.format(__class__.__name__, self.name)


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(128), index=True)
    ammout = db.Column(db.Float(precision=6))
    description = db.Column(db.String(128), index=True, default=None)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return '<{} {}>'.format(__class__.__name__, self.name)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    balance = db.Column(db.Float(precision=6))
    description = db.Column(db.String(128), index=True, nullable=True)
    currency = db.Column(db.String(8), index=True)
    account_type = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    incomes = db.relationship('Income', backref='account', lazy='dynamic')
    expenses = db.relationship('Expense', backref='account', lazy='dynamic')

    _euro_rate = rates['rates']['EUR']
    _usd_rate = rates['rates']['USD']
    _gbp_rate = rates['rates']['GBP']

    def lower_balance(self, ammout):
        '''Lowers account balance by given ammout'''
        self.balance = self.balance - float(ammout)
        return self.balance

    def increment_balance(self, ammout):
        '''Increments accountbalance by given ammout'''
        self.balance = self.balance + float(ammout)
        return self.balance

    def convert_balance(self, foreign_currency):
        '''Converts balance of single account to desired currency'''
        if self.currency == 'EUR':
            self.balance = self.convert_from_euro(foreign_currency)
        elif self.currency == 'USD':
            self.balance = self.convert_from_usd(foreign_currency)
        elif self.currency == 'GBP':
            self.balance = self.convert_from_gbp(foreign_currency)
        elif self.currency == 'PLN':
            self.balance = self.convert_from_pln(foreign_currency)
        return self.balance

    def convert_from_pln(self, foreign_currency):
        if foreign_currency == 'EUR':
            self.balance = float(self.balance) *  self._euro_rate
        elif foreign_currency == 'USD':
            self.balance = float(self.balance) * self._usd_rate
        elif foreign_currency == 'GBP':
            self.balance = float(self.balance) * self._gbp_rate
        return round(self.balance, 2)

    def convert_from_euro(self, foreign_currency):
        if foreign_currency == 'PLN':
            self.balance = float(self.balance) / self._euro_rate
        elif foreign_currency == 'USD':
            self.balance = float(self.balance) * (self._euro_rate / self._usd_rate)
        elif foreign_currency == 'GBP':
            self.balance = float(self.balance) * (self._euro_rate / self._gbp_rate)
        return round(self.balance, 2)

    def convert_from_usd(self, foreign_currency):
        if foreign_currency == 'PLN':
            self.balance = float(self.balance) / self._usd_rate
        elif foreign_currency == 'EUR':
            self.balance = float(self.balance) * (self._usd_rate / self._euro_rate)
        elif foreign_currency == 'GBP':
            self.balance = float(self.balance) * (self._gbp_rate / self._usd_rate)
        return round(self.balance, 2)

    def convert_from_gbp(self, foreign_currency):
        if foreign_currency == 'PLN':
            self.balance = float(self.balance) / self._gbp_rate
        elif foreign_currency == 'EUR':
            self.balance = float(self.balance) * (self._gbp_rate / self._euro_rate)
        elif foreign_currency == 'USD':
            self.balance = float(self.balance) * (self._gbp_rate / self._usd_rate)
        return round(self.balance, 2)


    def __repr__(self):
        return '<{} {}>'.format(__class__.__name__, self.name)
