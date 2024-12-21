import json
import os
from app import app, db
from app.models import HoaDonThanhToan, NguoiBenh, PhieuLichDat, PhieuKhamBenh, NguoiDung, VaiTro, Thuoc, LoHang
from sqlalchemy import text
from sqlalchemy.orm import joinedload, subqueryload
from flask import jsonify
from datetime import datetime
import random
from werkzeug.security import check_password_hash, generate_password_hash
from app.momo_payment import utils as momo_utils

# Test function
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_revenue():
    return read_json(os.path.join(app.root_path, "data/revenue.json"))

# Tra cứu thông tin bệnh nhân
def get_appointment_history_detail(user_id, order_id):
    phieukham = PhieuKhamBenh.query.filter(
        PhieuKhamBenh.benhNhan_id == user_id,
        PhieuKhamBenh.id == order_id
    ).first()
    print(phieukham.to_dict())
    return phieukham.to_dict()


def get_appointment_history(user_id):
    # Chỉ truy vấn các cột cần thiết để giảm áp lực cho db
    phieukhams = PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhan_id == user_id) \
        .with_entities(PhieuKhamBenh.id, PhieuKhamBenh.ngayKham, HoaDonThanhToan) \
        .join(HoaDonThanhToan, HoaDonThanhToan.phieuKham_id == PhieuKhamBenh.id, isouter=True) \
        .all()

    data = [
        {
            'id': pk[0],
            'ngayHen': pk[1] if pk[1] else None,
            'hoaDonThanhToan': pk[2].to_dict() if pk[2] else None
        }
        for pk in phieukhams
    ]

    return data


def load_invoices(draw, length, start, search, sort, order):
    query = db.session.query(
        HoaDonThanhToan.id.label('id'),
        HoaDonThanhToan.ngayLapHoaDon,
        NguoiBenh.ho.label('hoBenhNhan'),
        NguoiBenh.ten.label('tenBenhNhan'),
        NguoiDung.ho.label('hoBacSi'),
        NguoiDung.ten.label('tenBacSi'),
        HoaDonThanhToan.tongTien,
        HoaDonThanhToan.trangThai,
        PhieuKhamBenh.id.label('phieuKham_id')
    ).join(NguoiBenh, HoaDonThanhToan.benhNhan_id == NguoiBenh.id).join(PhieuKhamBenh, HoaDonThanhToan.phieuKham_id == PhieuKhamBenh.id, isouter=True).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id)

    if search:
        query = query.filter(
            db.or_(
            (NguoiBenh.ho + " " + NguoiBenh.ten).like(f"%{search}%"),
            (NguoiDung.ho + " " + NguoiDung.ten).like(f"%{search}%")
            )
        )

    total = query.count()
    query = query.order_by(text(f"{sort} {order}"))
    invoices = query.offset(start).limit(length).all()

    invoice_list = [{
        'id': HoaDonThanhToan.query.get(invoice.id).hashed_id,
        # 'hashed_id': HoaDonThanhToan.query.get(invoice.id).hashed_id,
        'ngayLapHoaDon': invoice.ngayLapHoaDon.strftime('%Y-%m-%d'),
        'hoBenhNhan': invoice.hoBenhNhan,
        'tenBenhNhan': invoice.tenBenhNhan,
        'bacSi': f"{invoice.hoBacSi} {invoice.tenBacSi}",
        'tongTien': invoice.tongTien,
        'trangThai': invoice.trangThai,
    } for invoice in invoices]

    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': invoice_list
    }


