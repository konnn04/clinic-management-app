from app.models import NguoiDung,VaiTro, NguoiBenh, PhieuLichDat
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, dao
from datetime import datetime
from collections import defaultdict
from sqlalchemy import text

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
            "name": "Trang chủ",
            "icon": "fa-sharp-duotone fa-solid fa-grid-horizontal ",
            "url_for": "cashier",
        },
        {
            "name": "Danh sách hoá đơn",
            "icon": "fa-sharp-duotone fa-solid fa-calendar",
            "url_for": "invoices",
        },
        ],
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
            "url_for": "schedule_list",
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


def get_diseases(q=None, exists = "", limit = 5):
    '''
    Trả về danh sách các bệnh dựa trên từ khóa tìm kiếm
    :param q: từ khóa tìm kiếm
    :return:
    '''
    diseases = ["Sốt", "Ho", "Đau đầu", "Viêm họng", "Viêm phổi", "Tiểu đường", "Cao huyết áp", "Đau dạ dày", "Viêm gan", "Suy thận", "Thiếu máu", "Viêm khớp", "Loãng xương", "Hen suyễn", "Viêm xoang", "Đau tim", "Đột quỵ", "Ung thư", "Rối loạn tiêu hóa", "Nhiễm trùng đường tiểu", "Viêm da", "Mất ngủ", "Trầm cảm", "Lo âu", "Rối loạn tiền đình", "Viêm tai giữa", "Viêm màng não", "Suy giảm trí nhớ", "Viêm phế quản", "Viêm ruột thừa", "Viêm tụy", "Viêm bàng quang", "Viêm tuyến tiền liệt", "Viêm phổi tắc nghẽn mãn tính", "Viêm gan B", "Viêm gan C", "Viêm gan A", "Viêm gan D", "Viêm gan E", "Viêm gan G", "Viêm gan F", "Viêm gan H", "Viêm gan I", "Viêm gan J", "Viêm gan K", "Viêm gan L", "Viêm gan M", "Viêm gan N", "Viêm gan O", "Viêm gan P", "Viêm gan Q", "Viêm gan R", "Viêm gan S", "Viêm gan T", "Viêm gan U", "Viêm gan V", "Viêm gan W", "Viêm gan X", "Viêm gan Y", "Viêm gan Z"]

    # Tìm kiếm theo từ khóa
    if q:
        diseases = [d for d in diseases if q.lower() in d.lower() and d.lower() not in exists.lower()][0:limit]
    else:
        diseases = diseases[0:limit]
    return diseases

def get_patients(draw, length, start, search_value, sort_column_index, sort_direction):
    columns = ['id', 'hoTen','gioiTinh', 'ngaySinh', 'soDienThoai', 'lanCuoiGhe']
    sort_column_name = columns[sort_column_index]
    patients = NguoiBenh.query
    if search_value:
        patients = patients.filter(NguoiBenh.hoTen.like(f"%{search_value}%"))
    total = patients.count()
    # sort_direction: 'asc' or 'desc'
    # sort_column_name: Tên cột cần sắp xếp
    patients = patients.order_by(text(f"{sort_column_name} {sort_direction}")).offset(start).limit(length).all()
    patient_list = [{
        'id': patient.id,
        'hoTen': patient.hoTen,  
        'gioiTinh': "Nam" if patient.gioiTinh else "Nữ",
        'ngaySinh': patient.ngaySinh.strftime('%Y-%m-%d'),
        'soDienThoai': patient.soDienThoai,
        'lanCuoiGhe': patient.lanCuoiGhe().strftime('%Y-%m-%d') if patient.lanCuoiGhe() is not None else ""
    } for patient in patients]
    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': patient_list
    }

