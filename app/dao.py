import json
import os
from app import app, db
from app.models import HoaDonThanhToan, NguoiBenh, PhieuLichDat, PhieuKhamBenh, NguoiDung, VaiTro, Thuoc, LoHang, LoaiDichVu, PhieuDichVu, DonThuoc, QuyDinh, TrangThaiLichDat, CaHen
from sqlalchemy import text
from sqlalchemy.orm import joinedload, subqueryload
from flask import jsonify, session
from datetime import datetime
import random
from werkzeug.security import check_password_hash, generate_password_hash
from app.momo_payment import utils as momo_utils
from flask_login import current_user

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
        PhieuKhamBenh.id == order_id,
        PhieuKhamBenh.active == True
    ).first()
    if phieukham is None:
        return None

    p = phieukham.to_dict()
    m = db.session.query(Thuoc, DonThuoc).join(DonThuoc, Thuoc.id == DonThuoc.thuoc_id).filter(DonThuoc.phieu_id == order_id).all()
    p['medicines'] = [{
        'id': thuoc.id,
        'ten': thuoc.ten,
        'soLuong': donthuoc.soLuong,
        'cachDung': donthuoc.cachDung,
        'donVi': thuoc.donVi,
        'thanhTien': donthuoc.thanhTien,
        'donGia': donthuoc.donGia
    } for thuoc, donthuoc in m]
    print(p)
    return p

def update_profile(data):
    try:
        user = NguoiDung.query.get(current_user.id)
        user.ho = data.get('ho')
        user.ten = data.get('ten')
        user.ngaySinh = datetime.strptime(data.get('ngaySinh'), "%Y-%m-%d")
        user.soDienThoai = data.get('soDienThoai')
        user.avatar = data.get('avatar')    
        db.session.commit()
        return {
            "status": "success",
            "message": "Cập nhật thông tin thành công"
        }
    except:
        return {
            "status": "error",
            "message": "Cập nhật thông tin thất bại"
        }
        

def get_appointment_history(user_id):
    # Chỉ truy vấn các cột cần thiết để giảm áp lực cho db
    phieukhams = PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhan_id == user_id and PhieuKhamBenh.active == True)\
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
    
    query = query.filter(HoaDonThanhToan.active == True)

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

    query = query.filter(db.func.date(PhieuLichDat.ngayHen) == date, PhieuLichDat.trangThai == status, PhieuLichDat.active == True)
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
        'caHen': schedule.caHen.value[1]
    } for schedule in schedules]
    
    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': schedule_list
    }

def get_patients(draw, length, start, search_value, sort_column, sort_direction):
    patients = db.session.query(
        NguoiBenh.id.label('id'),
        NguoiBenh.ho,
        NguoiBenh.ten,
        NguoiBenh.gioiTinh,
        NguoiBenh.ngaySinh,
        NguoiBenh.soDienThoai,
        db.func.coalesce(db.func.max(PhieuKhamBenh.ngayKham), datetime(1970, 1, 1)).label('lanCuoiGhe')
    ).join(PhieuKhamBenh, PhieuKhamBenh.benhNhan_id == NguoiBenh.id, isouter=True).group_by(
        NguoiBenh.id.label('id'),
        NguoiBenh.ho,
        NguoiBenh.ten,
        NguoiBenh.gioiTinh,
        NguoiBenh.ngaySinh,
        NguoiBenh.soDienThoai
    )

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

    patients = patients.order_by(text(f"{sort_column} {sort_direction}"))
    
    patients = patients.offset(start).limit(length).all()

    patient_list = [{
        'id': patient.id,
        'ho': patient.ho,
        'ten': patient.ten,
        'gioiTinh': "Nam" if patient.gioiTinh else "Nữ",
        'ngaySinh': patient.ngaySinh.strftime('%Y-%m-%d'),
        'soDienThoai': patient.soDienThoai,
        'lanCuoiGhe': patient.lanCuoiGhe if patient.lanCuoiGhe else None
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
    ).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id).join(NguoiBenh, PhieuKhamBenh.benhNhan_id == NguoiBenh.id).filter(PhieuKhamBenh.active == True)

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
    ).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id).join(NguoiBenh, PhieuKhamBenh.benhNhan_id == NguoiBenh.id).filter(PhieuKhamBenh.active == True)

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
    schedule.trangThai = TrangThaiLichDat.CHUA_DUYET
    db.session.commit()
    return True

