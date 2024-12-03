from flask import  render_template, request
from app.admin import *
from app import app, login_manager
from flask_login import current_user, login_required, logout_user

from app.models import NguoiDung

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

@app.route('/staff', methods=['GET', 'POST'])
def login():
    return render_template('staff/login.html')

# Doctor
@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    return render_template('doctor/index.html')

@app.route('/doctor/patients', methods=['GET', 'POST'])
def patients_doctor():
    return render_template('doctor/patients.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('layouts/404.html'), 404


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)


