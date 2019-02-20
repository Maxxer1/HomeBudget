import pytest
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.mark.order1
@pytest.fixture(scope='session')
def create_user():
    user = User(username='jim', email='jim@jim.pl')
    return user

