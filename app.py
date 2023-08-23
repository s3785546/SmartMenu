from flask import Flask, send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from flask_cors import CORS
from flask import session
from flask_jwt_extended import JWTManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder="frontend/build")
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*", "expose_headers": "Authorization"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bigSteve'
app.config['WTF_CSRF_SECRET_KEY'] = 'bigOldSteve'
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config['JWT_SECRET_KEY'] = 'hugeSteve'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
db = SQLAlchemy(app)
jwt = JWTManager(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(80), default="customer") 
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.role == "admin"
    
    @property
    def is_restaurant(self):
        return self.role == "restaurant"
    
    @property
    def is_customer(self):
        return self.role == "customer"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

from routes import *


if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=True)

