from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, Column, DateTime, Enum, Text, Time
from app import app, db
from enum import Enum as RoleEnum
from app.models import NguoiBenh, NguoiDung, PhieuKhamBenh, PhieuLichDat, HoaDonThanhToan, CaHen
from datetime import datetime
import random

ho = ["Nguyễn ", "Trần ", "Lê Thanh", "Phạm ", "Nguyễn ", "Trần Văn", "Lê Văn", "Phạm ",
      "Nguyễn ", "Trần Thị", "Lê Thị", "Phạm "]

ten = ["Hải", "Hùng", "Hưng", "Hà", "Hạnh", "Hiền", "Hoa", "Hồng", "Huyền", "Hương", "Huy", "Hào"]


# dichvu = ["Khám bệnh", "Tư vấn", "Chữa bệnh", "Điều trị", "Phẫu thuật", "Chăm sóc", "Dinh dưỡng", "Tập thể dục", "Yoga", "Thư giãn"]

def randomName():
    return random.choice(ho) + " " + random.choice(ten)


def randomPhone():
    return "0" + str(random.randint(100000000, 999999999))


if __name__ == "__main__":
    # Tạo dữ liệu người dùng
    with app.app_context():
        for i in range(1, 39):
            user = NguoiBenh(
                ho=random.choice(ho),
                ten=random.choice(ten),
                gioiTinh=random.choice([True, False]),
                ngaySinh=datetime(random.randint(1950, 2000), random.randint(1, 12), random.randint(1, 28)),
                diaChi="Số " + str(random.randint(1, 100)) + ", " + random.choice(
                    ["Đường 1", "Đường 2", "Đường 3", "Đường 4", "Đường 5"]),
                soDienThoai=randomPhone(),
                email="nguoibenh" + str(i) + "dsd@gmail.com"
            )
            db.session.add(user)
            db.session.commit()

            schedule = PhieuLichDat(
                ngayHen=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                # ngayHen=datetime.now(),


                caHen=random.choice([CaHen.SANG, CaHen.CHIEU, CaHen.TOI]),
                benhNhan_id=i + 3
            )
            db.session.add(schedule)
            db.session.commit()
            # try:
            #     db.session.add(schedule)
            #     db.session.commit()
            # except Exception as e:
            #     print(e)
            #     db.session.rollback()

# if __name__ == '__main__':
#     with app.app_context():
#         hoa_don=HoaDonThanhToan.query.get(3)

#         # print(hoa_don.to_dict())
#         print(hoa_don.hashed_id)
