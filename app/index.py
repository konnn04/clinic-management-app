from flask import  render_template, request
from app import app
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

# Các route được định nghĩa trong file này sẽ được gọi khi truy cập vào địa chỉ của server
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    return render_template('appointment.html')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)

