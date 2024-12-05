from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps
import cloudinary


app = Flask(__name__)

app.secret_key = 'aaa'

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/phongkhamdb?charset=utf8mb4'

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

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
            if current_user.role not in roles:
                return "You don't have permission to access this page"
            return func(*args, **kwargs)
        return wrapper
    return decorator


