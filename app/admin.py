from . import app, admin, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import NguoiDung,VaiTro
from flask_admin import BaseView,expose
from app import utils
# from flask import request, render_template, redirect, url_for, flash
from flask_admin.model.template import EndpointLinkRowAction
from flask_login import current_user, login_required, logout_user
from flask import redirect, url_for, request,render_template,flash


admin = Admin(app, name='Admin', template_mode='bootstrap4')

class CreateStaffView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self, *args, **kwargs):
        err_msg = ""
        if request.method.__eq__('POST'):
            ho = request.form.get('ho')
            ten = request.form.get('ten')
            ngaySinh = request.form.get('ngaySinh')
            soDienThoai = request.form.get('soDienThoai')
            email = request.form.get('email')
            taiKhoan = request.form.get('tenTK')
            matKhau = request.form.get('matKhau')
            xacNhanMK = request.form.get('xacNhanMK')
            avatar = request.files.get('avatar')
            roleValue = request.form.get('vaiTro')

            try:
                if not roleValue:
                    raise ValueError("Vai trò không được để trống!")
                role = VaiTro(int(roleValue))
                if matKhau.strip().__eq__(xacNhanMK.strip()):
                    utils.addUser(ho,ten,ngaySinh, soDienThoai, email, taiKhoan, matKhau, avatar, role)
                    return redirect(url_for('admin.index'))
                else:
                    err_msg = "MAT KHAU KHONG KHOP!!!"
            except Exception as ex:
                import traceback
                err_msg = "Đã xảy ra lỗi: " + str(ex)
                # In traceback chi tiết ra console
                traceback.print_exc()
        return self.render('admin/create_employee.html',VaiTro = VaiTro,err_msg = err_msg)

class UserView(ModelView):
    column_list = ('id', 'ho', 'ten', 'ngaySinh','role')


admin.add_view(UserView(NguoiDung, db.session))
admin.add_view(CreateStaffView(name='Tạo nhân viên', endpoint='create_employee'))

# @app.before_request
# def before_request():
#     if request.endpoint.startswith('admin.') and not current_user.is_authenticated:
#         return redirect(url_for('login', next=request.url))





