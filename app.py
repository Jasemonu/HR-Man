#!/usr/bin/env python3
"""Flask application"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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


# Load user details based on id passed to load_user
@login_manager.user_loader
def load_user(user_id):
    """
    Load and return the user object based on the user_id
    This function is required by Flask-Login to retrieve users from the ID
    It should return the user object or None if the user doesn't exist
    """
    return storage.get(User, user_id)


@app.route('/register', methods=['POST'])
def register_user():
    data = request.form

    # Validate presence of all required fields
    if not validate_fields(data):
        return jsonify({'error': 'All fields are required'}), 400

    # Extract data from the form
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    dob = data.get('date_of_birth')
    contact_number = data.get('phone_number')
    employment_date = data.get('employment_date')
    NID = data.get('NID')
    gender = data.get('gender')
    department = data.get('department')
    position = data.get('position')

    user = storage.find_email(User, email)
    if user:
        return jsonify({'error': 'User already exists'}), 400

    # Generate employee ID
    employee_id = generate_employee_id(first_name, last_name)

    # Generate a random password
    password = generate_random_password()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save user details in MongoDB
    user_data = {
        'staff_number': employee_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'date_of_birth': dob,
        'phone': contact_number,
        'NID': NID,
        'employment_date': employment_date,
        'gender': gender,
        'department': department,
        'position': position,
    }

    user = User(**user_data)
    user.save()

    # Send the password to the user's email
    send_email(email, password)

    return jsonify({'message': 'success', 'employee_id': employee_id}), 201


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        employee = storage.find_item('employees', {'email': email})

        if employee and employee.check_password(password, employee['hashed_password']):
            login_user(employee)

            log_event = {
                'employee_id': employee.id,
                'event_type': 'login',
                'login_time': datetime.now()
            }

            # employee.add(log_event)

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

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
