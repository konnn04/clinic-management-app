from sqlalchemy import Integer,String,Float,ForeignKey,Boolean,Column,DateTime,Enum,Text
from hospitalapp import app,db
from sqlalchemy.orm import relationship, mapped_column, Mapped, backref
from enum import Enum as E, unique
from datetime import datetime

class Role(E):
    ADMIN = 1
    BAC_SI = 2
    Y_TA = 3
    BENH_NHAN = 4

class NguoiDung(db.Model): # Có nên là abstract class
    # __abstract__ = True
    __tablename__ = 'nguoiDung'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ho = Column(String(10),nullable=False)
    ten = Column(String(10),nullable = False)
    soDienThoai = Column(String(15),nullable=False)
    ghiChu = Column(String(255),nullable = True)
    taiKhoan = Column(String(50))
    password = Column(Text)
    avatar = Column(String(255),nullable = True)
    role = Column(Enum(Role),nullable = False)
    bangCap = Column(String(255), nullable=True)

    hoaDonThanhToan = relationship('HoaDonThanhToan',backref = 'nguoiDung',lazy = True)
    phieuLichDat = relationship('PhieuLichDat',backref = 'nguoiDung',lazy = True)

    def __str__(self):
        return f"{self.ho} {self.ten}"

    def check_password(self,password):
        return True

class QuyDinh(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    value = Column(Integer,nullable = False)
    description = Column(String(255),nullable = False)
    nguoiQuanTri_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)

class HoaDonThanhToan(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ngayKham = Column(DateTime,default = datetime.utcnow)
    tienKham = Column(Float,nullable = False,default = 0.0)
    tienThuoc = Column(Float,nullable = False,default = 0.0)
    tongTien = Column(Float,nullable = False,default = 0.0)
    ngayLapHoaDon = Column(DateTime,default = datetime.utcnow)
    trangThai = Column(Boolean,nullable = False,default = False)
    # Bac Si
    nguoiDung_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)

phieuKham_DichVu = db.Table('phieuKham_DichVu',
                            Column('phieuKham_id',Integer,
                            ForeignKey('phieuKham.id'),
                            primary_key = True),
                            Column('dichVu_id',Integer,
                            ForeignKey('dichVu.id'),
                            primary_key = True))

class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieuKham'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ngayKham = Column(DateTime,default = datetime.utcnow)
    trieuChung = Column(String(255),nullable = False)
    duDoanLoaiBenh = Column(String(255))
    bacSi_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)
    benhNhan_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)
    dichvu = relationship('DichVuKham',
                          secondary='phieuKham_DichVu',
                          lazy = 'subquery',
                          backref=backref('phieuKham',lazy = True))

class DichVuKham(db.Model):
    __tablename__ = 'dichVu'
    id = Column(Integer,primary_key = True,autoincrement=True)
    tenDichVu = Column(String(100),nullable = False)
    moTa = Column(String(255),nullable = True)
    phi = Column(Float,nullable = False,default = 0.0)

class DanhMucThuoc(db.Model):
    __tablename__ = 'danhMucThuoc'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    ten = Column(String(100),nullable = False)
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
    ten = Column(String(100), nullable=False)
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

    # ????
    trangThai = Column(Boolean,nullable = False,default = False)

    nguoiDung_id = Column(Integer,ForeignKey(NguoiDung.id),nullable = False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


