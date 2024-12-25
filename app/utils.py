from app.models import VaiTro
# from werkzeug.security import generate_password_hash, check_password_hash
from app import db, dao
from datetime import datetime
from collections import defaultdict
from sqlalchemy import text

from flask import jsonify

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import phonenumbers


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



def send_otp_to_email(to_email,otp):
    api_key = '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'
    message = Mail(
        from_email='2251012121quang@ou.edu.vn',
        to_emails=to_email,
        subject='HERE IS YOUR OTP CODE',
        html_content=f'<p>Your OTP code is: </p> <h3>{otp}</h3>'
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("OTP sent successfully!")
        return jsonify({
            "status": "success",
            'message': 'OTP sent successfully!'
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "status": 'error',
            "message": 'Failed to send OTP!'}), 500


def convert_to_international_format(phone_number, country_code="VN"):
    try:
        parsed_number = phonenumbers.parse(phone_number, country_code)
        international_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        return international_number

    except phonenumbers.NumberParseException as e:
        return f"Invalid phone number: {e}"


def get_common_parameters(request):
    draw = request.args.get('draw', type=int, default=1)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    sort_column = request.args.get('sort', default='id')
    sort_direction = request.args.get('order', default='asc')
    search_value = request.args.get('search[value]', default='')

    return {
        'draw': draw,
        'start': start,
        'length': length,
        'search_value': search_value,
        'sort_column': sort_column,
        'sort_direction': sort_direction
    }
