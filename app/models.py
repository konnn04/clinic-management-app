from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, Column, DateTime, Enum, Text, Time
from app import app, db
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


class ThongTin(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ho = Column(String(10), nullable=False, unique=False)
    ten = Column(String(10), nullable=False)
    gioiTinh = Column(Boolean, nullable=False, default=True)  # True: Nam, False: Nu
    ngaySinh = Column(DateTime, nullable=False)
    soDienThoai = Column(String(15), nullable=True, unique=True)
    email = Column(String(50), nullable=True, unique=True)
    ghiChu = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ho': self.ho,
            'ten': self.ten,
            'ngaySinh': self.ngaySinh,
            'soDienThoai': self.soDienThoai,
            'email': self.email,
            'ghiChu': self.ghiChu
        }


class NguoiDung(ThongTin, UserMixin):
    __tablename__ = 'nguoiDung'
    taiKhoan = Column(String(50), nullable=False, unique=True)
    matKhau = Column(Text, nullable=False)
    avatar = Column(String(255), nullable=True)
    role = Column(Enum(VaiTro), nullable=False)

    def __str__(self):
        return f"{self.ho} {self.ten}"

    def to_dict(self):
        return {
            **super().to_dict(),
            'taiKhoan': self.taiKhoan,
            # 'matKhau': 'self.matKhau',
            'avatar': self.avatar,
            'role': self.role.name,
        }

    def check_password(self, password):
        return check_password_hash(self.matKhau, password)

    def set_password(self, password):
        self.matKhau = generate_password_hash(password)


class NguoiBenh(ThongTin):
    diaChi = Column(String(255), nullable=False)
    phieuLichDat = relationship('PhieuLichDat', backref='nguoiBenh', lazy=True)

    def getAge(self):
        return datetime.now().year - self.ngaySinh.year

    def lanCuoiGhe(self):
        return PhieuLichDat.query.filter(PhieuLichDat.nguoiBenh_id == self.id).order_by(
            PhieuLichDat.ngayHen.desc()).first().ngayHen

    def to_dict(self):
        return {
            **super().to_dict(),
            'diaChi': self.diaChi,
            # 'phieuLichDat': self.phieuLichDat,
        }


class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    value = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    nguoiQuanTri_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)


class HoaDonThanhToan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayKham = Column(DateTime, default=datetime.utcnow, nullable=False)
    tienKham = Column(Float, nullable=False, default=0.0)
    tienThuoc = Column(Float, nullable=False, default=0.0)
    tongTien = Column(Float, nullable=False, default=0.0)
    ngayLapHoaDon = Column(DateTime, default=datetime.utcnow, nullable=True)
    trangThai = Column(Boolean, nullable=False, default=False)
    # Bac Si
    phieuKham_id = Column(Integer, ForeignKey("phieuKham.id"), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ngayKham': self.ngayKham.isoformat() if self.ngayKham else None,
            'tienKham': self.tienKham,
            'tienThuoc': self.tienThuoc,
            'tongTien': self.tongTien,
            'ngayLapHoaDon': self.ngayLapHoaDon.isoformat() if self.ngayLapHoaDon else None,
            'trangThai': self.trangThai,
            'phieuKham_id': self.phieuKham_id
        }


