#!/usr/bin/env python3
"""Flask application"""

import os
from flask import Flask, render_template, request, jsonify, session, redirect
from flask import send_file, url_for, flash, abort, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime, date
from models import storage
from models.attendance import Attendance
from models.user import User
from models.bank import Bank
from models.leave import Leave
from models.payroll import Payroll
from models.payslip import Payslip
from payroll import create_payroll
from payslip import create_payslip
from models.messages import Message, reply_email
import bcrypt
from mongoengine.errors import NotUniqueError
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
        flash('All fields required', 'error')
        return render_template('employee.html')

    # Extract data from the form
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    dob = data.get('date_of_birth')
    contact_number = data.get('phone')
    employment_date = data.get('employment_date')
    gender = data.get('gender')
    department = data.get('department')
    position = data.get('position')

    user = storage.find_email(User, email)
    if user:
        flash('User already exists', 'error')
        return render_template('employee.html')

    # Generate employee ID
    staff_number = gen_employee_id(first_name, last_name)

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
        'employment_date': employment_date,
        'gender': gender,
        'department': department,
        'position': position,
    }

    user = User(**user_data)
    user.save()

    # Send the password to the user's email
    try:
        send_email(email, password)
    except Exception:
        flash("Couldn't send password to employee's email")
        return redirect(url_for('register_user'))

    flash('Created successful!', 'success')
    return render_template('employee.html')



@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        employee = storage.find_email(User, email)
        if not employee:
            flash("Email doesn't exists")
            return redirect(url_for('login'))

        try:
            if bcrypt.checkpw(pwd.encode('utf-8'),
                    employee.password.encode('utf-8')):
                login_user(employee)
                # employee.add(log_event)
                log_event = {
                    'employee_id': employee.id,
                    'event_type': 'login',
                    'login_time': datetime.now()
                    }

                # Logged in successfully
                if employee.Superuser:
                    flash('Login successful!', 'success')
                    session['user_id'] = str(employee.id)
                    return redirect(url_for('home'))
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            flash('Invalid username or password', 'error')
            return render_template('login.html')
        except Exception as e:
            print(e)
            flash('Oops Somthing went wrong')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/home', strict_slashes=False)
@login_required
def home():
    users = User.objects.order_by('-created_at')
    payslips = Payslip.objects.count()
    messages = Message.objects(viewed=False)
    employees = users[:5]
    return render_template('dashboard.html', users=users.count(), payslips=payslips,
                           messages=messages, count=messages.count(), employees=employees)

@app.route('/employees', methods=['GET'], strict_slashes=False)
@login_required
def get_employees():
    try:
        # Check if user is a Superuser
        if not current_user.Superuser:
            abort(403)

        # Return list of employees in the database
        employee_list = storage.all(User)

        return render_template('listemployees.html', rows=employee_list)
    except Exception as e:
        flash('Your are not authorise', 'error')
        return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    name = current_user.first_name
    logout_user()
    flash(f'Goodbye {name}!')
    return redirect(url_for('index'))


@app.route('/update/delete', methods=['GET'], strict_slashes=False)
@login_required
def update_delete():
    try:
        # Check if user is a Superuser
        if not current_user.Superuser:
            flash('Your are not authorise', 'error')
            return redirect(url_for('home'))

        # Return list of employees in the database
        update_delete = storage.all(User)

        return render_template('update_delete.html', rows=update_delete)
    except Exception as e:
        flash('Oops something went wrong', 'error')
        return render_template('update_delete.html', rows=update_delete)



# endpoit for deleting employeees
@app.route('/delete/<string:staff_number>', methods=['DELETE'], strict_slashes=False)
def delete(staff_number):
    try:
        # search and delete employee by staff_number
        result = storage.delete_staff(User, staff_number)
        if result:
            flash('Deleted Successfully!', 'success')
            return redirect(url_for('update_delete'))

        # if no result return to the lisemployees page 
        flash('Delete unsuccessful!, check Staff Number', 'error')
        return redirect(url_for('update_delete'))
    except Exception as e:
        flash('Oops something went wrong', 'error')
        return redirect(url_for('update_delete'))
    
