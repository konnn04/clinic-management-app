from . import app, admin, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import NguoiDung, VaiTro, Thuoc, LoHang, DanhMucThuoc
from flask_admin import BaseView,expose, AdminIndexView
from app import utils
from flask_admin.model.template import EndpointLinkRowAction
from flask_login import current_user, login_required, logout_user
from flask import redirect, url_for, request,render_template,flash,send_file
from datetime import datetime
import cloudinary.uploader
import pandas as pd
import os

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == VaiTro.ADMIN
    
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    details_template = 'admin/details.html'
    profile_template = 'admin/profile.html'

class MyBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == VaiTro.ADMIN



class CreateStaffView(MyBaseView):
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
            avatar = request.files.get('avatar',"")
            roleValue = request.form.get('vaiTro')

            try:
                if not roleValue:
                    raise ValueError("Vai trò không được để trống!")
                role = VaiTro(int(roleValue))
                if matKhau.strip().__eq__(xacNhanMK.strip()):
                    if avatar:
                        avatar = cloudinary.uploader.upload(avatar)
                    else:
                        avatar = ""
                    utils.addUser(ho=ho, ten=ten, ngaySinh=ngaySinh, soDienThoai=soDienThoai, email=email, taiKhoan=taiKhoan, matKhau=matKhau, role=role, avatar=avatar)
                    return redirect(url_for('admin.index'))
                else:
                    err_msg = "Password not match"
            except Exception as ex:
                import traceback
                err_msg = "Đã xảy ra lỗi: " + str(ex)
                # In traceback chi tiết ra console
                traceback.print_exc()
        return self.render('admin/create_employee.html',VaiTro = VaiTro,err_msg = err_msg)

class UserView(MyModelView):
    can_create = False
    column_list = ('id', 'ho', 'ten', 'ngaySinh','role')
    column_labels = {
        'id': 'ID',
        'ho': 'Họ',
        'ten': 'Tên',
        'ngaySinh': 'Ngày sinh',
        'role': 'Vai trò',
        'soDienThoai' : 'Số điện thoại',
        'ghiChu' : 'Ghi chú',
        'taiKhoan' : 'Tài khoản',
        'matKhau' : 'Mật khẩu'
    }
    form_labels = {
        'ho': 'Họ của người dùng',
        'ten': 'Tên của người dùng',
        'ngaySinh': 'Ngày sinh',
        'role': 'Quyền truy cập'
    }


# Quản lý thuốc
class ConsignmentView(MyModelView):
    column_list = ['id','ngayNhap','hanSuDung','ngaySanXuat','thuoc']
    column_labels = {
        'id': 'ID',
        'ngayNhap' : 'Ngày nhập',
        'hanSuDung' : 'Hạn sử dụng',
        'ngaySanXuat' : 'Ngày sản xuất',
        'thuoc' : 'Thuốc'
    }
    form_columns = ['ngayNhap', 'hanSuDung', 'ngaySanXuat', 'thuoc']

class MedicineView(MyModelView):
    column_list = ['id','ten','nhaCungCap','xuatXu','donVi','danhMucThuoc_id','loHang_id']
    column_labels = {
        'id': 'ID',
        'ten': 'Tên',
        'nhaCungCap': 'Nhà cung cấp',
        'xuatXu': 'Xuất xứ',
        'donVi' : 'Đơn vị',
        'danhMucThuoc_id': 'Mã danh mục',
        'loHang_id' : 'Lô hàng'
    }
    form_columns = ['ten', 'nhaCungCap', 'xuatXu', 'donVi', 'danhMucThuoc_id', 'loHang_id']

class MedicineCategoryView(MyModelView):
    column_list = ['id', 'ten']
    column_labels = {
        'id': 'ID',
        'ten': 'Tên',
        'thuoc' : 'Thuốc'
    }

class RevenueStats(MyBaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self, *args, **kwargs):
        revenue_data = utils.revenueStats()
        month = request.args.get('month', default=1, type=int)
        print(month)
        stats = utils.revenueStatsDetail(month = month)
        print(revenue_data)
        values = list(revenue_data.values()) # Danh sách tổng doanh thu tương ứng
        print(values)
        return self.render('admin/revenue_stats.html', data = values,stats = stats,month = month)

    @expose('/print-reports', methods=['POST'])
    def print_report(self):
        month = request.form.get('month', default=1, type=int)
        stats = utils.revenueStatsDetail(month=month)

        data = []
        for s in stats:
            date = list(s.keys())[0]
            data.append([date, s[date]['soBenhNhan'], s[date]['doanhThu']])

        df = pd.DataFrame(data, columns=['Ngày', 'Số bệnh nhân', 'Doanh thu'])
        file_name = os.path.join(app.root_path, f'static/temp/bao_cao_thang_{month}.xlsx')
        df.to_excel(file_name, index=True)  
        return send_file(file_name, as_attachment=True)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or current_user.role != VaiTro.ADMIN:
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()
    
admin = Admin(
    app, 
    name='Admin', 
    template_mode='bootstrap4', 
    index_view=MyAdminIndexView(
        name="Trang chủ", 
        menu_icon_type='fa', 
        menu_icon_value='fa-solid fa-home me-3'
        )
    )

admin.add_view(UserView(
    NguoiDung, 
    db.session, 
    name='Danh sách người dùng', 
    menu_icon_type='fa', 
    menu_icon_value='fa-solid fa-users me-3'
    ))
admin.add_view(CreateStaffView(
    name='Tạo nhân viên', 
    endpoint='create_employee', 
    menu_icon_type='fa', 
    menu_icon_value='fa-solid fa-user-plus me-3'
))

# Quản lý thuốc
admin.add_view(MedicineView(
    Thuoc, 
    db.session, 
    name="Quản lý thuốc", 
    menu_icon_type='fa', 
    menu_icon_value='fa-solid fa-pills me-3'
))
admin.add_view(ConsignmentView(
    LoHang, 
    db.session, 
    name="Lô hàng", 
    menu_icon_type='fa', 
    menu_icon_value='fa-solid fa-boxes me-3'
))
admin.add_view(MedicineCategoryView(
    DanhMucThuoc, 
    db.session, 
    name='Danh mục thuốc', 
    menu_icon_type='fa', 
    menu_icon_value='fa-solid fa-th-list me-3'
))

admin.add_view(RevenueStats(
    name='Thống kê doanh thu',
    endpoint='revenue_stats',
    menu_icon_type='fa',
    menu_icon_value='fa-solid fa-chart-line me-3'
))






