from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps
import cloudinary


app = Flask(__name__)

app.secret_key = '6 79ts7as b86as9 ftas907f5ta8s7f5a8s7 ft97astf87a9tf97artf897arf987rtas789 f7as8'

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/phongkhamdb?charset=utf8mb4'

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = '/staff/login'

app.config.MAX_PAGE = 12

cloudinary.config(
    cloud_name = "dbxht4ocu",
    api_key = "693848432562243",
    api_secret = "lZxC9_Cbx5fKxMIuqj_icXqFg64", # Click 'View API Keys' above to copy your API secret
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

