## Môn Công nghệ phần mềm

# Đề tài Quản lý phòng mạch tư

### Giảng viên yêu cầu: 

Thầy Dương Hữu Thành

### Thành viên:

- 2251012121 - Phí Minh Quang

- 2251012046 - Hoàng Anh Duy

- 2251052127 - NguyễnThanh Triều

## Giới thiệu:

## Hướng dẫn:

### 1.  Tải và khởi chạy

- Clone về máy: `git clone https://github.com/konnn04/CNPM_QuanLyPhongMach.git`.
- Tạo môi trường ảo: `python -m venv <tên môi trường>`.
- Mở môi trường: `<tên môi trường>/Scripts/activate`.
- Tải thư viện: `pip install -r requirements.txt`.
- Đổi tên file `.env-template` thành `.env` và chỉnh sửa các thông tin cần thiết để app chạy.
- Sửa địa chỉ web site ở 2 dòng cuối file `momo_payment/__init__.py`
- Cấu hình database ở file `app/__init__.py`
- Chạy file `generate_db.py` để tạo dữ liệu mẫu.
- Chạy file `test.py` để tạo thêm nhiều dữ liệu mẫu.
- Chạy dự án: `python -m app.index`.

### 2. Thông tin các endpoint và địa chỉ
- Dành cho khách hàng: http://localhost.com:5100
- Nhân viên và admin dùng trang: http://localhost.com:5100/staff
- Các endpoint khác vui lòng tham khảo index.py


