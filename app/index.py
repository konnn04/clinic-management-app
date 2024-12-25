import json
from datetime import datetime
from flask import render_template, request, jsonify, session
from app import app, utils, login_manager, roles_required, dao, login_patient_required
from flask_login import current_user, login_required, logout_user, login_user
import os
import cloudinary
# from cloudinary.uploader import upload
import random
from app.models import NguoiDung, VaiTro, NguoiBenh, TrangThaiLichDat
from app.momo_payment import utils as momo_utils
from app.twilio_service import utils as twilio_utils
from app.models import HoaDonThanhToan

host = '0.0.0.0'
port = os.getenv('DEV_PORT', 5000)

@app.context_processor
def update_template_context():
    u = session.get('current_user')
    is_login = False
    if u:
        is_login = True
    return {
        'meta':{
            'title': 'Hospital Management System',
            'description':'Chào mừng bạn đến với Phòng mạch OU, nơi cung cấp dịch vụ chăm sóc sức khỏe tốt nhất cho bạn và gia đình.',
            'keyword':'phòng mạch, phòng mạch OU, chăm sóc sức khỏe, bác sĩ, y tá, y khoa, y học, bệnh viện, bệnh tật, bệnh lý, thuốc, dược phẩm, y học cổ truyền, y học hiện đại, y học phương Đông, y học phương Tây, y học phổ thông, y học chuyên sâu, y học cấp cứu, y học phòng ngừa, y học gia đình, y học công cộng, y học cộng đồng, y học tư vấn, y học chăm sóc, y học tâm lý, y học thể chất, y học tinh thần, y học xã hội, y học môi trường, y học công nghệ, y học thông tin, y học truyền thông, y học giáo dục, y học đào tạo, y học nghiên cứu, y học phát triển, y học quản lý, y học hành vi, y học tư duy, y học sáng tạo, y học đổi mới, y học phát minh',
            'author':'Duy Quang Trieu'
        },
        'funcs': utils.get_nav(current_user),
        "is_login": is_login,
    }

@app.template_filter('format_money')
def format_money(value):
    return f"{value:,.0f} VND"

@login_manager.user_loader
def load_user(user_id):
    return NguoiDung.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointment', methods=['GET', 'POST'])
@login_patient_required
def appointment():
    cur_user = session.get('current_user')

    if request.method.__eq__('POST'):
        ngayHen = request.form.get('date_inp')
        gioKham = request.form.get('time')

        status = dao.add_appointments(cur_id=cur_user["id"], ngayHen=ngayHen, gioKham=gioKham)
        if status['status'] == 'success':
            return redirect(url_for('appointment_history', success='1'))
        else:
            return render_template('appointment.html', msg=status['message'])

    return render_template('appointment.html')

# test api start
# @app.route('/add_session', methods=['GET'])
# @login_patient_required
# def add_session():
#     u = session.get('current_user')
#     if not u:
#         u = NguoiBenh.query.get(1)
#         print(u.to_dict())
#         session['current_user'] = u.to_dict()
#     return redirect('/appointment/history')

# test api end

@app.route('/appointment/history', methods=['GET'])
@login_patient_required
def appointment_history():
    u = session.get('current_user')
    if not u:
        return redirect(url_for('guest_login'))
    return render_template('appointment_history.html')

@app.route('/appointment/history/detail/<int:order_id>', methods=['GET'])
def appointment_history_detail(order_id):
    u = session.get('current_user')
    if not u:
        return redirect(url_for('guest_login'))

    data = dao.get_appointment_history_detail(u['id'], order_id)
    return render_template('appointment_history_detail.html', data=data)


@app.route('/api/appointment/history', methods=['GET'])
@login_patient_required
def lookup_appointment_history():
    try:
        u = session.get('current_user')
        appointment_histories = dao.get_appointment_history(u['id'])
        return jsonify(appointment_histories), 200
    except Exception as ex:
        return jsonify({'message': ex}), 500

# Staff
@app.route('/staff/profile', methods=['GET', 'POST'])
@login_required
def staff_profile():
    data = {
        'ho': request.form.get('ho'),
        'ten': request.form.get('ten'),
        'ngaySinh': request.form.get('ngaySinh'),
        'avatar': request.form.get('avatar'),
        'ghiChu': request.form.get('ghiChu'),
    }
    current_data = current_user.to_dict()
    avatar_file = request.files.get('avatar')
    if request.method == 'POST' and (current_data != data or avatar_file != None):
        data['ngaySinh'] = datetime.strptime(request.form['ngaySinh'],'%Y-%m-%d')
        if ( avatar_file.headers[0][1] != 'form-data; name="avatar"; filename=""'):
            data['avatar'] = cloudinary.uploader.upload(avatar_file).get('secure_url')
            print(data['avatar'])
        # Ràng buộc lại dữ liệu
        status = dao.update_profile(data)
        if (status['status'] == 'success'):
            return redirect(url_for('staff_profile'))
        else:
            return render_template('staff/profile.html', msg=status['message'])
            
    user_data = {
        'id': current_user.id,
        'name': current_user.ho + ' ' + current_user.ten,
        'email': current_user.email,
        'phone': current_user.soDienThoai,
        'avatar': current_user.avatar,
        'role': current_user.role.name,
        'username': current_user.taiKhoan,
        'dob': current_user.ngaySinh.strftime('%Y-%m-%d'),
        'note': current_user.ghiChu,
    }
    return render_template('staff/profile.html', user_info=user_data)
    

