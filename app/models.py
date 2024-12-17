from sqlalchemy import Integer,String,Float,ForeignKey,Boolean,Column,DateTime,Enum,Text, Time
from app import app,db
from sqlalchemy.orm import relationship, mapped_column, Mapped, backref
from enum import Enum as RoleEnum
from datetime import datetime, time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class VaiTro(RoleEnum):
    ADMIN = 1
    BAC_SI = 2
    Y_TA = 3
    BENH_NHAN = 4
    THU_NGAN = 5


class NguoiDung(db.Model, UserMixin): 
    __tablename__ = 'nguoiDung'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ho = Column(String(10),nullable=False,unique = False)
    ten = Column(String(10),nullable = False)
    ngaySinh = Column(DateTime,nullable = False)
    soDienThoai = Column(String(15),nullable=True,unique = True)
    email = Column(String(50),nullable=True,unique=True)
    ghiChu = Column(String(255),nullable = True)
    taiKhoan = Column(String(50),nullable = False,unique = True)
    matKhau = Column(Text,nullable = False)
    avatar = Column(String(255),nullable = True)
    role = Column(Enum(VaiTro),nullable = False)
    gioiTinh = Column(Boolean,nullable = False,default = True) # True: Nam, False: Nu
    
    def __str__(self):
        return f"{self.ho} {self.ten}"

    def to_dict(self):
        return {
            'id': self.id,
            'ho': self.ho,
            'ten': self.ten,
            'ngaySinh': self.ngaySinh,
            'soDienThoai': self.soDienThoai,
            'email': self.email,
            'ghiChu': self.ghiChu,
            'taiKhoan': self.taiKhoan,
            'matKhau': 'self.matKhau',
            'avatar': self.avatar,
            'role': self.role.name,
        }

    def check_password(self,password):
        return check_password_hash(self.matKhau,password)
    
    def set_password(self,password):
        self.matKhau = generate_password_hash(password)
        

