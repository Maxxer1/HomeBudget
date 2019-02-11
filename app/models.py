from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


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
    timestamp = db.Column(db.DateTime, index=True, default=datetime.isoformat(datetime.utcnow()))
    ip = db.Column(db.String(16), index=True)
    city = db.Column(db.String(128), index=True)
    country = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    expenses = db.relationship( 'Expense', backref='category', lazy='dynamic')
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

    def __repr__(self):
        return '<{} {}>'.format(__class__.__name__, self.name)