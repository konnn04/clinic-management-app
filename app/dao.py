import json
import os
from app import app, db
from app.models import HoaDonThanhToan, NguoiBenh, PhieuLichDat
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

def get_patients(draw, length, start, search_value, sort_column_index, sort_direction):
    columns = ['id', 'ho', 'ten','gioiTinh', 'ngaySinh', 'soDienThoai', 'lanCuoiGhe']
    
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
    sort_column_map = {
        0: NguoiBenh.id,
        1: NguoiBenh.ho,
        2: NguoiBenh.ten,
        3: NguoiBenh.gioiTinh,
        4: NguoiBenh.ngaySinh,
        5: NguoiBenh.soDienThoai,
        6: NguoiBenh.lanCuoiGhe
    }

    sort_column = columns[sort_column_index]
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