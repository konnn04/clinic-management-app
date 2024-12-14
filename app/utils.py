from app.models import NguoiDung,VaiTro
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, dao
from datetime import datetime
from collections import defaultdict


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
            "name": "Trang chủ",
            "icon": "fa-sharp-duotone fa-solid fa-grid-horizontal ",
            "url_for": "nurse",
        },
        {
            "name": "Danh sách đăng ký",
            "icon": "fa-sharp-duotone fa-solid fa-calendar",
            "url_for": "nurse",
        },{
            "name": "Danh sách lịch khám",
            "icon": "fa-sharp-duotone fa-solid fa-calendar",
            "url_for": "nurse",
        }],
    }
    return func.get(role, [])


def revenueStats():
    '''
    Dữ liệu trả về có dạng dictionary
    [
        { "01: 123000},
        { "02: 122000},
        ...
    ]
    :return:
    '''
    bills = dao.load_revenue()
    monthly_revenue = defaultdict(float)  # Sử dụng defaultdict để gán giá trị mặc định là 0.0

    for bill in bills:
        ngay_hoa_don = bill['ngayLapHoaDon']
        tong_tien = bill['tongTien']

        # Chuyển đổi ngày sang định dạng datetime
        date_obj = datetime.strptime(ngay_hoa_don, "%Y-%m-%d")
        month_key = date_obj.strftime("%m")  # Lấy định dạng tháng-năm (e.g., "2024-01")

        # Cộng tổng tiền vào tháng tương ứng
        monthly_revenue[month_key] += tong_tien

    # Chuyển đổi kết quả thành dictionary thường (tùy chọn)
    sorted_revenue = dict(sorted(monthly_revenue.items()))
    return sorted_revenue


def revenueStatsDetail(month = 1):
    '''
    Trả về một list các dictionary tính số bệnh nhân trong ngày, doanh thu
    [
        { "2024-02-01" : { "soBenhNhan" : 2, "doanhThu" : 20000000},
        ....
    ]
    :param month:
    :return:
    '''
    data = dao.load_revenue()
    filtered_data = [
        entry for entry in data
        if datetime.strptime(entry['ngayKham'], '%Y-%m-%d').month == month
    ]

    setDay = set()
    stats = []
    for d in filtered_data:
        setDay.add(d['ngayKham'])

    for s in setDay:
        d = dict()
        curr_day = [c for c in filtered_data if c['ngayKham'].__eq__(s)]
        d[s] = {
            "soBenhNhan" : len(curr_day),
            "doanhThu" : sum([entry["tongTien"] for entry in curr_day])
        }
        stats.append(d)
    return stats