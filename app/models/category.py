from app import db

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