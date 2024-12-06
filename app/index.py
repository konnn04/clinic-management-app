from flask import  render_template, request
from app import app, login_manager, roles_required
from flask_login import current_user, login_required, logout_user,login_user
from app import utils
import pdb

from app.models import NguoiDung, VaiTro

host = '0.0.0.0'
port = 5100

def update_template_context():
    return dict(
        meta=dict(
            title='Phòng mạch OU - Trang chủ',
            description='Chào mừng bạn đến với Phòng mạch OU, nơi cung cấp dịch vụ chăm sóc sức khỏe tốt nhất cho bạn và gia đình.',
            keywords='phòng mạch, phòng mạch OU, chăm sóc sức khỏe, bác sĩ, y tá, y khoa, y học, bệnh viện, bệnh tật, bệnh lý, thuốc, dược phẩm, y học cổ truyền, y học hiện đại, y học phương Đông, y học phương Tây, y học phổ thông, y học chuyên sâu, y học cấp cứu, y học phòng ngừa, y học gia đình, y học công cộng, y học cộng đồng, y học tư vấn, y học chăm sóc, y học tâm lý, y học thể chất, y học tinh thần, y học xã hội, y học môi trường, y học công nghệ, y học thông tin, y học truyền thông, y học giáo dục, y học đào tạo, y học nghiên cứu, y học phát triển, y học quản lý, y học hành vi, y học tư duy, y học sáng tạo, y học đổi mới, y học phát minh',
            author='Duy Quang Trieu'
        ),
    )

app.context_processor(update_template_context)

@login_manager.user_loader
def load_user(user_id):
    return NguoiDung.query.get(int(user_id))

# Các route được định nghĩa trong file này sẽ được gọi khi truy cập vào địa chỉ của server
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    return render_template('appointment.html')


@app.route('/logout')
def patient_logout():
    logout_user()
    return redirect(url_for('patient_login'))


@app.route('/staff')
def staff():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role == VaiTro.ADMIN:
        return redirect(url_for('admin.index'))
    elif current_user.role == VaiTro.BAC_SI:
        return redirect(url_for('doctor'))
    else:
        return redirect(url_for('index'))

@app.route('/staff/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('staff')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_account(username, password)
        if user and user.role not in [VaiTro.BENH_NHAN]:
            login_user(user)
            return redirect(url_for('staff'))
        else:
            return render_template('staff/login.html', msg='Sai tài khoản')
        
    return render_template('staff/login.html')
# Doctor
@app.route('/doctor', methods=['GET', 'POST'])
@roles_required([VaiTro.BAC_SI])
def doctor():
    return render_template('doctor/index.html')

@app.route('/doctor/patients', methods=['GET', 'POST'])
@roles_required([VaiTro.BAC_SI])
def patients_doctor():
    return render_template('doctor/patients.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('layouts/404.html'), 404


if __name__ == '__main__':
    from app.admin import *
    app.run(host=host, port=port, debug=True)


