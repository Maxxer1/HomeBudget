import requests

# TODO Parametrize function with ip
def get_user_location():
    r = requests.get('http://api.ipstack.com/89.64.42.127?access_key=3d7a1cdae74b6991679f35d39484dc8c')
    data = r.json()
    return data['city'], data['country_name']