# Patients

@app.route('/register',methods=["GET","POST"])
def patient_register():
    msg = ""
    if request.method.__eq__("POST"):
        ho = request.form.get('lastName')
        ten = request.form.get('firstName')
        email = request.form.get('email')
        soDienThoai = request.form.get('phone')
        gioiTinh = int(request.form.get('gender'))
        ghiChu = request.form.get('note')
        diaChi = request.form.get('address')
        ngaySinh = request.form.get('birthday')

        if not soDienThoai and not email:
            msg = "Phải nhập 1 trong 2 thông tin email hoặc số điện thoại"
        else:
            dao.add_patients(ho=ho,ten=ten,email=email,soDienThoai=soDienThoai,ngaySinh=ngaySinh,gioiTinh=gioiTinh,diaChi=diaChi,ghiChu=ghiChu)
            return redirect(url_for('patient_login'))
    return render_template('register.html',msg=msg)

@app.route('/send-otp',methods=['POST'])
def send_otp():
    data = request.json
    info = data.get('info') # Lấy thông tin có thể là số điện thoại hoặc email

    current_user = dao.check_user(info)

    if current_user:
        # print(current_user.to_dict())
        if '@' in info: # Nếu như là email
            otp = str(random.randint(100000, 999999))
            session['otp']=otp # Thêm trường otp để kiểm tra
            return utils.send_otp_to_email(current_user.email,otp)
        else: # Nếu như là số điện thoại
            current_user.soDienThoai = utils.convert_to_international_format(info)
            return twilio_utils.send_sms_otp(current_user.soDienThoai)
    else:
        return jsonify({"status": "failed",
                        "message": "Authentication failed"}),401



@app.route('/logout')
def patient_logout():
    if session.get('current_user'):
        session.pop('current_user')
    return redirect(url_for('patient_login'))

@app.route('/login',methods = ['GET','POST'])
def patient_login():
    if session.get('current_user'):
        return redirect(url_for('index'))
    msg = ""
    if request.method.__eq__('POST'):
        info = request.form.get('info').strip()
        otp = request.form.get('otp').strip()
        user = dao.check_user(info)
        if not user:
            return redirect(url_for('index'))

        if user.soDienThoai:
            user.soDienThoai = utils.convert_to_international_format(info)

        # try:
        if (info.__contains__("@") and otp.__eq__(session.get('otp'))) or \
            (twilio_utils.verify_sms_otp(user.soDienThoai, otp)['status'] == "verified"):

            session['current_user'] = user.to_dict()
            return redirect(url_for('index'))
        else:
            msg = "OTP không hợp lệ!!!"
        # except Exception as ex:
        #     print(ex)
        #     msg = "Vui lòng nhập thông tin người dùng"
    return render_template('login.html',msg=msg)

@app.route('/staff/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/staff')
def staff():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    next_urls = {
        VaiTro.BAC_SI: 'doctor',
        VaiTro.Y_TA: 'nurse',
        VaiTro.THU_NGAN: 'cashier',
        VaiTro.ADMIN: 'admin.index'
    }
    return redirect(url_for(next_urls[current_user.role]))