class PhieuKhamBenh(db.Model):
    __tablename__ = 'phieuKham'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayKham = Column(DateTime, default=datetime.utcnow)
    trieuChung = Column(String(255), nullable=False)
    duDoanLoaiBenh = Column(String(255), nullable=False)
    bacSi_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    bacSi = relationship(NguoiDung, backref=backref('phieuKham', uselist=False))
    benhNhan = relationship(NguoiBenh, backref=backref('phieuKham', uselist=False))
    benhNhan_id = Column(Integer, ForeignKey(NguoiBenh.id), nullable=False)
    phieuDichVu = relationship('PhieuDichVu', backref=backref('phieuKham', uselist=False))
    hoaDonThanhToan = relationship('HoaDonThanhToan', backref=backref('phieuKham', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'ngayKham': self.ngayKham,
            'trieuChung': self.trieuChung,
            'duDoanLoaiBenh': self.duDoanLoaiBenh,
            'bacSi_id': self.bacSi_id,
            'benhNhan_id': self.benhNhan_id,
            'bacSi': self.bacSi.to_dict(),
            'benhNhan': self.benhNhan.to_dict(),
            'phieuDichVu': [dich_vu.to_dict() for dich_vu in self.phieuDichVu] if self.phieuDichVu else [],
            'hoaDonThanhToan': [hoa_don.to_dict() for hoa_don in self.hoaDonThanhToan] if self.hoaDonThanhToan else []
        }

class ChiTietDichVu(db.Model):
    phieuDichVu_id = Column(ForeignKey('phieudichvu.id'), primary_key=True)
    dichVu_id = Column(ForeignKey('loaidichvu.id'), primary_key=True)

    ketQua = Column(String(255), nullable=False)

    loaiDichVu = relationship("LoaiDichVu",  back_populates="cacPhieuDichVu")
    phieuDichVu = relationship("PhieuDichVu", back_populates="cacLoaiDichVu")


# chiTietDichVu = db.Table('chiTietDichVu',
#                          Column('phieuDichVu_id', Integer,ForeignKey('phieudichvu.id'), primary_key=True,),
#                          Column('loaiDichVu', Integer,ForeignKey('loaidichvu.id'), primary_key=True),
#                          Column('ketQua', String(255), nullable=True)
#                          )

class PhieuDichVu(db.Model):
    __tablename__ = 'phieudichvu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayLap = Column(DateTime, default=datetime.utcnow)
    ghiChu = Column(Text, nullable=True)
    phieukham_id = Column(Integer, ForeignKey("phieuKham.id"), unique=True)
    cacLoaiDichVu = relationship(ChiTietDichVu, back_populates='phieuDichVu')

    def to_dict(self):
        return {
            'id': self.id,
            'ngayLap': self.ngayLap.isoformat() if self.ngayLap else None,
            'ghiChu': self.ghiChu,
            'phieukham_id': self.phieukham_id
        }


class LoaiDichVu(db.Model):
    __tablename__ = 'loaidichvu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenDichVu = Column(String(255), nullable=False, unique=True)
    giaDichVu = Column(Float, default=0, nullable=False)
    moTa = Column(Text, nullable=True)
    cacPhieuDichVu = relationship(ChiTietDichVu, back_populates='loaiDichVu')



class DanhMucThuoc(db.Model):
    __tablename__ = 'danhMucThuoc'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ten = Column(String(100), nullable=False, unique=True)
    thuoc = relationship('Thuoc', backref='danhMucThuoc', lazy=True)


class LoHang(db.Model):
    __tablename__ = 'loHang'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayNhap = Column(DateTime, default=datetime.utcnow)
    hanSuDung = Column(DateTime, nullable=False)
    ngaySanXuat = Column(DateTime, nullable=False)
    thuoc = relationship("Thuoc", backref=backref('loHang', uselist=False))


class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ten = Column(String(100), nullable=False, unique=True)
    nhaCungCap = Column(String(100), nullable=False)
    xuatXu = Column(String(100), nullable=False)
    donVi = Column(String(100), nullable=False)
    danhMucThuoc_id = Column(Integer, ForeignKey(DanhMucThuoc.id), nullable=False)
    loHang_id = Column(Integer, ForeignKey("loHang.id"), unique=True)
    gia = Column(Float, nullable=False)

    def __str__(self):
        return self.ten


class DonThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phieu_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    cachDung = Column(String(255), nullable=False)
    soLuong = Column(Integer, nullable=False, default=0)


class PhieuLichDat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayDat = Column(DateTime, nullable=False, default=datetime.now())
    ngayHen = Column(DateTime, nullable=False)
    trangThai = Column(Boolean, nullable=False, default=False)
    caHen = Column(String(10), nullable=False)  # sang, chieu, toi
    # Nguoi benh dat lich
    nguoiBenh_id = Column(Integer, ForeignKey(NguoiBenh.id), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'ngayDat': self.ngayDat.isoformat() if isinstance(self.ngayDat, datetime) else self.ngayDat,
            'ngayHen': self.ngayHen.isoformat() if isinstance(self.ngayHen, datetime) else self.ngayHen,
            'trangThai': self.trangThai,
            'caHen': self.caHen,
            'nguoiBenh_id': self.nguoiBenh_id
        }


class CaLamViecBacSi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    bacSi_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    caSang = Column(Boolean, nullable=False, default=False)
    caChieu = Column(Boolean, nullable=False, default=False)
    caToi = Column(Boolean, nullable=False, default=False)

