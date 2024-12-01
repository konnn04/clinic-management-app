from app.models import NguoiDung,VaiTro
from werkzeug.security import generate_password_hash, check_password_hash


def check_account(username,password,role = VaiTro.BENH_NHAN):
    user = NguoiDung.query.filter_by(taiKhoan=username, role=role).first()
    if user and user.matKhau.__eq__(password):
        return user
    else:
        return None