@app.route('/staff/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('staff'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        user = dao.check_account(username, password)
        if user and user.role not in [VaiTro.BENH_NHAN]:
            login_user(user)
            print("OK 2")
            return redirect(url_for('staff'))
        else:
            print("Another bug")
            return render_template('staff/login.html', msg='Sai tài khoản')
        
    return render_template('staff/login.html')


# Nurse
@app.route('/nurse', methods=['GET', 'POST'])
@login_required
@roles_required([VaiTro.Y_TA])
def nurse():
    return render_template('nurse/index.html', index=1)

@app.route('/nurse/schedule_list', methods=['GET', 'POST'])
@roles_required([VaiTro.Y_TA])
def schedule_list():
    list_ = {
        'current': datetime.now().strftime('%Y-%m-%d'),
    }
    return render_template('nurse/schedule-list.html', index=3, list=list_)

@app.route('/nurse/schedule/accept', methods=['POST'])
@login_required
@roles_required([VaiTro.Y_TA])
def accpect_schedule():
    id = request.form.get('id')
    res = dao.accept_schedule(id=id)
    if res:
        return jsonify({'status': 'success', 'message': 'Đã chấp nhận lịch hẹn'})
    return jsonify({'status': 'error', 'message': 'Đã có lỗi xảy ra'})


@app.route('/nurse/schedule/cancel', methods=['POST'])
@login_required
@roles_required([VaiTro.Y_TA])
def cancel_schedule():
    id = request.form.get('id')
    res = dao.cancel_schedule(id=id)
    if res:
        return jsonify({'status': 'success', 'message': 'Đã hủy lịch hẹn'})
    return jsonify({'status': 'error', 'message': 'Đã có lỗi xảy ra'})
# Admin


# Cashier
# Invoice: Hóa đơn trả sau
# Payment: Thanh toán trước
# Bill: Hóa đơn trả trước

@app.route('/cashier', methods=['GET', 'POST'])
@login_required
@roles_required([VaiTro.THU_NGAN])
def cashier():
    return render_template('cashier/index.html', index=1)

@app.route('/cashier/payment', methods=['GET', 'POST'])
@roles_required([VaiTro.THU_NGAN])
def payment():
    return render_template('cashier/payment.html', index=2)

@app.route('/cashier/payment/<string:order_hashed>', methods=['GET'])
@roles_required([VaiTro.THU_NGAN])
def pay(order_hashed):
    order_id = HoaDonThanhToan.decode_hashed_id(hashed_id=order_hashed)
    hoa_don = HoaDonThanhToan.query.filter(HoaDonThanhToan.id==order_id).first()
    msg=""


    if hoa_don:
        if hoa_don.trangThai == True:
            msg = "Hoa don da thanh toan"
        else:
            if hoa_don.payUrl:
                return redirect(hoa_don.payUrl)
            else:
                data = momo_utils.create_request_data(hoa_don=hoa_don)
                response = momo_utils.post_request(data)

                if 'payUrl' not in response.json():
                    msg=response.json()['message']
                else:
                    print("response data = ", response.json())
                    dao.set_payUrl(hoa_don=hoa_don,payUrl=response.json()['payUrl'])
                    return redirect(response.json()['payUrl'])
    else:
        msg="Hoa don khong ton tai"

    return render_template('cashier/payment.html', data={"status":"error","message": msg})

@app.route('/cashier/invoice/<string:order_hashed>', methods=['GET'])
@roles_required([VaiTro.THU_NGAN])
def invoice_detail(order_hashed):
    order_id = HoaDonThanhToan.decode_hashed_id(hashed_id=order_hashed)
    hoa_don = HoaDonThanhToan.query.filter(HoaDonThanhToan.id==order_id).first()
    msg=""


    if hoa_don:
        return render_template('cashier/invoice_detail.html', data={"status": "success", "message": hoa_don.to_dict()})
    else:
        msg="Hoa don khong ton tai"
        return render_template('cashier/invoice_detail.html', data={"status":"error","message": msg})



@app.route('/payment/result/<string:order_hashed>', methods=['POST'])
def payment_result(order_hashed):
    if request.method.__eq__('POST'):
        print("Momo goi")
        data = request.data

        response_str = data.decode('utf-8')
        response_dict = json.loads(response_str)

        result = dao.handle_payment_result(response_dict)

        print( {
            "result": result,
            "data": response_dict
        })
        return jsonify({})

@app.route('/cashier/invoices', methods=['GET', 'POST'])
@roles_required([VaiTro.THU_NGAN])
def invoices():
    return render_template('cashier/invoices.html', index=2)


# Doctor
@app.route('/doctor', methods=['GET', 'POST'])
@login_required
@roles_required([VaiTro.BAC_SI])
def doctor():
    return render_template('doctor/index.html',  index=1)

@app.route('/doctor/patients', methods=['GET', 'POST'])
@roles_required([VaiTro.BAC_SI])
def patients_doctor():
    return render_template('doctor/patients.html', index=2)

@app.route('/doctor/create-patient', methods=['GET', 'POST'])
@roles_required([VaiTro.BAC_SI])
def create_patient():
    return render_template('doctor/create-patient.html', index=2)

#API
@app.route('/api/get-dieases', methods=['GET'])
def get_dieases():
    q = request.args.get('q')
    exists = request.args.get('exists')

    return jsonify(utils.get_diseases(q, exists,5))

# Lấy danh sách hoá đơn
@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    draw = request.args.get('draw', type=int, default=1)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    sort = request.args.get('sort')
    order = request.args.get('order', default='asc')
    search_value = request.args.get('search[value]', default='')
    '''
    Lấy dữ liệu từ request
    draw: Số thứ tự của request
    start: Vị trí bắt đầu lấy dữ liệu
    length: Số lượng dữ liệu cần lấy
    sort_column: Cột cần sắp xếp
    sort_direction: Hướng sắp xếp
    search_value: Giá trị tìm kiếm
    '''
    q = dao.load_invoices(draw, length, start, search_value, sort, order)
    return jsonify(q)

@app.route('/api/patient-stat', methods=['GET'])
@roles_required([VaiTro.BAC_SI, VaiTro.Y_TA, VaiTro.THU_NGAN, VaiTro.ADMIN])
def patient_stat():
    return jsonify(dao.patient_stat())

@app.route('/api/patient-list', methods=['GET'])
@roles_required([VaiTro.BAC_SI, VaiTro.Y_TA, VaiTro.THU_NGAN, VaiTro.ADMIN])
def get_patients():
    draw = request.args.get('draw', type=int, default=1)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    sort_column = request.args.get('sort', default='id')
    sort_direction = request.args.get('order', default='asc')
    search_value = request.args.get('search[value]', default='')

    return jsonify(dao.get_patients(
        draw=draw, 
        length=length,
        start= start, 
        search_value=search_value, 
        sort_column=sort_column, 
        sort_direction=sort_direction))

@app.route('/api/schedule-list', methods=['GET'])
@roles_required([VaiTro.Y_TA])
def get_schedule_list():
    draw = int(request.args.get('draw', 1))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '')
    order_column = request.args.get('sort', 'id')
    order_dir = request.args.get('order', 'asc')
    status = request.args.get('schedule_status', 'false')
    if status == 'true':
        status = TrangThaiLichDat.DA_DUYET
    else:
        status = TrangThaiLichDat.CHUA_DUYET
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    return jsonify(
        dao.load_schedule_list(
            date=date, status=status, 
            draw=draw, length=length, 
            start=start, 
            search=search_value,
            sort_column=order_column, 
            sort_order=order_dir
            )
        )

