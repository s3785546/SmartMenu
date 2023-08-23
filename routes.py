from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, User, login_manager
from forms import LoginForm
from flask import jsonify, request, session
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request

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

@app.route('/api/current_user/', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'role': user.role
        })
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401



@app.route('/api/dashboard/')
@jwt_required() 
def dashboard():
    if current_user.role != "restaurant":
        return "Access Forbidden", 403
    return render_template('restaurantDashboard.html')

@app.route('/api/logout/', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


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
    token = request.headers.get('Authorization')
    print("Received Token:", token) 

    try:
        verify_jwt_in_request()  
        identity = get_jwt_identity()
        user = User.query.get(identity) 
        if user:
            role = user.role
            is_auth = True
        else:
            role = None
            is_auth = False
        print("JWT Identity:", identity) 
    except Exception as e:
        print("Error:", e)  
        is_auth = False
        role = None

    return jsonify({
        'is_authenticated': is_auth,
        'role': role
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
