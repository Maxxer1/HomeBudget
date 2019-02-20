from app import db
from currency_rate_scheduler import rates

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