@app.route('/api/examination-list-overview', methods=['GET'])
@login_required
@roles_required([VaiTro.BAC_SI, VaiTro.Y_TA, VaiTro.THU_NGAN, VaiTro.ADMIN])
def get_examination_list():
    draw = int(request.args.get('draw', 1))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '')
    order_column = request.args.get('sort', 'id')
    order_dir = request.args.get('order', 'asc')
    return jsonify(
        dao.load_examination_list(
            draw=draw, length=length, 
            start=start, 
            search=search_value,
            sort_column=order_column, 
            sort_order=order_dir
            )
        )
    
@app.route('/api/examination-list-v1', methods=['GET'])
@login_required
@roles_required([VaiTro.BAC_SI, VaiTro.Y_TA])
def get_examination_list_v1():
    col_sort = request.args.get('col_sort', 'ngay_kham')
    order = request.args.get('order', 'desc')
    page = request.args.get('page_index', 1, type=int)
    data = dao.get_examination_list_v1(
        sort_column=col_sort, 
        sort_order=order, 
        page_index=page
        )
    return jsonify(data)


@app.route('/api/schedules-overview',methods=['GET'])
@login_required
@roles_required([VaiTro.BAC_SI])
def get_schedules_overview():
    q = request.args.get('q')
    return jsonify(dao.get_schedules_overview(q))

@app.route('/api/medicine', methods=['GET'])
@login_required
@roles_required([VaiTro.BAC_SI])
def get_medicine():
    q = request.args.get('name')
    exists = request.args.get('exists')
    return jsonify(dao.get_medicine(q, exists))

@app.route('/api/get-services', methods=['GET'])
@login_required
@roles_required([VaiTro.BAC_SI])
def get_services():
    q = request.args.get('q')
    exists = request.args.get('exists')
    return jsonify(dao.get_services(q, exists))

@app.route('/api/save-examination', methods=['POST'])
@login_required
@roles_required([VaiTro.BAC_SI])
def save_patient():
    data = request.json
    return jsonify(dao.save_patient(data))

@app.route('/api/patient/get-appointment-list', methods=['GET'])
@login_patient_required
def get_appointment_list():
    u = session.get('current_user')
    return jsonify(dao.get_appointment_list(u['id']))

@app.route('/api/cancel-appointment', methods=['POST'])
@login_patient_required
def cancel_appointment():
    lichKham_id = request.json['lichKham_id']
    return jsonify(dao.cancel_appointment(lichKham_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('layouts/404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('layouts/403.html'), 403


if __name__ == '__main__':
    with app.app_context():
        from app.admin import *
        db.create_all()
        dao.init_varaibles()
        app.run(host=host, port=port, debug=True)
        # app.run(host=host, port=port)


