from sqlalchemy import Integer,String,Float,ForeignKey,Boolean,Column,DateTime,Enum,Text, Time
from app import app,db
from enum import Enum as RoleEnum
from app.models import NguoiBenh, NguoiDung, PhieuKhamBenh, PhieuLichDat, HoaDonThanhToan
from datetime import datetime
import random

ho = ["Nguyễn Thanh", "Trần Thanh", "Lê Thanh", "Phạm Thanh", "Nguyễn Văn", "Trần Văn", "Lê Văn", "Phạm Văn", "Nguyễn Thị", "Trần Thị", "Lê Thị", "Phạm Thị"]

ten = ["Hải", "Hùng", "Hưng", "Hà", "Hạnh", "Hiền", "Hoa", "Hồng", "Huyền", "Hương", "Huy", "Hào"]

# dichvu = ["Khám bệnh", "Tư vấn", "Chữa bệnh", "Điều trị", "Phẫu thuật", "Chăm sóc", "Dinh dưỡng", "Tập thể dục", "Yoga", "Thư giãn"]

def randomName():
    return random.choice(ho) + " " + random.choice(ten)

def randomPhone():
    return "0" + str(random.randint(100000000, 999999999))

if __name__ == "__main__":
   # Tạo dữ liệu người dùng
    with app.app_context():
        for i in range(1, 11):
            user = NguoiBenh(
                ho = random.choice(ho),
                ten = random.choice(ten),
                gioiTinh = random.choice([True, False]),
                ngaySinh = datetime(random.randint(1950, 2000), random.randint(1, 12), random.randint(1, 28)),
                diaChi = "Số " + str(random.randint(1, 100)) + ", " + random.choice(["Đường 1", "Đường 2", "Đường 3", "Đường 4", "Đường 5"]),
                soDienThoai = randomPhone(),
                email = "nguoibenh" + str(i) + "@gmail.com"
            )
            
            
            schedule = PhieuLichDat(
                ngayHen = datetime.now(),
                caHen = random.choice(["sang", "chieu", "toi"]),
                trangThai = False,
                benhNhan_id = i+1
            )

            try:
                db.session.add(user)
                db.session.add(schedule)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()