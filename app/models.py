from sqlalchemy import Integer,String,Float,ForeignKey,Boolean,Column,DateTime,Enum,Text
from app import app,db
from sqlalchemy.orm import relationship, mapped_column, Mapped, backref
from enum import Enum as RoleEnum
from datetime import datetime

class VaiTro(RoleEnum):
    ADMIN = 1
    BAC_SI = 2
    Y_TA = 3
    BENH_NHAN = 4
    THU_NGAN = 5

class NguoiDung(db.Model): # Có nên là abstract class
    # __abstract__ = True
    __tablename__ = 'nguoiDung'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ho = Column(String(10),nullable=False,unique = True)
    ten = Column(String(10),nullable = False)
    ngaySinh = Column(DateTime,nullable = False)
    soDienThoai = Column(String(15),nullable=True,unique = True)
    email = Column(String(50),nullable=True,unique=True)
    ghiChu = Column(String(255),nullable = True)
    taiKhoan = Column(String(50),nullable = False,unique = True)
    matKhau = Column(Text,nullable = False)
    avatar = Column(String(255),nullable = True)
    role = Column(Enum(VaiTro),nullable = False)
    phieuLichDat = relationship('PhieuLichDat',backref = 'nguoiDung',lazy = True)

    def __str__(self):
        return f"{self.ho} {self.ten}"

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
    benhNhan_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)
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

class DonThuoc(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    phieu_id = Column(Integer,ForeignKey(PhieuKhamBenh.id),nullable = False)
    thuoc_id = Column(Integer,ForeignKey(Thuoc.id),nullable = False)
    cachDung = Column(String(255),nullable = False)
    soLuong = Column(Integer,nullable = False,default = 0)

class PhieuLichDat(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ngayDat = Column(DateTime,nullable = False)
    hoTen = Column(String(50),nullable = False)
    # ????
    trangThai = Column(Boolean,nullable = False,default = False)

    nguoiDung_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

