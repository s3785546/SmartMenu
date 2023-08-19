from flask import render_template, request, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app import app, db, User, login_manager
from forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age'] if request.form['age'] else None
        role = request.form['role']

        user = User(firstname=firstname, lastname=lastname, email=email, password=password, age=age, role=role)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_user.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/users/') 
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users) 

@app.route('/view_users/')  
def view_users():
    all_users = User.query.all()  
    return render_template('view_users.html', users=all_users) 

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/index/')
def index():
    return render_template('index.html')