def patient_stat():
    man_count = NguoiBenh.query.filter(NguoiBenh.gioiTinh == True).count()
    women_count = NguoiBenh.query.count() - man_count

    # Tạo dữ liệu thống kê theo ngẫu nhiên
    month_stat = []
    for month in range(1, 13):
        month_stat.append({
            'month': f'Tháng {month}',
            'total': random.randint(70, 100)
        })

    disease_stat = []
    for d in ["Tiểu đường", "Huyết áp", "Tim mạch", "Đau lưng", "Đau đầu"]:
        disease_stat.append({
            'disease': d,
            'total': random.randint(50, 120)
        })

    patient_stat = {
        'man': man_count,
        'women': women_count
    }
    disease_stat.sort(key=lambda x: x['total'], reverse=True)

    return {
        'patient_stat': patient_stat,
        'month_stat': month_stat,
        'disease_stat': disease_stat
    }


def load_schedule_list(date, type, draw, length, start, search, sort_column, sort_order):
    query = PhieuLichDat.query.filter(PhieuLichDat.ngay == date, PhieuLichDat.loai == type)
    
def load_schedule_list(date,status, draw, length, start, search, sort_column, sort_order):
    query = db.session.query(
        PhieuLichDat.id.label('id'),
        PhieuLichDat.ngayHen,
        PhieuLichDat.trangThai,
        PhieuLichDat.caHen,
        NguoiBenh.id.label('benhNhan_id'),
        NguoiBenh.ho,
        NguoiBenh.ten,
        NguoiBenh.soDienThoai,
        NguoiBenh.ngaySinh,
        NguoiBenh.gioiTinh
    ).join(NguoiBenh, PhieuLichDat.benhNhan_id == NguoiBenh.id)

    query = query.filter(db.func.date(PhieuLichDat.ngayHen) == date, PhieuLichDat.trangThai == status)
    if search:
        query = query.filter(
            db.or_(
            (NguoiBenh.ho + " " + NguoiBenh.ten).like(f"%{search}%"),
            NguoiBenh.soDienThoai.like(f"%{search}%")
            )
        )
    total = query.count()
    query = query.order_by(text(f"{sort_column} {sort_order}"))
    schedules = query.offset(start).limit(length).all()
    schedule_list = [{
        'id': schedule.id,
        'benhNhan_id': schedule.benhNhan_id,
        'ho': schedule.ho,
        'ten': schedule.ten,
        'ngaySinh': schedule.ngaySinh.strftime('%Y-%m-%d'),
        'gioiTinh': 'Nam' if schedule.gioiTinh else 'Nữ',
        'caHen': {"sang": "Sáng", "chieu": "Chiều", "toi":"Tối"}[schedule.caHen],
    } for schedule in schedules]
    
    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': schedule_list
    }

def get_patients(draw, length, start, search_value, sort_column, sort_direction):
    patients = NguoiBenh.query
    if search_value:
        patients = patients.filter(
            db.or_(
            (NguoiBenh.ho + " " + NguoiBenh.ten).like(f"%{search_value}%"),
            NguoiBenh.soDienThoai.like(f"%{search_value}%")
            )
        )
    total = patients.count()
    # sort_direction: 'asc' or 'desc'
    # sort_column_name: Tên cột cần sắp xếp

    if sort_direction == 'asc':
        patients = patients.order_by(getattr(NguoiBenh, sort_column).asc())
    else:
        patients = patients.order_by(getattr(NguoiBenh, sort_column).desc())
    
    patients = patients.offset(start).limit(length).all()

    patient_list = [{
        'id': patient.id,
        'ho': patient.ho,
        'ten': patient.ten,
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

def load_examination_list(draw, length, start, search, sort_column, sort_order):
    query = db.session.query(
        PhieuKhamBenh.id.label('id'),
        PhieuKhamBenh.ngayKham,
        NguoiDung.ho.label('ho_bac_si'),
        NguoiDung.ten.label('ten_bac_si'),
        NguoiBenh.ho.label('ho_benh_nhan'),
        NguoiBenh.ten.label('ten_benh_nhan'),
        NguoiBenh.soDienThoai.label('soDienThoai'),
        NguoiBenh.ngaySinh,
        NguoiBenh.gioiTinh,
    ).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id).join(NguoiBenh, PhieuKhamBenh.benhNhan_id == NguoiBenh.id)

    if search:
        query = query.filter(
            db.or_(
            (
                NguoiBenh.ho + " " + NguoiBenh.ten).like(f"%{search}%"),
                NguoiDung.ho + " " + NguoiDung.ten).like(f"%{search}%"),
                NguoiBenh.soDienThoai.like(f"%{search}%")
            )
    total = query.count()
    query = query.order_by(text(f"{sort_column} {sort_order}"))
    examinations = query.offset(start).limit(length).all()
    examination_list = [{
        'id': examination.id,
        'ho_bac_si': examination.ho_bac_si,
        'ten_bac_si': examination.ten_bac_si,
        'ho_benh_nhan': examination.ho_benh_nhan,
        'ten_benh_nhan': examination.ten_benh_nhan,
        'ngayKham': examination.ngayKham.strftime('%Y-%m-%d'),
        'gioiTinh': 'Nam' if examination.gioiTinh else 'Nữ',
        'soDienThoai': examination.soDienThoai
    } for examination in examinations]
    
    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': examination_list
    }
    
