from . import app, admin, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import NguoiDung, VaiTro, Thuoc, LoHang, DanhMucThuoc
from flask_admin import BaseView,expose
from app import utils
from flask_admin.model.template import EndpointLinkRowAction
from flask_login import current_user, login_required, logout_user
from flask import redirect, url_for, request,render_template,flash


admin = Admin(app, name='Admin',template_mode='bootstrap4')

class MyModelView(ModelView):
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    details_template = 'admin/details.html'

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
            # avatar = request.files.get('avatar',"")
            roleValue = request.form.get('vaiTro')

            try:
                if not roleValue:
                    raise ValueError("Vai trò không được để trống!")
                role = VaiTro(int(roleValue))
                if matKhau.strip().__eq__(xacNhanMK.strip()):
                    utils.addUser(ho,ten,ngaySinh, soDienThoai, email, taiKhoan, matKhau, "", role)
                    return redirect(url_for('admin.index'))
                else:
                    err_msg = "MAT KHAU KHONG KHOP!!!"
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

admin.add_view(UserView(NguoiDung, db.session,name = "Danh sách người dùng"))
admin.add_view(CreateStaffView(name='Tạo nhân viên', endpoint='create_employee'))

# Quản lý thuốc
admin.add_view(MedicineView(Thuoc,db.session,name="Quản lý thuốc"))
admin.add_view(ConsignmentView(LoHang,db.session,name = "Lô hàng"))
admin.add_view(MedicineCategoryView(DanhMucThuoc,db.session, name = 'Danh mục thuốc'))