def accept_schedule(id):
    schedule = PhieuLichDat.query.get(id)
    if schedule is None:
        return False
    schedule.trangThai = TrangThaiLichDat.DA_DUYET
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
    ).join(NguoiBenh, PhieuLichDat.benhNhan_id == NguoiBenh.id).filter(PhieuLichDat.trangThai == TrangThaiLichDat.DA_DUYET, db.func.date(PhieuLichDat.ngayHen) == datetime.now().date(), PhieuLichDat.active == True)

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
    

def add_appointments(cur_id, ngayHen, gioKham ):
    o = PhieuLichDat.query.filter_by(benhNhan_id = cur_id, ngayHen = datetime.strptime(ngayHen, "%Y-%m-%d"), active = True).first()
    if o:
        return {
            "status": "error",
            "message": "Đã có lịch hẹn trùng với ngày và ca hẹn đã chọn"
        }
    
    # Đếm số phiếu có trong ngày, biết ngày hẹn là datetime
    q = PhieuLichDat.query.filter_by(ngayHen = datetime.strptime(ngayHen, "%Y-%m-%d"), active = True).count()
    print(q)
    print(datetime.strptime(ngayHen, "%Y-%m-%d"))
    if q >= int(QuyDinh.query.filter_by(key="MAX_APPOINTMENT").first().value):
        return {
            "status": "error",
            "message": "Đã đủ số lượng lịch hẹn trong ngày"
        }

    p = PhieuLichDat(benhNhan_id = cur_id,
                     ngayHen = datetime.strptime(ngayHen, "%Y-%m-%d"),
                     trangThai = TrangThaiLichDat.CHUA_DUYET,
                     caHen = CaHen.SANG if gioKham == "SANG" else CaHen.CHIEU if gioKham == "CHIEU" else CaHen.TOI)
    db.session.add(p)
    db.session.commit()

    return {
        "status": "success",
        "message": "Đã thêm lịch hẹn"
    }

def get_benh_nhan(id):
    return NguoiBenh.query.get(id)

def check_user(info):
    return NguoiBenh.query.filter_by(soDienThoai=info).first() or NguoiBenh.query.filter_by(email=info).first()
    # q sẽ trả về None khi không tồn tại nên không cần
    # if q_email or q_phone:# Nếu đã tồn tại email hay số điện thoại
    #     return q_email if q_email else q_phone
    # else:
    #     return None

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