# This endpoit updates emploees records
@app.route('/update/<string:staff_number>', methods=['POST', 'GET'], strict_slashes=False)
def update(staff_number):
    try:
        # check if employee exist by the staff_number
        employee = User.objects(staff_number=staff_number).first()

        if request.method == 'POST':
            # retrieve data from the form and update the records 
            updated_data = request.form
            for key, value in updated_data.items():
                if hasattr(employee, key):
                    setattr(employee, key, value)
            employee.save()
            flash('Employee details updated successfully', 'success')
            return redirect(url_for('get_employees'))

        return render_template('updateemployee.html', employee=employee)

    except Exception as e:
        flash('Oops something went wrong', 'error')
        return redirect(url_for('update_delete'))


@app.route('/viewpayroll', defaults={'name': None}, strict_slashes=False)
@app.route('/viewpayroll/<string:name>', methods=['GET', 'POST'])
def payroll(name):
    list = []
    if name:
        payroll = Payroll.objects(name=name).first()
        if payroll:
            list = payroll.items
        return render_template('viewpayroll.html', list=list)
    payrolls = Payroll.objects()
    if payrolls:
        list = payrolls
    return render_template('listpayroll.html', list=list)

@app.route('/createpayroll', methods=['GET', 'POST'], strict_slashes=False)
def createpayroll():
    if request.method == 'POST':
        staff_number = request.form.get('staff_number')
        user = User.objects(staff_number=staff_number).first()
        if not user:
            flash('Staff does not exists')
            return render_template('salary.html')
        if not request.form.get('gross'):
            gross = 0
            for key, value in request.form.items():
                if key == 'staff_number' or key == 'gross':
                    continue
                gross += int(value)
            obj = request.form
            flash('Confirm Gross')
            return render_template('gross.html', gross=gross, obj=obj)
        res = create_payroll(request.form, user)
        if res == 'exists':
            flash(f'Payroll for {staff_number} exists')
            return redirect(url_for('createpayroll'))
        if not res:
            flash('Payroll unsuccessfull')
            return render_template('salary.html')
        flash('Successfully added payroll')
        return render_template('salary.html')
    return render_template('salary.html')


@app.route('/viewpayslip', defaults={'name': None})
@app.route('/viewpayslip/<name>', strict_slashes=False)
@login_required
def viewpayslip(name):
    if current_user.Superuser:
        list = []
        payslips = Payslip.objects()
        if payslips:
            list = payslips
        return render_template('listpayslip.html', list=list)
    if name and not current_user.Superuser:
        payslip = Payslip.objects(staff=current_user).first()
        if payslip:
            folder = 'static/assets/pdf/'
            for path in os.listdir(folder):
                if path == payslip.name:
                    return send_file(folder + name)
        flash('Could not open file')
        return render_template('viewpayslip.html')
    list = []
    payslips = Payslip.objects()
    if payslips is not None:
        list = payslips
    if not current_user.Superuser:
        payslips = Payslip.objects(staff=current_user)
        if payslips:
            list = payslips
    return render_template('viewpayslip.html', payslips=list)


@app.route('/createpayslip', methods=["GET", "POST"], strict_slashes=False)
@login_required
def createpayslip():
    if request.method == 'POST':
        staff_number = request.form.get('staff_number')
        staff = User.objects(staff_number=staff_number).first()
        if staff:
            res = create_payslip(request.form, staff)
            if res == 'exists':
                flash(f'Staff {staff_number} slip exists')
                return render_template('payslip.html')
            if res == 'Null':
                flash("Can't create Null payslip add earnings first")
                return redirect(url_for('createpayslip'))
            if res is None:
                flash('Oops Someting went wrong')
                return render_template('payslip.html')
            flash(f'Staff {res.staff.staff_number} payslip created')
            return render_template('payslip.html')
        flash(f"Staff {request.form.get('staff_number')} doesn't Exist")
        return render_template('payslip.html')
    return render_template('payslip.html')

@app.route('/payslips', defaults={'name': None}, strict_slashes=False)
@app.route('/payslips/<name>', methods=['GET', 'DELETE'])
@login_required
def delete_payslip(name):
    list = []
    if name:
        payslip = Payslip.objects(name=name).first()
        if payslip:
            payslip.delete()
            payslips = Payslip.objects()
            if not payslips:
                path = 'static/assets/pdf/'
                os.remove(path + name)
                list = payslips
                flash(f'Payslip {name} deleted successfully')
                return render_template('deletepayslip.html', payslips=list)
        payslips = Payslip.objects()
        if payslips:
            list = payslips
        flash(f"Payslip {name} doesn't exist")
        return render_template('deletepayslip.html', payslips=list)
    payslips = Payslip.objects()
    if payslips:
        list = payslips
    return render_template('deletepayslip.html', payslips=list)


