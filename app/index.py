import json
# from crypt import methods
from datetime import datetime

from flask import render_template, request, jsonify
from app import app, login_manager, roles_required
from flask_login import current_user, login_required, logout_user, login_user
from app import utils
import pdb
import cloudinary
from cloudinary.uploader import upload

from app.models import NguoiDung, VaiTro

host = '0.0.0.0'
port = 5100



@app.context_processor
def update_template_context():
    return {
        'meta':{
            'title': 'Hospital Management System',
            'description':'Chào mừng bạn đến với Phòng mạch OU, nơi cung cấp dịch vụ chăm sóc sức khỏe tốt nhất cho bạn và gia đình.',
            'keyword':'phòng mạch, phòng mạch OU, chăm sóc sức khỏe, bác sĩ, y tá, y khoa, y học, bệnh viện, bệnh tật, bệnh lý, thuốc, dược phẩm, y học cổ truyền, y học hiện đại, y học phương Đông, y học phương Tây, y học phổ thông, y học chuyên sâu, y học cấp cứu, y học phòng ngừa, y học gia đình, y học công cộng, y học cộng đồng, y học tư vấn, y học chăm sóc, y học tâm lý, y học thể chất, y học tinh thần, y học xã hội, y học môi trường, y học công nghệ, y học thông tin, y học truyền thông, y học giáo dục, y học đào tạo, y học nghiên cứu, y học phát triển, y học quản lý, y học hành vi, y học tư duy, y học sáng tạo, y học đổi mới, y học phát minh',
            'author':'Duy Quang Trieu'
        },
        'funcs': utils.get_nav(current_user)
    }

@login_manager.user_loader
def load_user(user_id):
    return NguoiDung.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    return render_template('appointment.html')

@app.route('/staff/profile', methods=['GET', 'POST'])
@login_required
def staff_profile():
    data = request.form.to_dict()
    current_data = current_user.to_dict()
    avatar_file = request.files.get('avatar')
    if request.method == 'POST' and (current_data != data or avatar_file != None):
        data['ngaySinh'] = datetime.strptime(request.form['ngaySinh'],'%Y-%m-%d')
        if ( avatar_file.headers[0][1] != 'form-data; name="avatar"; filename=""'):
            data['avatar'] = cloudinary.uploader.upload(avatar_file).get('secure_url')
            print(data['avatar'])
        # Ràng buộc lại dữ liệu
        for key, value in data.items():
            setattr(current_user, key, value)
        db.session.commit()
        return redirect(url_for('staff_profile'))
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
    


@app.route('/logout')
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
        user = utils.check_account(username, password)
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



# Admin


# Cashier

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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('layouts/404.html'), 404



if __name__ == '__main__':
    from app.admin import *
    app.run(host=host, port=port, debug=True)