def addUser(ho,ten,ngaySinh,gioiTinh,soDienThoai,email,taiKhoan,matKhau,avatar,role = VaiTro.BAC_SI,ghiChu = ""):
    matKhau = generate_password_hash(matKhau)
    user = NguoiDung(ho = ho.strip(),
                     ten = ten.strip(),
                     ngaySinh = datetime.strptime(ngaySinh, "%Y-%m-%d"),
                     gioiTinh = gioiTinh,
                     soDienThoai = soDienThoai.strip(),
                     email = email.strip(),
                     taiKhoan = taiKhoan.strip(),
                     matKhau = matKhau,
                     avatar = avatar,
                     role = role,
                     ghiChu = ghiChu
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

    query = query.filter(Thuoc.ten.like(f"%{q}%" if q else "%"), LoHang.soLuong > 0, Thuoc.active == True)
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

def get_services(q, exists):
    query = db.session.query(
        LoaiDichVu.id.label('id'),
        LoaiDichVu.tenDichVu.label('ten_dich_vu'),
        LoaiDichVu.giaDichVu.label('gia_dich_vu'),
    )

    query = query.filter(LoaiDichVu.tenDichVu.like(f"%{q}%" if q else "%"), LoaiDichVu.active == True)

    for e in exists.split(","):
        query = query.filter(LoaiDichVu.id != e.strip())

    query = query.all()
    return [{
        'id': e.id,
        'ten_dich_vu': e.ten_dich_vu,
        'gia_dich_vu': e.gia_dich_vu
    } for e in query]

def create_invoice(phieuKham):
    dichVuKham = PhieuDichVu.query.filter(PhieuDichVu.phieukham_id == phieuKham.id).all()
    tienDichVu = sum([dv.giaDichVu for dv in dichVuKham]) + QuyDinh.query.filter_by(key="EXAMINATION_COST").first().value
    donThuoc = DonThuoc.query.filter(DonThuoc.phieu_id == phieuKham.id).all()
    tienThuoc = 0
    tienKham = QuyDinh.query.filter_by(key="EXAMINATION_COST").first().value
    for thuoc in donThuoc:
        tienThuoc += DonThuoc.query.get(thuoc.id).thanhTien
    hoaDon = HoaDonThanhToan(
        benhNhan_id = phieuKham.benhNhan_id,
        tienKham = tienKham,
        tienThuoc = tienThuoc,
        phieuKham_id = phieuKham.id,
        tongTien = tienDichVu + tienThuoc,
        )
    db.session.add(hoaDon)
    db.session.commit()

def save_patient(data):
    examination = PhieuLichDat.query.get(data.get('examination_id'))
    if examination is None:
        return {
            "status": "error",
            "message": "Không tìm thấy phiếu khám"
        }
    
    patient = NguoiBenh.query.get(examination.benhNhan_id)
    if patient is None:
        return {
            "status": "error",
            "message": "Không tìm thấy bệnh nhân"
        }
    
    trieuChung = "Không có triệu chứng"
    duDoanLoaiBenh = "Không có dự đoán loại bệnh"
    if data.get('diseases'):
        duDoanLoaiBenh = ", ".join(data.get('diseases'))

    services = data.get('services')
    medicines = data.get('medicines')

    bacSi = current_user.id        
    ghiChu = data.get('ghiChu')

    # Kiểm tra thuốc
    medicines = data.get('medicines')
    if medicines:
        for medicine in medicines:
            thuoc = Thuoc.query.get(medicine.get('medicine'))
            if thuoc is None:
                return {
                    "status": "error",
                    "message": "Không tìm thấy thuốc"
                }
            
            soLuongThuoc = LoHang.query.filter(LoHang.thuoc_id == thuoc.id).with_entities(db.func.sum(LoHang.soLuong)).scalar()
            if soLuongThuoc < int(medicine.get('value')):
                return {
                    "status": "error",
                    "message": "Số lượng thuốc không đủ"
                }

    if services:
        for service in services:
            loaiDichVu = LoaiDichVu.query.get(int(service))
            if loaiDichVu is None:
                return {
                    "status": "error",
                    "message": "Không tìm thấy dịch vụ"
                }

            pk = PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhan_id == examination.benhNhan_id).order_by(PhieuKhamBenh.ngayKham.desc()).first()

            p = PhieuDichVu(
                phieukham_id = pk.id,
                dichVu_id = loaiDichVu.id,
                giaDichVu = loaiDichVu.giaDichVu
            )
            db.session.add(p)
            db.session.commit()

    phieuKham = PhieuKhamBenh(
        benhNhan_id = patient.id,
        bacSi_id = bacSi,
        trieuChung = trieuChung,
        duDoanLoaiBenh = duDoanLoaiBenh,
        ghiChu = ghiChu
    )

    db.session.add(phieuKham)
    db.session.commit()

    phieuKham = PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhan_id == patient.id).order_by(PhieuKhamBenh.ngayKham.desc()).first()
    for medicine in medicines:
        cachDung = ""

        uongKhi = {
            "before": "Uống rước khi ăn",
            "after": "Uống sau khi ăn",
            "none": "Trước hoặc sau khi ăn",
        }.get(medicine.get('when'))

        thuoc = Thuoc.query.get(int(medicine.get('medicine')))
        if thuoc is None:
            continue
        
        if medicine.get('method') == "stc":
            cachDung = f'Uống sáng trưa chiều, ({medicine.get("morning")}h, {medicine.get("noon")}h, {medicine.get("evening")}h), {uongKhi}, mỗi lần {medicine.get("time")} {medicine.get("unit")}, cách nhau {medicine.get("day")} ngày'
        else:
            cachDung = f'Uống mỗi {medicine.get("hourly")} giờ, {uongKhi}, mỗi lần {medicine.get("time")} {medicine.get("unit")}, cách nhau {medicine.get("day")} ngày'
        p = DonThuoc(
            phieu_id = phieuKham.id,
            thuoc_id = medicine.get('medicine'),
            soLuong = medicine.get('value'),
            cachDung = cachDung,
            donGia = thuoc.gia,
            thanhTien = thuoc.gia * int(medicine.get('value'))
        )
        db.session.add(p)

        db.session.commit()

    create_invoice(phieuKham)
    PhieuLichDat.query.filter(PhieuLichDat.benhNhan_id == patient.id, PhieuLichDat.active == True).update({PhieuLichDat.trangThai: TrangThaiLichDat.DA_GIAI_QUYET})

    return {
        "status": "success",
        "message": "Đã lưu thông tin bệnh nhân",
    }
    

def init_varaibles():
    quydinh = {
        "MAX_PAGE": 10,
        "MAX_APPOINTMENT": 40,
        "EXAMINATION_COST": 100000,
    }

    for key in quydinh:
        q = QuyDinh.query.filter_by(key=key).first()
        if not q:
            q = QuyDinh(key=key, value=quydinh[key])
        db.session.add(q)
    db.session.commit()

