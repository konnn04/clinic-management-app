from app.models import NguoiDung,VaiTro
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

def check_account(username,password):
    user = NguoiDung.query.filter_by(taiKhoan=username).first()
    if user and check_password_hash(user.matKhau, password):
        print("OK")
        return user
    else:
        print("BUG")
        return None


def addUser(ho,ten,ngaySinh,soDienThoai,email,taiKhoan,matKhau,avatar,role = VaiTro.BENH_NHAN):
    matKhau = generate_password_hash(matKhau)
    user = NguoiDung(ho = ho.strip(),
                     ten = ten.strip(),
                     ngaySinh = datetime.strptime(ngaySinh, "%Y-%m-%d"),
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

def get_nav(current_user):
    if not current_user.is_authenticated:
        return []
    role = current_user.role
    func = {
        VaiTro.BAC_SI:[{
            "name": "Dashboard",
            "icon": "fa-sharp-duotone fa-solid fa-grid-horizontal ",
            "url_for": "doctor",
        },
        {
            "name": "Patients",
            "icon": "fa-sharp-duotone fa-solid fa-calendar",
            "url_for": "patients_doctor",
        }],
        VaiTro.THU_NGAN:[{
            "name": "Dashboard",
            "icon": "fa-sharp-duotone fa-solid fa-grid-horizontal ",
            "url_for": "cashier",
        }],
        VaiTro.Y_TA:[{
            "name": "Dashboard",
            "icon": "fa-sharp-duotone fa-solid fa-grid-horizontal ",
            "url_for": "nurse",
        }],
    }
    return func.get(role, [])
