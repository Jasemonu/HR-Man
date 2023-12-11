from flask import Flask, url_for, request, jsonify, session
from flask.templating import render_template
from models.engine.user import User

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/admin', methods=['GET'], strict_slashes=False)
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.find_user(name=username, password=password)

    if user and user['Superuser'] == True:
        # Login successful
        session['user_id'] = str(user['_id'])
        return render_template('admin_dashboard')
    else:
        return jsonify({'error': 'You are not an Admin'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug =True)