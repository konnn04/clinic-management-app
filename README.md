## Môn Công nghệ phần mềm

# Đề tài Quản lý phòng mạch tư

### Giảng viên yêu cầu:

Thầy Dương Hữu Thành

### Thành viên:

- 2251012121 - Phí Minh Quang

- 2251012046 - Hoàng Anh Duy

- 2251052127 - NguyễnThanh Triều

## Giới thiệu:

Hệ thống Quản lý Phòng khám là một ứng dụng web được phát triển để hỗ trợ quản lý các hoạt động trong một phòng khám, bao gồm quản lý lịch hẹn, thông tin bệnh nhân, hóa đơn thanh toán và các dịch vụ y tế khác. Hệ thống này giúp cải thiện quy trình làm việc của nhân viên y tế và nâng cao trải nghiệm của bệnh nhân.

## Tính năng

- **Quản lý lịch hẹn**: Bệnh nhân có thể đặt lịch hẹn với bác sĩ và xem lịch sử hẹn của mình.
- **Quản lý thông tin bệnh nhân**: Nhân viên y tế có thể xem và cập nhật thông tin bệnh nhân, bao gồm hồ sơ y tế và thông tin liên lạc.
- **Quản lý hóa đơn**: Hệ thống cho phép tạo và quản lý hóa đơn thanh toán cho bệnh nhân, bao gồm thanh toán trực tuyến qua MoMo.
- **Quản lý nhân viên**: Quản lý thông tin và quyền truy cập của nhân viên trong hệ thống.
- **Thống kê**: Cung cấp các báo cáo và thống kê về số lượng bệnh nhân, doanh thu và các dịch vụ đã cung cấp.

## Công nghệ sử dụng

- **Flask**: Framework web cho Python.
- **SQLAlchemy**: ORM cho việc tương tác với cơ sở dữ liệu.
- **Cloudinary**: Dịch vụ lưu trữ hình ảnh.
- **Twilio**: Dịch vụ gửi SMS OTP.
- **MoMo**: Dịch vụ thanh toán trực tuyến.

## Hướng dẫn cài đặt

1. **Clone repository**:
   ```bash
   git clone https://github.com/konnn04/CNPM_QuanLyPhongMach.git
   ```
2. **Tạo môi trường ảo**:
   ```bash
   python -m venv <tên môi trường>
   ```
3. **Kích hoạt môi trường**:
   ```bash
   <tên môi trường>/Scripts/activate
   ```
4. **Cài đặt các thư viện cần thiết**:

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   python test.py
   ```

5. **Cấu hình file `.env`**: Đổi tên file `.env-template` thành `.env` và chỉnh sửa các thông tin cần thiết để ứng dụng hoạt động.
6. **Cấu hình database**: Chỉnh sửa thông tin kết nối database trong file `app/__init__.py`.
7. **Chạy file tạo dữ liệu mẫu**:
   ```bash
   python generate_db.py
   ```
8. **Chạy ứng dụng**:
   ```bash
   python -m app.index
   ```

## Các endpoint chính

- **Trang chủ**: `http://localhost.com:5000`
- **Trang dành cho nhân viên và admin**: `http://localhost.com:5000/staff`
- **API cho lịch hẹn**: `/api/appointment/history`
- **API cho hóa đơn**: `/api/invoices`
- **API cho thông tin bệnh nhân**: `/api/patient-list`