def get_examination_list_v1(sort_column, sort_order, page_index):
    query = db.session.query(
        PhieuKhamBenh.id.label('id'),
        PhieuKhamBenh.ngayKham.label('ngay_kham'),
        NguoiDung.ho.label('ho_bac_si'),
        NguoiDung.ten.label('ten_bac_si'),
        NguoiBenh.ho.label('ho_benh_nhan'),
        NguoiBenh.ten.label('ten_benh_nhan'),
        NguoiBenh.soDienThoai.label('so_dien_thoai'),
        NguoiBenh.ngaySinh.label('ngay_sinh'),
        NguoiBenh.gioiTinh.label('gioi_tinh')
    ).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id).join(NguoiBenh, PhieuKhamBenh.benhNhan_id == NguoiBenh.id)
    total = query.count()
    if (page_index < 1):
        page_index = 1

    if (page_index > total//12 + 1):
        page_index = total//12 + 1

    query = query.order_by(text(f"{sort_column} {sort_order}"))
    examinations = query.offset((page_index-1)*12).limit(12).all()

    examination_list = [{
        'id': examination.id,
        'ho_bac_si': examination.ho_bac_si,
        'ten_bac_si': examination.ten_bac_si,
        'ho_benh_nhan': examination.ho_benh_nhan,
        'ten_benh_nhan': examination.ten_benh_nhan,
        'ngayHen': examination.ngay_kham.strftime('%Y-%m-%d'),
        'gioi_tinh': 'Nam' if examination.gioi_tinh else 'Nữ',
        'so_dien_thoai': examination.so_dien_thoai
    } for examination in examinations]

    return {
        'total': total,
        'data': examination_list,
        'page_index': page_index,
        'next': True if page_index < total//12+1 else False,
        'prev': True if page_index > 1 else False
    }


def cancel_schedule(id):
    schedule = PhieuLichDat.query.get(id)
    if schedule is None:
        return False
    schedule.trangThai = False
    db.session.commit()
    return True

def accept_schedule(id):
    schedule = PhieuLichDat.query.get(id)
    if schedule is None:
        return False
    schedule.trangThai = True
    db.session.commit()
    return True

def get_schedules_overview(q):
    query = db.session.query(
        PhieuLichDat.id.label('id'),
        PhieuLichDat.ngayHen,
        PhieuLichDat.trangThai,
        PhieuLichDat.caHen,
        NguoiBenh.id.label('benhNhan_id'),
        NguoiBenh.ho,
        NguoiBenh.ten,
        NguoiBenh.soDienThoai,
        NguoiBenh.ngaySinh,
        NguoiBenh.gioiTinh,
        PhieuLichDat.hoanThanh,
    ).join(NguoiBenh, PhieuLichDat.benhNhan_id == NguoiBenh.id).filter(PhieuLichDat.trangThai == True, PhieuLichDat.hoanThanh == False, db.func.date(PhieuLichDat.ngayHen) == datetime.now().date())

    query = query.filter(
            db.or_(
            (NguoiBenh.ho + " " + NguoiBenh.ten).like(f"%{q}%"),
            NguoiBenh.soDienThoai.like(f"%{q}%")
            )
        ).order_by(PhieuLichDat.ngayHen.desc()).limit(5).all()
    
    return [{
        'id': e.id,
        'nguoi_benh_id': e.benhNhan_id,
        'ho': e.ho,
        'ten': e.ten,
        'sdt': e.soDienThoai,
        'tuoi': datetime.now().year - e.ngaySinh.year,
        'gioi_tinh': 'Nam' if e.gioiTinh else 'Nữ',
        'nhom_mau': 'KXD'
        
    } for e in query]

def check_account(username,password):
    user = NguoiDung.query.filter_by(taiKhoan=username).first()
    if user and check_password_hash(user.matKhau, password):
        print("OK")
        return user
    else:
        print("BUG")
        return None
    

def add_appointments(ngayDat, hoTen):
    p = PhieuLichDat(hoTen = hoTen,
                     ngayDat = datetime.strptime(ngayDat, "%Y-%m-%d"),
                     trangThai = True,
                     nguoiDung_id = 1)
    db.session.add(p)
    db.session.commit()

def check_user(info):
    q_email = NguoiBenh.query.filter_by(email=info).first()
    q_phone = NguoiBenh.query.filter_by(soDienThoai=info).first()

    if q_email or q_phone:# Nếu đã tồn tại email hay số điện thoại
        return q_email if q_email else q_phone
    else:
        return None

def add_patients(ho,ten,email,soDienThoai,ngaySinh,gioiTinh,diaChi,ghiChu):
    n = NguoiBenh(ho = ho,
                  ten = ten,
                  gioiTinh = gioiTinh,
                  ngaySinh = datetime.strptime(ngaySinh, "%Y-%m-%d"),
                  soDienThoai=soDienThoai,
                  email=email,
                  diaChi = diaChi,
                  ghiChu=ghiChu)
    db.session.add(n)
    db.session.commit()

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

def get_medicine(q, exists = ""):
    query = db.session.query(
        Thuoc.id.label('id'),
        Thuoc.ten.label('ten'),
        Thuoc.donVi.label('don_vi'),
        Thuoc.gia.label('gia'),
        db.func.sum(LoHang.soLuong).label('so_luong')
    ).join(LoHang, Thuoc.id == LoHang.thuoc_id).group_by(Thuoc.id)

    query = query.filter(Thuoc.ten.like(f"%{q}%" if q else "%"))
    # query = query.filter
    for e in exists.split(","):
        query = query.filter(Thuoc.id != e)
    
    query = query.all()
    return [{
        'id': e.id,
        'ten': e.ten,
        'don_vi': e.don_vi,
        'gia': e.gia,
        'so_luong': e.so_luong
    } for e in query]

def set_payUrl(hoa_don, payUrl):
    setattr(hoa_don,'payUrl', payUrl)
    db.session.commit()

def handle_payment_result(response_dict):

    order_id = HoaDonThanhToan.decode_hashed_id(response_dict.get('orderId'))
    order = HoaDonThanhToan.query.filter_by(id=order_id).first()

    msg = ""

    # signature check

    signature = momo_utils.create_confirm_signature(hoa_don=order, response=response_dict)

    print(response_dict.get('signature'),"==========",signature)

    if not response_dict.get('signature') == signature:
        msg="Chu ky khong hop le"
    else:
        if not order:
            msg = "Khong tim thay hoa don"
        else:
            if response_dict.get('resultCode') == 0:
                setattr(order, "trangThai", True)
                db.session.commit()
                return {"status": "success", "message": "Thanh toan thanh cong"}
    return {"status": "error", "message": msg}