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
    
def load_schedule_list(date,type, draw, length, start, search, sort_column, sort_order):
    query = PhieuLichDat.query.filter(PhieuLichDat.ngay == date, PhieuLichDat.loai == type)
    if search:
        query = query.filter(
            db.or_(
                PhieuLichDat.nguoiBenh.soDienThoai.like(f"%{search}%"),
                PhieuLichDat.nguoiBenh.hoten.like(f"%{search}%")
            )
        )
    total = query.count()
    # Tạm tắt sort
    query = query.order.by(PhieuLichDat.ca_id)
    schedules = query.offset(start).limit(length).all()
    schedule_list = [{
        'id': schedule.id,
        'nguoiBenh_id': schedule.nguoiBenh.id,
        'hoTen': schedule.nguoiBenh.hoten,
        'ngaySinh': schedule.nguoiBenh.ngaySinh.strftime('%Y-%m-%d'),
        'gioiTinh': 'Nam' if schedule.nguoiBenh.gioiTinh else 'Nữ',
        'gioKham': schedule.ca.gio_kham(),
        'bacSi': schedule.bacSi.hoten if schedule.bacSi else 'Không chọn',
    } for schedule in schedules]
    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': schedule_list
    }