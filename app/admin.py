from . import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, User, Post

admin = Admin(app, name='Admin', template_mode='bootstrap4')
# Add your models here

