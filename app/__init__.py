import os
from dotenv import load_dotenv 
from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps
import cloudinary

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/phongkhamdb?charset=utf8mb4'

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = '/staff/login'

app.config.MAX_PAGE = 12

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('API_KEY'),
    api_secret = os.getenv('API_SECRET'),
    secure=True
)

def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in current_user.__dict__ or current_user.role not in roles:
                return "You don't have permission to access this page"
            return func(*args, **kwargs)
        return wrapper
    return decorator

def upload_file(file):
    if file:
        return cloudinary.uploader.upload(file, folder="phongkham")
    return None

