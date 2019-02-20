from app import db

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
