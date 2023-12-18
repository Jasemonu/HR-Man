#!/usr/bin/env python3
"""Flask application"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime
from models import storage
from models.user import User
from models.payroll import Payroll
import bcrypt
from models.user import random_password, gen_employee_id, send_email, valid_fields



app = Flask(__name__)

# Instatiation of Login Manger with instance of our app

app.config.update(TESTING=True, SECRET_KEY = 'samjoerosdan2023')

login_manager = LoginManager(app)
# Initializing the login manager
login_manager.init_app(app)

storage.connect()


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


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'GET':
        return render_template('employee.html')
    data = request.form

    # Validate presence of all required fields
    if not valid_fields(data):
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
    staff_number = gen_employee_id(first_name, last_name)

    # Generate a random password
    password = random_password()


    # Generate a random password
    password = random_password()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Save user details in MongoDB
    user_data = {
        'staff_number':staff_number,
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

    return jsonify({'message': 'success', 'employee_id': staff_number}), 201



@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        employee = storage.find_email(User, email)

        if employee: #and check_password(password, employee.password):
            login_user(employee)
            # employee.add(log_event)
            log_event = {
                'employee_id': employee.id,
                'event_type': 'login',
                'login_time': datetime.now()
            }

            # Logged in successfully
            if employee.Superuser:
                session['user_id'] = str(employee.id)
                return redirect(url_for('home'))
            return redirect(url_for('home'))
        return 'Invalid credentials'

    return render_template('login.html')


@app.route('/home', strict_slashes=False)
def home():
    return render_template('dashboard.html')

@app.route('/employees', methods=['GET'], strict_slashes=False)
@login_required
def get_employees():
    try:
        # Check if user is a Superuser
        if not current_user.Superuser:
            message = {'error': 'Access denied. Only superusers can view the employee list.'}
            return jsonify(message), 403

        # Return list of employees in the database
        employee_list = storage.all(User)
        print(employee_list)

        return render_template('listemployees.html', rows=employee_list)
    except Exception as e:
        print(e)
        return str(e), 500


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete/<staff_number>', methods=['GET'])
def delete(staff_number):
    if request.method == 'GET':
        render_template('listemployees.html')
    try:
        result = storage.delete_staff(User, staff_number)
        if result:
            return f"Successfully deleted object with ID {staff_number}"
        else:
            return f"Object with ID {staff_number} not found or deletion failed", 404
    except Exception as e:
        print(e)
        return f"Deletion failed for ID {staff_number}. Please check logs for details", 500
    return jsonify({'error': 'Invalid request method'}), 405


@app.route('/update', methods=['POST', 'GET'], strict_slashes=False)
def update():
    if request.form == 'GET':
        render_template('listemployees.html')
    staff_number = request.form.get('staff_number')
    updated_data = request.form.get('updated_data')
    storage.update(staff_number, updated_data)

@app.route('/payroll', methods=['GET', 'POST'], strict_slashes=False)
def payroll():
    payroll = Payroll.objects(name='NCT78649_August_23').first()
    return render_template('viewpayroll.html', list=payroll.items)

@app.route('/earning', methods=['GET', 'POST'], strict_slashes=False)
def createpayroll():
    return render_template('salary.html')

@app.route('/deduction', methods=['GET', 'POST'], strict_slashes=False)
def deduction():
    return render_template('deductions.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
