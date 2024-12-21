import json
import os
from app import app, db
from app.models import HoaDonThanhToan, NguoiBenh, PhieuLichDat, PhieuKhamBenh, NguoiDung
from sqlalchemy import text
from flask import jsonify
from datetime import datetime 
import random

def read_json(path):
    with open(path,"r") as f:
        return json.load(f)

def load_revenue():
    return read_json(os.path.join(app.root_path, "data/revenue.json"))

def load_invoices(draw, length, start, search, sort_column, sort_order):
    columns = ['id', 'date', 'patient', 'doctor', 'total', 'status']
    sort_column = columns[sort_column]
    query = HoaDonThanhToan.query
    if search:
        query = query.filter(HoaDonThanhToan.phieuKham.like(f"%{search}%"))
    total = query.count()
    query = query.order_by(text(f"{sort_column} {sort_order}"))
    invoices = query.offset(start).limit(length).all()
    
    invoice_list = [{
        'id': invoice.id,
        'date': invoice.date.strftime('%Y-%m-%d'),
        'patient': invoice.customer,
        'doctor': invoice.doctor,
        'total': invoice.total,
        'status': invoice.status,
        'action': invoice.action
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
        PhieuLichDat.ngayKham,
        PhieuLichDat.trangThai,
        PhieuLichDat.caKham,
        NguoiBenh.id.label('nguoiBenh_id'),
        NguoiBenh.ho,
        NguoiBenh.ten,
        NguoiBenh.soDienThoai,
        NguoiBenh.ngaySinh,
        NguoiBenh.gioiTinh
    ).join(NguoiBenh, PhieuLichDat.nguoiBenh_id == NguoiBenh.id)

    query = query.filter(db.func.date(PhieuLichDat.ngayKham) == date, PhieuLichDat.trangThai == status)
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
        'nguoiBenh_id': schedule.nguoiBenh_id,
        'ho': schedule.ho,
        'ten': schedule.ten,
        'ngaySinh': schedule.ngaySinh.strftime('%Y-%m-%d'),
        'gioiTinh': 'Nam' if schedule.gioiTinh else 'Nữ',
        'caKham': {"sang": "Sáng", "chieu": "Chiều", "toi":"Tối"}[schedule.caKham],
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
    ).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id).join(NguoiBenh, PhieuKhamBenh.nguoiBenh_id == NguoiBenh.id)

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
    ).join(NguoiDung, PhieuKhamBenh.bacSi_id == NguoiDung.id).join(NguoiBenh, PhieuKhamBenh.nguoiBenh_id == NguoiBenh.id)
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
        'ngayKham': examination.ngay_kham.strftime('%Y-%m-%d'),
        'gioi_tinh': 'Nam' if examination.gioiTinh else 'Nữ',
        'soDienThoai': examination.soDienThoai
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
        PhieuLichDat.ngayKham,
        PhieuLichDat.trangThai,
        PhieuLichDat.caKham,
        NguoiBenh.id.label('nguoiBenh_id'),
        NguoiBenh.ho,
        NguoiBenh.ten,
        NguoiBenh.soDienThoai,
        NguoiBenh.ngaySinh,
        NguoiBenh.gioiTinh,
        PhieuLichDat.hoanThanh,
    ).join(NguoiBenh, PhieuLichDat.nguoiBenh_id == NguoiBenh.id).filter(PhieuLichDat.trangThai == True, PhieuLichDat.hoanThanh == False, db.func.date(PhieuLichDat.ngayKham) == datetime.now().date())

    query = query.filter(
            db.or_(
            (NguoiBenh.ho + " " + NguoiBenh.ten).like(f"%{q}%"),
            NguoiBenh.soDienThoai.like(f"%{q}%")
            )
        ).order_by(PhieuLichDat.ngayKham.desc()).limit(5).all()
    
    return [{
        'id': e.id,
        'nguoi_benh_id': e.nguoiBenh_id,
        'ho': e.ho,
        'ten': e.ten,
        'sdt': e.soDienThoai,
        'tuoi': datetime.now().year - e.ngaySinh.year,
        'gioi_tinh': 'Nam' if e.gioiTinh else 'Nữ',
        'nhom_mau': 'KXD'
        
    } for e in query]
