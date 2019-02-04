from app import app
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user
from app.models import User
from datetime import timedelta
from error_messages import ErrorMessage


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
            login_user(user, remember=request.form.get('remember-me'), duration=timedelta(minutes=15))
            return redirect(url_for('index'))
        return render_template('login.html', error_message=ErrorMessage.LOGIN_CREDENTIALS_INVALID.value)
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
