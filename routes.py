# routes.py
from flask import render_template, request, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app import app, db, Customer, login_manager
from forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

@app.route('/create_customer/', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age'] if request.form['age'] else None

        customer = Customer(firstname=firstname, lastname=lastname, email=email, password=password, age=age)
        db.session.add(customer)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_customer.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):  # Check password here
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/customers/')
def customers():
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)

@app.route('/view_customers/')
def view_customers():
    all_customers = Customer.query.all()
    return render_template('view_customers.html', customers=all_customers)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/index/')
def index():
    return render_template('index.html')