@app.route('/profile', methods=['GET'], strict_slashes=False)
@login_required
def profile():
    bank = Bank.objects(staff=current_user).first()
    return render_template('profile.html', bank=bank)


@app.route('/update_profile', defaults={'staff': None})
@app.route('/update_profile/<staff>', methods=["GET", "POST"], strict_slashes=False)
@login_required
def update_profile(staff):
    if staff and request.method == 'POST':
        setUser = False
        setBank = False
        user = User.objects(staff_number=staff).first()
        bank = Bank.objects(staff=user).first()
        for key, value in request.form.items():
            if hasattr(user, key):
                setattr(user, key, value)
                setUser = True
            if bank:
                if hasattr(bank, key):
                    setattr(bank, key, value)
                    setBank = True
        if setUser:
            user.save()
        if not setBank:
            obj = {
                    'staff': user,
                    'name': request.form.get('name'),
                    'branch': request.form.get('branch'),
                    'code': request.form.get('code'),
                    'account_name': request.form.get('account_name'),
                    'account_number': request.form.get('account_number')
                    }
            bank = Bank(**obj)
            try:
                bank.save()
            except NotUniqueError:
                flash('Coulld not update bank')
                return redirect(url_for('profile'))
        else:
            bank.save()
        flash('Profile Update Successfull')
        return redirect(url_for('profile'))
    bank = Bank.objects(staff=current_user).first()
    return render_template('updateprofile.html', bank=bank)


