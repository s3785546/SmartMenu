from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, User, login_manager
from forms import LoginForm
from flask import jsonify, request

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/create_user/', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.json
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        age = data['age'] if 'age' in data else None
        role = data['role']

        user = User(firstname=firstname, lastname=lastname, email=email, password=password, age=age, role=role)
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": True})

@app.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        login_user(user)
        return jsonify({"success": True, "message": "Logged in successfully"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401


@app.route('/api/dashboard/')
@login_required
def dashboard():
    if current_user.role != "restaurant":
        return "Access Forbidden", 403
    return render_template('restaurantDashboard.html')

@app.route('/api/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/users/') 
def list_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'role': user.role,
        'email': user.email,
        'age': user.age,
        'created_at': user.created_at,
        'is_active': user.is_active
    } for user in users]) 

@app.route('/api/is_authenticated/')
def is_authenticated():
    return jsonify({
        'is_authenticated': current_user.is_authenticated,
        'role': getattr(current_user, 'role', None)
    })


@app.route('/api/view_users/')  
def view_users():
    try:
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'role': user.role,
            'email': user.email,
            'age': user.age,
            'created_at': user.created_at,
            'is_active': user.is_active
        } for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/')
def hello():
    return render_template('index.html')

@app.route('/api/index/')
def index():
    return render_template('index.html')
