from app.models import NguoiDung,VaiTro
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


def check_account(username,password,role = VaiTro.BENH_NHAN):
    user = NguoiDung.query.filter_by(taiKhoan=username, role=role).first()
    if user and user.matKhau.__eq__(password):
        return user
    else:
        return None


def addUser(ho,ten,ngaySinh,soDienThoai,email,taiKhoan,matKhau,avatar,role = VaiTro.BENH_NHAN):
    matKhau = generate_password_hash(matKhau,method='pbkdf2:sha512')
    user = NguoiDung(ho = ho.strip(),
                     ten = ten.strip(),
                     ngaySinh = ngaySinh,
                     soDienThoai = soDienThoai.strip(),
                     email = email.strip(),
                     taiKhoan = taiKhoan.strip(),
                     matKhau = matKhau,
                     avatar = avatar,
                     role = role
                     )
    print(user)
    db.session.add(user)
    db.session.commit()