@app.route('/attendance', defaults={'period': None})
@app.route('/attendance/<period>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def attendance(period):
    today = date.today()
    time = datetime.now().strftime('%H:%M')
    obj = Attendance.objects()
    if not current_user.Superuser:
        name = current_user.staff_number + today.strftime('%a')
        obj = Attendance.objects(name=name)
    if request.method == 'POST':
        name = name=request.form.get('ID') + today.strftime('%a')
        if period == 'entry':
            att = Attendance.objects(name=name).first()
            if att:
                flash('Signed in already')
                return redirect(url_for('attendance'))
            obj = {
                'staff': current_user,
                'name': name,
                'date': request.form.get('date'),
                'entry_time': request.form.get('entry_time')
                }
            n_att = Attendance(**obj)
            n_att.save()
            flash('signed in Successfull')
            return redirect(url_for('attendance'))
        if period == 'exit':
            att = Attendance.objects(name=name).first()
            if not att:
                flash('Must signed in first')
                return redirect(url_for('attendance'))
            if att.exit_time:
                flash('Signed out already please logout')
                return redirect(url_for('attendance'))
            exit = request.form.get('exit_time')
            att.update(__raw__={'$set': {'exit_time': exit}})
            att.save()
            flash('Signed out Succesfull please logout')
        return redirect(url_for('attendance'))
    return render_template('attendance.html',
                           date=today.isoformat(), time=time, rows=obj)


@app.route('/resetpwd', methods=['GET', 'POST'], strict_slashes=False)
def resetpwd():
    if request.method == 'POST':
        user = User.objects(email=request.form.get('email')).first()
        if user:
            pwd = request.form.get('password')
            confirm = request.form.get('confirmpwd')
            if pwd == confirm:
                hashpwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
                user.update(__raw__={'$set':{'password': hashpwd}})
                user.save()
                flash('Password updated Please login')
                return redirect(url_for('login'))
            flash('Password not matching')
            return redirect(url_for('resetpwd'))
        flash(f"Staff doesn't exist")
        return redirect(url_for('resetpwd'))
    return render_template('resetpwd.html')



@app.route('/messages', methods=['POST', 'GET'], defaults={'id': None})
@app.route('/messages/<string:id>', methods=['GET', 'DELETE'], strict_slashes=False)
def message(id):
    if request.method == 'DELETE' and id:
        message = storage.get(Message, id)
        if not message:
            message.delete()
            res = make_response('Message Delete Successful')
            res.headers['HX-Refresh'] = 'true'
            flash('Message Delete Successful', 'success')
            return res
        res = make_response('Message Delete Unsuccessful')
        res.headers['HX-Redirect'] = f'/messages/{id}'
        flash('Message Delete Unsuccessful', 'error')
        return res
    if request.method == 'POST':
        try:
            massage = Message(**request.form).save()
        except Exception as e:
            return "Message Not Sent"
        return "Message Sent"
    if id:
        message = storage.get(Message, id)
        if not message:
            flash("Message can't be opened")
            return redirect(url_for('message'))
        message.update(viewed=True)
        message.save()
        return render_template('viewmessage.html', message=message)
    messages = storage.all(Message)
    return render_template('messages.html', messages=messages)


@app.route('/reply', methods=['POST', 'GET'], defaults={'email': None})
@app.route('/reply/<email>', methods=['GET'], strict_slashes=False)
def reply_message(email):
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            subject = request.form.get('subject')
            message = request.form.get('message')
            reply_email(email, subject, message)
        except Exception as e:
            flash("Reply not sent, Try again")
            return redirect(url_for('reply_message'))
        message = Message.objects(email=email, reply=False).first()
        message.update(reply=True)
        message.save()
        flash('Message sent successful')
        return render_template('replymessage.html', message=message)

    message = Message.objects(email=email, reply=False).first()
    return render_template('replymessage.html', message=message)


@app.route('/leave', methods=['POST', 'GET'], strict_slashes=False)
def leave():
    if request.method == 'POST':
        data = request.form
        # Extract data from the form
        staffNumber = data.get('staff_number')
        staffName = data.get('staff_name')
        startDate = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        endDate = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
        leaveType = data.get('leave_type')

        if startDate < datetime.now():
            flash('Start date cannot be lower than current date', 'error')
            return render_template('leavereq.html')
        if endDate <= startDate:
            flash('End date should be higher than start date', 'error')
            return render_template('leavereq.html')
        leave_days = (endDate - startDate).days + 1
        user = storage.find_staff(User, staffNumber)
        leave = Leave.objects(staff=user).first()
        if not leave:
            if leave_days >= 0:
                leave_data = {
                        'staff': user,
                        'staff_name': staffName,
                        'start_date': startDate,
                        'end_date': endDate,
                        'leave_type': leaveType,
                        'requested_days': leave_days
                        }
                leave_req = Leave(**leave_data)
                leave_req.save()
            else:
                flash(f"You have 30 days leave limit", "error")
                return render_template('leavereq.html')
        if leave:
            if leave.remaining < leave_days:
                flash(f"You have only {leave.remaining} days left")
                return render_template('leavereq.html')
            leave_data = {
                    'start_date': startDate,
                    'end_date': endDate,
                    'leave_type': leaveType,
                    'requested_days': leave_days,
                    'leave_status': 'pending',
                    'comment': 'No comments'
                    }
            for key, value in leave_data.items():
                setattr(leave, key, value)
            leave.save()
            flash("Leave application successful and pending approval", "success")
            return redirect(url_for('leave_history'))
    return render_template('leavereq.html')

@app.route('/pending_leave', methods=['POST', 'GET'], strict_slashes=False)
def leave_approval():
    leave_list = storage.all(Leave)
    for dictionary in leave_list:
        staff_number = dictionary.staff.staff_number
        leave_status = dictionary['leave_status']
        if staff_number == current_user.staff_number:
            leave_list.remove(dictionary)
        if leave_status == 'Accepted':
            leave_list.remove(dictionary)
        if leave_status == 'Declined':
            leave_list.remove(dictionary)
    return render_template('leave.html', rows=leave_list)

@app.route('/process_form', methods=['POST'], strict_slashes=False)
def accept_reject():
    decision = request.form.get('decision')
    comment = request.form.get('comment')
    staff_number = request.form.get('staff_number')
    user =  storage.find_staff(User, staff_number)
    leave = Leave.objects(staff=user).first()
    if leave is None:
        abort(404)
    if len(comment) == 0:
        leave.comment = 'No comments'
    else:
        leave.comment = comment
    if decision == 'accept':
        leave.leave_status = 'Accepted'
        leave.remaining -= leave.requested_days
        flash(f"You have successfully approved {leave.staff_name}'s leave")
    elif decision == 'reject':
        leave.leave_status = 'Declined'
        flash(f"You declined {leave.staff_name}'s leave")
    else:
        flash("You can either approve or decline")
        return redirect(url_for('leave_approval'))
    leave.save()
    return redirect(url_for('leave_approval'))

@app.route('/leave_history', methods=['GET'], strict_slashes=False)
def leave_history():
    staff = current_user
    leave = Leave.objects(staff=staff).first()
    return render_template('Lhis.html', row=leave)


@app.errorhandler(404)
def page_not_found(e):
    message ={
            'Error': 404,
            'message': 'NOT FOUND return and try again'
            }
    return jsonify(message), 404

@app.errorhandler(401)
def notallowed(e):
    return render_template('error.html'), 401


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
