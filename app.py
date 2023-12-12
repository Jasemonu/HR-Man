#!/usr/bin/env python3
"""Flask application"""

from flask import Flask, url_for, request, jsonify, session, redirect
from flask.templating import render_template
from models.engine.user import User
from flask_login import LoginManager, login_user
from datetime import datetime
from models.engine.storage import Storage

app = Flask(__name__)

# Instatiation of Login Manger with instance of our app
login_manager = LoginManager(app)
# Initializing the login manager
login_manager.init_app(app)

storage = Storage()
user = User()


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Load user details base on id passed to load_user
@login_manager.user_loader
def load_user(user_id):
    """
    Load and return the user object based on the user_id
    This function is required by Flask-Login to retrieve users from the ID
    It should return the user object or None if the user doesn't exist
     """
    return storage.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        employee = User.find_user(email=email)

        if (
            employee
            and employee.check_password(
                password, employee['hashed_password']
            )
        ):
            login_user(employee)

            log_event = {
                'employee_id': employee.get('employee_id'),
                'event_type': 'login',
                'login_time': datetime.now()
            }
            employee.add(log_event)

            # Logged in successfully
            return render_template('user_dashboard.html')
        return 'Invalid credentials'
    return render_template('login.html')


@app.route('/admin', methods=['POST'], strict_slashes=False)
def admin_login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = User.find_user(name=username)

        if user and user.check_password(password, user['hashed_password']):
            if user['Superuser'] == True:
                # Login successful
                session['user_id'] = str(user['_id'])
                return render_template('admin_dashboard')
        else:
            return redirect(url_for('home.html'))
            
    return jsonify({'error': 'You are not an Admin'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