def get_appointment_list(id):
    # print(id)
    try:
        phieulichdat = PhieuLichDat.query.filter(PhieuLichDat.benhNhan_id == int(id), PhieuLichDat.active == True, PhieuLichDat.ngayHen >= datetime.now().date()).all()
        
        return [{
            'id': e.id,
            'ngayHen': e.ngayHen.strftime('%Y-%m-%d'),
            'caHen': e.caHen.value[1],
            'trangThai': e.trangThai.value[1],
            'coTheHuy': True if e.trangThai == TrangThaiLichDat.CHUA_DUYET else False
        } for e in phieulichdat]
    except:
        return []
    
def cancel_appointment(lichKham_id):
    try:
        print(session['current_user'].get("id"))
        phieulichdat = PhieuLichDat.query.get(int(lichKham_id))
        if phieulichdat is None:
            return {'status': 'error', 'message': 'Không tìm thấy lịch khám'}
        if phieulichdat.benhNhan_id != session['current_user'].get("id"):
            return {'status': 'error', 'message': 'Không tìm thấy lịch khám'}
        if phieulichdat.trangThai != TrangThaiLichDat.CHUA_DUYET:
            return {'status': 'error', 'message': 'Lịch khám đã được duyệt hoặc hủy'}
        if phieulichdat.ngayHen.date() < datetime.now().date():
            return {'status': 'error', 'message': 'Không thể hủy lịch khám đã qua'}
        phieulichdat.active = False
        db.session.commit()
        return {'status': 'success', 'message': 'Hủy lịch khám thành công'}
    except:
        return {'status': 'error', 'message': 'Hủy lịch kham thất bại'}
        
def medicine_stats_details(month):
    year = datetime.now().year
    lo_hang_subquery = (
        db.session.query(
            LoHang.thuoc_id,
            db.func.sum(
                db.case(
                    (
                        db.or_(
                            db.extract('year', LoHang.hanSuDung) > year,
                            db.and_(
                                db.extract('year', LoHang.hanSuDung) == year,
                                db.extract('month', LoHang.hanSuDung) >= month
                            )
                        ),
                        LoHang.soLuong
                    ),
                    else_=0
                )
            ).label('tong_so_luong')
        )
        .group_by(LoHang.thuoc_id)  # Nhóm theo thuốc
        .subquery()  # Truy vấn con
    )

    query = (
        db.session.query(
            Thuoc.ten,
            Thuoc.donVi,
            db.func.sum(DonThuoc.soLuong).label('so_luong'),
            lo_hang_subquery.c.tong_so_luong.label('tong')
        )
        .join(DonThuoc, Thuoc.id == DonThuoc.thuoc_id)
        .join(PhieuKhamBenh, PhieuKhamBenh.id == DonThuoc.phieu_id)
        .outerjoin(lo_hang_subquery, Thuoc.id == lo_hang_subquery.c.thuoc_id)  # Kết hợp với subquery
        .filter(
            db.extract('month', PhieuKhamBenh.ngayKham) == month,
            db.extract('year', PhieuKhamBenh.ngayKham) == year
        )
        .group_by(Thuoc.id, Thuoc.donVi, lo_hang_subquery.c.tong_so_luong)  # Nhóm theo thuốc và kết quả subquery
    )
    return query.all()

def revenue_stats_details(month):
    # Tổng doanh thu của tháng chỉ định
    total_revenue_month = (
        db.session.query(db.func.sum(HoaDonThanhToan.tongTien))
        .filter(
            db.extract('month', HoaDonThanhToan.ngayLapHoaDon) == month
        )
        .scalar()  # Lấy giá trị đơn
    )

    daily_stats = (
        db.session.query(
            db.func.date(HoaDonThanhToan.ngayLapHoaDon).label('day'),  # Ngày
            db.func.count(HoaDonThanhToan.id).label('patient_count'),  # Số lượng hóa đơn
            db.func.sum(HoaDonThanhToan.tongTien).label('daily_revenue'),  # Doanh thu trong ngày
            db.func.round((db.func.sum(HoaDonThanhToan.tongTien) / total_revenue_month), 3).label('daily_ratio')
        )
        .filter(
            HoaDonThanhToan.trangThai == 1,
            db.extract('month', HoaDonThanhToan.ngayLapHoaDon) == month
        )
        .group_by(db.func.date(HoaDonThanhToan.ngayLapHoaDon))  # Nhóm theo ngày
        .order_by(db.func.date(HoaDonThanhToan.ngayLapHoaDon))  # Sắp xếp theo ngày
        .all()
    )

    # Thống kê theo từng ngày

    return daily_stats, total_revenue_month