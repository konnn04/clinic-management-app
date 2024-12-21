from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, Column, DateTime, Enum, Text, Time
from app import db, app
from sqlalchemy.orm import relationship, mapped_column, Mapped, backref
from enum import Enum as RoleEnum
from datetime import datetime, time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashids import Hashids


class VaiTro(RoleEnum):
    ADMIN = 1, "Admin"
    BAC_SI = 2, "Bác sĩ"
    Y_TA = 3, "Y tá"
    BENH_NHAN = 4, "Bệnh nhân"
    THU_NGAN = 5, "Thu ngân"
    


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

    def hoTen(self):
        return f"{self.ho} {self.ten}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'ho': self.ho,
            'ten': self.ten,
            'gioiTinh': self.gioiTinh,
            'ngaySinh': self.ngaySinh,
            'soDienThoai': self.soDienThoai,
            'email': self.email,
            'ghiChu': self.ghiChu,
        }

class NguoiDung(ThongTin, UserMixin): 
    __tablename__ = 'nguoiDung'  
    taiKhoan = Column(String(50),nullable = False,unique = True)
    matKhau = Column(Text,nullable = False)
    avatar = Column(String(255),nullable = True, default = '/static/images/user.png')
    role = Column(Enum(VaiTro),nullable = False)
    
    def __str__(self):
        return f"{self.ho} {self.ten}"

    def to_dict(self):
        return {
            'id': self.id,
            'ho': self.ho,
            'ten': self.ten,
            'gioiTinh': self.gioiTinh,
            'ngaySinh': self.ngaySinh,
            'soDienThoai': self.soDienThoai,
            'email': self.email,
            'ghiChu': self.ghiChu,
        }
    
    def check_password(self, password):
        return check_password_hash(self.matKhau, password)

    def set_password(self, password):
        self.matKhau = generate_password_hash(password)





class NguoiBenh(ThongTin):
    diaChi = Column(String(255), nullable=False)
    phieuLichDat = relationship('PhieuLichDat', backref='nguoiBenh', lazy=True)
    phieuKhamBenh = relationship('PhieuKhamBenh',backref = 'nguoiBenh',lazy = True)

    def getAge(self):
        return datetime.now().year - self.ngaySinh.year

    def lanCuoiGhe(self):
        p = PhieuKhamBenh.query.filter(PhieuKhamBenh.benhNhan_id == self.id).order_by(PhieuKhamBenh.ngayKham.desc()).first()
        if p:
            return p.ngayKham
        return None


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
    benhNhan_id = Column(Integer, ForeignKey(NguoiBenh.id), nullable=False)
    tienKham = Column(Float, nullable=False, default=0.0)
    tienThuoc = Column(Float, nullable=False, default=0.0)
    tongTien = Column(Float, nullable=False, default=0.0)
    ngayLapHoaDon = Column(DateTime, default=datetime.utcnow, nullable=True)
    trangThai = Column(Boolean, nullable=False, default=False)
    # Bac Si
    phieuKham_id = Column(Integer, ForeignKey("phieuKham.id"), unique=True)
    payUrl = Column(String(255), nullable=True)

    @property
    def hashed_id(self):
        # hash order id
        return Hashids(min_length=5, salt=app.secret_key).encode(self.id)

    @classmethod
    def decode_hashed_id(self, hashed_id):
        # decoded hashed_id -> order id
        decoded = Hashids(min_length=5, salt=app.secret_key).decode(hashed_id)
        return decoded[0] if decoded else None
    def to_dict(self, include_phieu_kham=False):
        return {
            'id': self.id,
            'ngayKham': self.ngayKham.isoformat() if self.ngayKham else None,
            'tienKham': self.tienKham,
            'tienThuoc': self.tienThuoc,
            'tongTien': self.tongTien,
            'ngayLapHoaDon': self.ngayLapHoaDon.isoformat() if self.ngayLapHoaDon else None,
            'trangThai': self.trangThai,
            'phieuKham_id': self.phieuKham_id,
            'phieuKham': self.phieuKham.to_dict(include_hoa_don=False) if include_phieu_kham and self.phieuKham else None
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

class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ten = Column(String(100), nullable=False, unique=True)
    nhaCungCap = Column(String(100), nullable=False)
    xuatXu = Column(String(100), nullable=False)
    donVi = Column(String(100), nullable=False)
    danhMucThuoc_id = Column(Integer, ForeignKey(DanhMucThuoc.id), nullable=False)
    loHang = relationship('LoHang',backref='thuoc',lazy=True)
    gia = Column(Float, nullable=False)

    def __str__(self):
        return self.ten


class LoHang(db.Model):
    __tablename__ = 'loHang'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayNhap = Column(DateTime, default=datetime.now())
    hanSuDung = Column(DateTime, nullable=False)
    ngaySanXuat = Column(DateTime, nullable=False)
    soLuong = Column(Integer,nullable=False)
    thuoc_id = Column(Integer,ForeignKey(Thuoc.id))


class PhieuLichDat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ngayDat = Column(DateTime, nullable=False, default=datetime.now())
    ngayHen = Column(DateTime, nullable=False)
    trangThai = Column(Boolean, nullable=False, default=False)
    caHen = Column(String(10), nullable=False)  # sang, chieu, toi
    hoanThanh = Column(Boolean, nullable=False, default=False)
    # Nguoi benh dat lich
    benhNhan_id= Column(Integer, ForeignKey(NguoiBenh.id), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'ngayDat': self.ngayDat.isoformat() if isinstance(self.ngayDat, datetime) else self.ngayDat,
            'ngayHen': self.ngayHen.isoformat() if isinstance(self.ngayHen, datetime) else self.ngayHen,
            'trangThai': self.trangThai,
            'caHen': self.caHen,
            'benhNhan_id': self.benhNhan_id
        }

class DonThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phieu_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    cachDung = Column(String(255), nullable=False)
    soLuong = Column(Integer, nullable=False, default=0)

class CaLamViecBacSi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    bacSi_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    caSang = Column(Boolean, nullable=False, default=False)
    caChieu = Column(Boolean, nullable=False, default=False)
    caToi = Column(Boolean, nullable=False, default=False)

