from . import app, admin, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import NguoiDung
from flask_admin import BaseView,expose

from flask_login import current_user, login_required, logout_user
from flask import redirect, url_for, request,render_template


admin = Admin(app, name='Admin', template_mode='bootstrap4')


class UserView(ModelView):
    column_list = ('id', 'ho','ten','ngaySinh')

    # def is_accessible(self):
    #     return current_user.is_authenticated
    
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('login', next=request.url))


admin.add_view(UserView(NguoiDung, db.session))

# @app.before_request
# def before_request():
#     if request.endpoint.startswith('admin.') and not current_user.is_authenticated:
#         return redirect(url_for('login', next=request.url))





