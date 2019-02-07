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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.isoformat(datetime.utcnow()))
    ip = db.Column(db.String(16), index=True)
    city = db.Column(db.String(128), index=True)
    country = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(128))
    is_expense = db.Column(db.Boolean)
    expenses = db.relationship( 'Expense', backref='category', lazy='dynamic')
    incomes = db.relationship('Income', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(128), index=True)
    ammout = db.Column(db.Float(precision=6))
    description = db.Column(db.String(128), index=True, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Expense {}>'.format(self.name)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(128), index=True)
    ammout = db.Column(db.Float(precision=6))
    description = db.Column(db.String(128), index=True, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Income {}>'.format(self.name)