class NguoiBenh(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    hoTen = Column(String(50),nullable = False)
    gioiTinh = Column(Boolean,nullable = False,default = True) # True: Nam, False: Nu
    ngaySinh = Column(DateTime,nullable = False)
    soDienThoai = Column(String(15),nullable = False)
    email = Column(String(50),nullable = True)
    diaChi = Column(String(255),nullable = False)
    phieuLichDat = relationship('PhieuLichDat',backref = 'nguoiBenh',lazy = True)

    def getAge(self):
        return datetime.now().year - self.ngaySinh.year
    
    def lanCuoiGhe(self):
        return PhieuLichDat.query.filter(PhieuLichDat.nguoiBenh_id == self.id).order_by(PhieuLichDat.ngayHen.desc()).first().ngayHen
    


class QuyDinh(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    value = Column(Integer,nullable = False)
    description = Column(String(255),nullable = False)
    nguoiQuanTri_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)

class HoaDonThanhToan(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ngayKham = Column(DateTime,default = datetime.utcnow,nullable=False)
    tienKham = Column(Float,nullable = False,default = 0.0)
    tienThuoc = Column(Float,nullable = False,default = 0.0)
    tongTien = Column(Float,nullable = False,default = 0.0)
    ngayLapHoaDon = Column(DateTime,default = datetime.utcnow,nullable=True)
    trangThai = Column(Boolean,nullable = False,default = False)
    # Bac Si
    phieuKham_id = Column(Integer, ForeignKey("phieuKham.id"), unique=True)

class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieuKham'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ngayKham = Column(DateTime,default = datetime.utcnow)
    trieuChung = Column(String(255),nullable = False)
    duDoanLoaiBenh = Column(String(255),nullable = False)
    bacSi_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)
    benhNhan_id = Column(Integer,ForeignKey(NguoiBenh.id),nullable = False)
    phieuDichVu = relationship('PhieuDichVu',backref = backref('phieuKham',uselist = False)) 
    hoaDonThanhToan = relationship('HoaDonThanhToan', backref = backref('phieuKham',uselist = False))

class PhieuDichVu(db.Model):
    __tablename__ = 'phieudichvu'
    id = Column(Integer,primary_key = True,autoincrement=True)
    ngayLap = Column(DateTime,default=datetime.utcnow)
    ghiChu = Column(Text,nullable=True)
    phieukham_id = Column(Integer,ForeignKey("phieuKham.id"),unique = True)

class LoaiDichVu(db.Model):
    __tablename__ = 'loaidichvu'
    id = Column(Integer,primary_key = True,autoincrement=True)
    tenDichVu = Column(String(255),nullable=False,unique=True)
    giaDichVu = Column(Float,default=0,nullable=False)
    moTa = Column(Text,nullable=True)

chiTietDichVu = db.Table('chiTietDichVu',
                         Column('phieuDichVu_id',
                                Integer,
                                ForeignKey('phieudichvu.id'),
                                primary_key=True,
                                ),
                        Column('loaiDichVu',
                               Integer,
                               ForeignKey('loaidichvu.id'),
                               primary_key=True),
                        Column('ketQua',String(255),nullable=False))

class DanhMucThuoc(db.Model):
    __tablename__ = 'danhMucThuoc'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ten = Column(String(100),nullable = False,unique=True)
    thuoc = relationship('Thuoc',backref = 'danhMucThuoc',lazy = True)

class LoHang(db.Model):
    __tablename__ = 'loHang'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayNhap = Column(DateTime, default=datetime.utcnow)
    hanSuDung = Column(DateTime, nullable=False)
    ngaySanXuat = Column(DateTime, nullable=False)
    thuoc = relationship("Thuoc",backref = backref('loHang',uselist = False))

class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ten = Column(String(100), nullable=False,unique = True)
    nhaCungCap = Column(String(100), nullable=False)
    xuatXu = Column(String(100), nullable=False)
    donVi = Column(String(100), nullable=False)
    danhMucThuoc_id = Column(Integer, ForeignKey(DanhMucThuoc.id), nullable=False)
    loHang_id = Column(Integer,ForeignKey("loHang.id"),unique = True)

    def __str__(self):
        return self.ten

class DonThuoc(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    phieu_id = Column(Integer,ForeignKey(PhieuKhamBenh.id),nullable = False)
    thuoc_id = Column(Integer,ForeignKey(Thuoc.id),nullable = False)
    cachDung = Column(String(255),nullable = False)
    soLuong = Column(Integer,nullable = False,default = 0)

# Trieu thêm
class CaLamViec(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ten = Column(String(100), nullable=False)
    batDau = Column(Time, nullable=False)
    ketThuc = Column(Time, nullable=False)

    def gio_kham(self):
        return f'{self.batDau.strftime("%H:%M")} - {self.ketThuc.strftime("%H:%M")}'
    

class PhieuLichDat(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ngayDat = Column(DateTime,nullable = False,default = datetime.now())
    ngayHen = Column(DateTime,nullable = False)
    trangThai = Column(Boolean,nullable = False,default = False)
    ca_id = Column(Integer,ForeignKey(CaLamViec.id),nullable = False)
    # Nguoi benh dat lich
    nguoiBenh_id = Column(Integer,ForeignKey(NguoiBenh.id),nullable = False)


    
class LichLamViec(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    bacSi_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    ca_id = Column(Integer, ForeignKey(CaLamViec.id), nullable=False)
    ngay_trong_tuan = Column(Integer, nullable=False) 
   


def initCaLamViec():
    i = 0
    # Từ 7h đến 21h, mỗi 30 phút một ca
    while CaLamViec.query.count() < 28:
        ca = CaLamViec(ten=f'Ca {(i*2)+1}', batDau=time(hour=7+i, minute=0), ketThuc=time(hour=7+i, minute=30))
        ca2 = CaLamViec(ten=f'Ca {(i*2)+2}', batDau=time(hour=7+i, minute=30), ketThuc=time(hour=8+i, minute=0))
        db.session.add(ca)
        db.session.add(ca2)
        i += 1
    db.session.commit()
    # Ca sáng: 7h00 - 11h00: Ca 0 -> Ca 7
    # Ca chiều: 13h00 - 17h00: Ca 12 -> Ca 19
    # Ca tối: 19h00 - 21h00: Ca 24 -> Ca 27

def initLichLamViec(bac_si, type = 'sang'):
    # 0: CN, 1: T2, 2: T3, 3: T4, 4: T5, 5: T6, 6: T7
    if type == 'sang':
        for i in range(7):
            for j in range(1, 9):
                lich = LichLamViec(bacSi_id=bac_si.id, ca_id=j, ngay_trong_tuan=i)
                db.session.add(lich)

    if type == 'chieu':
        for i in range(7):
            for j in range(13, 21):
                lich = LichLamViec(bacSi_id=bac_si.id, ca_id=j, ngay_trong_tuan=i)
                db.session.add(lich)
    if type == 'toi':
        for i in range(7):
            for j in range(25, 29):
                lich = LichLamViec(bacSi_id=bac_si.id, ca_id=j, ngay_trong_tuan=i)
                db.session.add(lich)
    db.session.commit()

def initUser():
    ad = NguoiDung(ho = 'admin',ten = 'admin',ngaySinh = datetime.now(),soDienThoai = '0123456789',email = 'admin@admin.com',taiKhoan = 'admin',matKhau = generate_password_hash('admin'),role = VaiTro.ADMIN)
    bs = NguoiDung(
        ho='Nguyen', 
        ten='Van A', 
        ngaySinh=datetime(1999, 1, 1),
        soDienThoai='012345434789', 
        email = 'a@a.com',
        taiKhoan='doctor1',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.BAC_SI)
    
    bs2 = NguoiDung(
        ho='Le', 
        ten='Van K', 
        ngaySinh=datetime(1999, 10, 12),
        soDienThoai='012345431189', 
        email = 'aaa@a.com',
        taiKhoan='doctor2',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.BAC_SI)
    
    yt = NguoiDung(
        ho='Nguyen', 
        ten='Van B', 
        ngaySinh=datetime.now(), 
        soDienThoai='012345456744', 
        email = 'b@b.com',
        taiKhoan='nurse1',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.Y_TA)
    c = NguoiDung(
        ho='Nguyen', 
        ten='Van C', 
        ngaySinh=datetime.now(), 
        soDienThoai='012312256789', 
        email = 'c@c.com',
        taiKhoan='cashier1',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.THU_NGAN)
    db.session.add(ad)
    db.session.add(bs)
    db.session.add(bs2)
    db.session.add(yt)
    db.session.add(c)
    db.session.commit()
    initLichLamViec(bs, 'sang')
    initLichLamViec(bs2, 'chieu')

def initPhieuLichDat():
    nb1 = NguoiBenh(hoTen = 'Nguyen Van A',ngaySinh = datetime.now(),soDienThoai = '0123456789',email = 'a@gmail.com',diaChi = '123 abc')
    nb2 = NguoiBenh(hoTen = 'Nguyen Van b',ngaySinh = datetime.now(),soDienThoai = '0123456788',email = 'a2@gmail.com',diaChi = '123 abc')
    nb3 = NguoiBenh(hoTen = 'Nguyen Van C',ngaySinh = datetime.now(),soDienThoai = '0123456787',email = 'a3@gmail.com',diaChi = '123 abc')
    nb4 = NguoiBenh(hoTen = 'Le Thi D', ngaySinh = datetime.now(), soDienThoai = '0123456786',email = 'a5@gmail.com',diaChi = '123 abc', gioiTinh = False)
    nb5 = NguoiBenh(hoTen = 'Pham Thi F', ngaySinh = datetime.now(), soDienThoai = '0123456785',email = 'qqq@asd.com',diaChi = '123 abc', gioiTinh = False)
    db.session.add(nb5)
    db.session.add(nb1)
    db.session.add(nb2)
    db.session.add(nb3)
    db.session.add(nb4)
    p1 = PhieuLichDat(ngayHen = datetime.now(),trangThai = False,nguoiBenh_id = 1, ca_id=1)
    p2 = PhieuLichDat(ngayHen = datetime(2025, 1, 12),trangThai = False,nguoiBenh_id = 2, ca_id=3)
    p3 = PhieuLichDat(ngayHen = datetime(2025, 1, 16),trangThai = False,nguoiBenh_id = 3, ca_id=5)
    p4 = PhieuLichDat(ngayHen = datetime(2025, 1, 16),trangThai = False,nguoiBenh_id = 4, ca_id=1)
    p5 = PhieuLichDat(ngayHen = datetime(2025, 1, 12),trangThai = False,nguoiBenh_id = 1, ca_id=2)
    p6 = PhieuLichDat(ngayHen = datetime(2025, 1, 15),trangThai = False,nguoiBenh_id = 2, ca_id=3)
    p7 = PhieuLichDat(ngayHen = datetime(2025, 1, 13),trangThai = False,nguoiBenh_id = 3, ca_id=4)
    p8 = PhieuLichDat(ngayHen = datetime(2025, 1, 14),trangThai = False,nguoiBenh_id = 4, ca_id=5)
    p9 = PhieuLichDat(ngayHen = datetime(2025, 1, 14),trangThai = False,nguoiBenh_id = 5, ca_id=4)
    p10 = PhieuLichDat(ngayHen = datetime(2025, 1, 12),trangThai = False,nguoiBenh_id = 5, ca_id=4)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)
    db.session.add(p6)
    db.session.add(p7)
    db.session.add(p8)
    db.session.add(p9)
    db.session.add(p10)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initUser()
        initPhieuLichDat()
        initCaLamViec()
