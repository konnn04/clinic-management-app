from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)

app.secret_key = 'aaa'

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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



