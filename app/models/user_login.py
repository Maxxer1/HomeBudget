from app import db
import requests
from datetime import datetime

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