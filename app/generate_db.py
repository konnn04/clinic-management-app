from app import app, db
from app.models import NguoiDung, VaiTro, NguoiBenh, PhieuLichDat, PhieuKhamBenh, PhieuDichVu, LoaiDichVu, ChiTietDichVu, DanhMucThuoc, Thuoc, LoHang, DonThuoc, HoaDonThanhToan, CaLamViecBacSi

from werkzeug.security import generate_password_hash
from datetime import datetime


def initUser():
    ad = NguoiDung(ho='admin', ten='admin', ngaySinh=datetime.now(), soDienThoai='0123456789', email='admin@admin.com',
                   taiKhoan='admin', matKhau=generate_password_hash('admin'), role=VaiTro.ADMIN)
    bs = NguoiDung(
        ho='Nguyen',
        ten='Van A',
        ngaySinh=datetime(1999, 1, 1),
        soDienThoai='012345434789',
        email='a@a.com',
        taiKhoan='doctor1',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.BAC_SI)

    bs2 = NguoiDung(
        ho='Le',
        ten='Van K',
        ngaySinh=datetime(1999, 10, 12),
        soDienThoai='012345431189',
        email='aaa@a.com',
        taiKhoan='doctor2',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.BAC_SI)

    yt = NguoiDung(
        ho='Nguyen',
        ten='Van B',
        ngaySinh=datetime.now(),
        soDienThoai='012345456744',
        email='b@b.com',
        taiKhoan='nurse1',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.Y_TA)
    c = NguoiDung(
        ho='Nguyen',
        ten='Van C',
        ngaySinh=datetime.now(),
        soDienThoai='012312256789',
        email='c@c.com',
        taiKhoan='cashier1',
        matKhau=generate_password_hash('1212'),
        role=VaiTro.THU_NGAN)

    caBS1 = CaLamViecBacSi(bacSi_id=1, caSang=True)
    caBS2 = CaLamViecBacSi(bacSi_id=2, caChieu=True)

    db.session.add(ad)
    db.session.add(bs)
    db.session.add(bs2)
    db.session.add(yt)
    db.session.add(c)
    db.session.add(caBS1)
    db.session.add(caBS2)
    db.session.commit()


def initNguoiBenh():
    nb1 = NguoiBenh(ho='Nguyen Van', ten='A', ngaySinh=datetime.now(), soDienThoai='0123456789', email='a@gmail.com',
                    diaChi='123 abc')
    nb2 = NguoiBenh(ho='Nguyen Van', ten='B', ngaySinh=datetime.now(), soDienThoai='0123456788', email='a2@gmail.com',
                    diaChi='123 abc')
    nb3 = NguoiBenh(ho='Nguyen Van', ten='C', ngaySinh=datetime.now(), soDienThoai='0123456787', email='a3@gmail.com',
                    diaChi='123 abc')
    nb4 = NguoiBenh(ho='Le Thi', ten='D', ngaySinh=datetime.now(), soDienThoai='0123456786', email='a5@gmail.com',
                    diaChi='123 abc', gioiTinh=False)
    nb5 = NguoiBenh(ho='Pham Thi', ten='E', ngaySinh=datetime.now(), soDienThoai='0123456785', email='qqq@asd.com',
                    diaChi='123 abc', gioiTinh=False)
    db.session.add(nb5)
    db.session.add(nb1)
    db.session.add(nb2)
    db.session.add(nb3)
    db.session.add(nb4)


def initPhieuLichDat():
    p1 = PhieuLichDat(ngayHen=datetime.now(), trangThai=False, benhNhan_id=1, caHen='sang')
    p2 = PhieuLichDat(ngayHen=datetime(2025, 1, 12), trangThai=False, benhNhan_id=2, caHen='chieu')
    p3 = PhieuLichDat(ngayHen=datetime(2025, 1, 16), trangThai=False, benhNhan_id=3, caHen='sang')
    p4 = PhieuLichDat(ngayHen=datetime(2025, 1, 16), trangThai=False, benhNhan_id=4, caHen='chieu')
    p5 = PhieuLichDat(ngayHen=datetime(2025, 1, 12), trangThai=False, benhNhan_id=1, caHen='chieu')
    p6 = PhieuLichDat(ngayHen=datetime(2025, 1, 15), trangThai=False, benhNhan_id=2, caHen='chieu')
    p7 = PhieuLichDat(ngayHen=datetime(2025, 1, 13), trangThai=False, benhNhan_id=3, caHen='sang')
    p8 = PhieuLichDat(ngayHen=datetime(2025, 1, 14), trangThai=False, benhNhan_id=4, caHen='chieu')
    p9 = PhieuLichDat(ngayHen=datetime(2025, 1, 14), trangThai=False, benhNhan_id=5, caHen='sang')
    p10 = PhieuLichDat(ngayHen=datetime(2025, 1, 12), trangThai=False, benhNhan_id=5, caHen='chieu')
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


def initPhieuKhamBenh():
    pk1 = PhieuKhamBenh(
        ngayKham=datetime.now(),
        trieuChung="Ho, sốt, đau đầu",
        duDoanLoaiBenh="Cảm cúm",
        bacSi_id=1,
        benhNhan_id=1
    )

    pk2 = PhieuKhamBenh(
        ngayKham=datetime(2024, 12, 20),
        trieuChung="Đau bụng, buồn nôn",
        duDoanLoaiBenh="Rối loạn tiêu hóa",
        bacSi_id=2,
        benhNhan_id=1
    )

    pk3 = PhieuKhamBenh(
        ngayKham=datetime(2024, 12, 18),
        trieuChung="Khó thở, đau ngực",
        duDoanLoaiBenh="Hen suyễn",
        bacSi_id=1,
        benhNhan_id=1
    )

    pk4 = PhieuKhamBenh(
        ngayKham=datetime(2024, 12, 15),
        trieuChung="Sốt cao, mệt mỏi",
        duDoanLoaiBenh="Sốt xuất huyết",
        bacSi_id=2,
        benhNhan_id=1
    )

    pk5 = PhieuKhamBenh(
        ngayKham=datetime(2024, 12, 10),
        trieuChung="Đau răng, sưng nướu",
        duDoanLoaiBenh="Viêm lợi",
        bacSi_id=1,
        benhNhan_id=1
    )

    db.session.add(pk1)
    db.session.add(pk2)
    db.session.add(pk3)
    db.session.add(pk4)
    db.session.add(pk5)
    db.session.commit()


def initPhieuDichVu_LoaiDichVu_ChiTietDichVu():
    # Dữ liệu mẫu
    dv1 = LoaiDichVu(tenDichVu="Dịch vụ sửa chữa", giaDichVu=150000, moTa="Dịch vụ 1")
    dv2 = LoaiDichVu(tenDichVu="Dịch vụ bảo trì", giaDichVu=50000, moTa="Dịch vụ 2")
    dv3 = LoaiDichVu(tenDichVu="Dịch vụ tư vấn", giaDichVu=200000, moTa="Dịch vụ 3")
    dv4 = LoaiDichVu(tenDichVu="Dịch vụ vệ sinh", giaDichVu=30000, moTa="Dịch vụ 4")

    db.session.add_all([dv1, dv2, dv3, dv4])
    db.session.commit()

    #

    pk1 = PhieuKhamBenh.query.get(1)
    pk2 = PhieuKhamBenh.query.get(2)

    pdv1 = PhieuDichVu(phieukham_id=pk1.id, ghiChu="Kiểm tra huyết áp và xét nghiệm máu")
    pdv2 = PhieuDichVu(phieukham_id=pk2.id, ghiChu="X-ray và kiểm tra chức năng gan")

    db.session.add(pdv1)
    db.session.add(pdv2)
    db.session.commit()

    pdv1.cacLoaiDichVu.append(ChiTietDichVu(ketQua="KQ1", loaiDichVu=dv1))
    pdv1.cacLoaiDichVu.append(ChiTietDichVu(ketQua="KQ2", loaiDichVu=dv2))

    pdv2.cacLoaiDichVu.append(ChiTietDichVu(ketQua="KQ3", loaiDichVu=dv1))


def initDMThuoc_LoHang_Thuoc():
    dm1 = DanhMucThuoc(ten="Thuốc giảm đau")
    dm2 = DanhMucThuoc(ten="Thuốc kháng sinh")
    dm3 = DanhMucThuoc(ten="Thuốc trị cảm cúm")
    dm4 = DanhMucThuoc(ten="Thuốc trị ho")
    dm5 = DanhMucThuoc(ten="Thuốc chống dị ứng")

    db.session.add(dm1)
    db.session.add(dm2)
    db.session.add(dm3)
    db.session.add(dm4)
    db.session.add(dm5)

    db.session.commit()

    thuoc1 = Thuoc(
        ten="Paracetamol",
        nhaCungCap="Công ty Dược phẩm ABC",
        xuatXu="Việt Nam",
        donVi="Viên",
        danhMucThuoc_id=1,  # Thuộc danh mục 'Thuốc giảm đau'
        gia=20000
    )

    thuoc2 = Thuoc(
        ten="Amoxicillin",
        nhaCungCap="Công ty Dược phẩm XYZ",
        xuatXu="Pháp",
        donVi="Viên",
        danhMucThuoc_id=2,  # Thuộc danh mục 'Thuốc kháng sinh'
        gia=50000
    )

    thuoc3 = Thuoc(
        ten="Acetaminophen",
        nhaCungCap="Công ty Dược phẩm DEF",
        xuatXu="Hoa Kỳ",
        donVi="Chai",
        danhMucThuoc_id=3,  # Thuộc danh mục 'Thuốc trị cảm cúm'
        gia=15000
    )

    thuoc4 = Thuoc(
        ten="Cough Syrup",
        nhaCungCap="Công ty Dược phẩm JKL",
        xuatXu="Anh",
        donVi="Chai",
        danhMucThuoc_id=4,  # Thuộc danh mục 'Thuốc trị ho'
        gia=30000
    )

    thuoc5 = Thuoc(
        ten="Cetirizine",
        nhaCungCap="Công ty Dược phẩm MNO",
        xuatXu="Đức",
        donVi="Viên",
        danhMucThuoc_id=5,  # Thuộc danh mục 'Thuốc chống dị ứng'
        gia=25000
    )

    # Thêm các đối tượng vào phiên làm việc
    db.session.add(thuoc1)
    db.session.add(thuoc2)
    db.session.add(thuoc3)
    db.session.add(thuoc4)
    db.session.add(thuoc5)

    # Lưu vào cơ sở dữ liệu
    db.session.commit()
    
    lohang1 = LoHang(
        ngayNhap=datetime(2024, 12, 1),
        hanSuDung=datetime(2025, 12, 1),
        ngaySanXuat=datetime(2024, 6, 1),
        soLuong=100,
        thuoc_id=1  # Liên kết với thuốc có id=1 (Paracetamol)
    )

    lohang2 = LoHang(
        ngayNhap=datetime(2024, 12, 5),
        hanSuDung=datetime(2025, 11, 30),
        ngaySanXuat=datetime(2024, 5, 30),
        soLuong=100,
        thuoc_id=2  # Liên kết với thuốc có id=2 (Amoxicillin)

    )

    lohang3 = LoHang(
        ngayNhap=datetime(2024, 12, 10),
        hanSuDung=datetime(2026, 1, 1),
        ngaySanXuat=datetime(2024, 7, 1),
        soLuong=100,
        thuoc_id=3  # Liên kết với thuốc có id=3 (Acetamin
    )

    lohang4 = LoHang(
        ngayNhap=datetime(2024, 12, 15),
        hanSuDung=datetime(2025, 12, 15),
        ngaySanXuat=datetime(2024, 8, 15),
        soLuong=100,
        thuoc_id=4  # Liên kết với thuốc có id=4 (Cough Sy
    )

    lohang5 = LoHang(
        ngayNhap=datetime(2024, 12, 20),
        hanSuDung=datetime(2026, 6, 20),
        ngaySanXuat=datetime(2024, 9, 20),
        soLuong=100,
        thuoc_id=5  # Liên kết với thuốc có id=5 (Cetirizine
    )
    lohang6 = LoHang(
        ngayNhap=datetime(2024, 12, 25),
        hanSuDung=datetime(2026, 6, 25),
        ngaySanXuat=datetime(2024, 10, 1),
        soLuong=100,
        thuoc_id=1  # Liên kết với thuốc có id=1 (Paracetamol)
    )

    lohang7 = LoHang(
        ngayNhap=datetime(2024, 12, 30),
        hanSuDung=datetime(2026, 7, 1),
        ngaySanXuat=datetime(2024, 11, 1),
        soLuong=100,
        thuoc_id=2  # Liên kết với thuốc có id=2 (Amoxicillin)
    )

    lohang8 = LoHang(
        ngayNhap=datetime(2025, 1, 5),
        hanSuDung=datetime(2026, 8, 1),
        ngaySanXuat=datetime(2024, 12, 1),
        soLuong=100,
        thuoc_id=3  # Liên kết với thuốc có id=3 (Acetaminophen)
    )

    lohang9 = LoHang(
        ngayNhap=datetime(2025, 1, 10),
        hanSuDung=datetime(2026, 9, 1),
        ngaySanXuat=datetime(2025, 1, 1),
        soLuong=100,
        thuoc_id=4  # Liên kết với thuốc có id=4 (Cough Syrup)
    )

    lohang10 = LoHang(
        ngayNhap=datetime(2025, 1, 15),
        hanSuDung=datetime(2026, 10, 1),
        ngaySanXuat=datetime(2025, 2, 1),
        soLuong=100,
        thuoc_id=5  # Liên kết với thuốc có id=5 (Cetirizine)
    )



    # Thêm dữ liệu vào phiên làm việc
    db.session.add_all([lohang1, lohang2, lohang3, lohang4, lohang5, lohang6, lohang7, lohang8, lohang9, lohang10])

    # Lưu các thay đổi vào cơ sở dữ liệu
    db.session.commit()

    


def initDonThuoc():
    # Tạo đơn thuốc mẫu
    don_thuoc1 = DonThuoc(
        phieu_id=1,  # Giả sử phiếu khám bệnh có id=1
        thuoc_id=1,  # Giả sử thuốc có id=1 (Paracetamol)
        cachDung="Uống 2 viên sau bữa ăn sáng và tối",
        soLuong=10
    )

    don_thuoc2 = DonThuoc(
        phieu_id=1,  # Cùng phiếu khám bệnh id=1
        thuoc_id=2,  # Thuốc có id=2 (Amoxicillin)
        cachDung="Uống 1 viên mỗi 8 giờ",
        soLuong=15
    )

    don_thuoc3 = DonThuoc(
        phieu_id=2,  # Phiếu khám bệnh id=2
        thuoc_id=3,  # Thuốc có id=3 (Acetaminophen)
        cachDung="Uống 1 viên mỗi 6 giờ",
        soLuong=12
    )

    don_thuoc4 = DonThuoc(
        phieu_id=3,  # Phiếu khám bệnh id=3
        thuoc_id=4,  # Thuốc có id=4 (Cough Syrup)
        cachDung="Uống 2 muỗng sau mỗi bữa ăn",
        soLuong=3
    )

    don_thuoc5 = DonThuoc(
        phieu_id=4,  # Phiếu khám bệnh id=4
        thuoc_id=5,  # Thuốc có id=5 (Cetirizine)
        cachDung="Uống 1 viên trước khi ngủ",
        soLuong=7
    )

    # Thêm các bản ghi vào phiên làm việc
    db.session.add(don_thuoc1)
    db.session.add(don_thuoc2)
    db.session.add(don_thuoc3)
    db.session.add(don_thuoc4)
    db.session.add(don_thuoc5)

    # Lưu các thay đổi vào cơ sở dữ liệu
    db.session.commit()


def initHoaDonThanhToan():
    # Tạo các hóa đơn mẫu
    hoa_don1 = HoaDonThanhToan(
        ngayKham=datetime(2024, 12, 20),
        tienKham=50000.0,
        tienThuoc=150000.0,
        tongTien=200000.0,  # Tổng tiền = tiền khám + tiền thuốc
        ngayLapHoaDon=datetime(2024, 12, 21),
        trangThai=True,
        phieuKham_id=1  # Liên kết với phiếu khám bệnh có id=1
    )

    hoa_don2 = HoaDonThanhToan(
        ngayKham=datetime(2024, 12, 18),
        tienKham=60000.0,
        tienThuoc=120000.0,
        tongTien=180000.0,
        ngayLapHoaDon=datetime(2024, 12, 19),
        trangThai=True,
        phieuKham_id=2  # Liên kết với phiếu khám bệnh có id=2
    )

    hoa_don3 = HoaDonThanhToan(
        ngayKham=datetime(2024, 12, 15),
        tienKham=70000.0,
        tienThuoc=180000.0,
        tongTien=250000.0,
        ngayLapHoaDon=datetime(2024, 12, 16),
        trangThai=True,
        phieuKham_id=3  # Liên kết với phiếu khám bệnh có id=3
    )

    hoa_don4 = HoaDonThanhToan(
        ngayKham=datetime(2024, 12, 10),
        tienKham=80000.0,
        tienThuoc=100000.0,
        tongTien=180000.0,
        ngayLapHoaDon=datetime(2024, 12, 11),
        trangThai=True,
        phieuKham_id=4  # Liên kết với phiếu khám bệnh có id=4
    )

    hoa_don5 = HoaDonThanhToan(
        ngayKham=datetime(2024, 12, 5),
        tienKham=55000.0,
        tienThuoc=90000.0,
        tongTien=145000.0,
        ngayLapHoaDon=datetime(2024, 12, 6),
        trangThai=True,
        phieuKham_id=5  # Liên kết với phiếu khám bệnh có id=5
    )

    # Thêm các hóa đơn vào phiên làm việc
    db.session.add(hoa_don1)
    db.session.add(hoa_don2)
    db.session.add(hoa_don3)
    db.session.add(hoa_don4)
    db.session.add(hoa_don5)

    # Lưu các thay đổi vào cơ sở dữ liệu
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initUser()
        initNguoiBenh()
        initPhieuLichDat()
        initPhieuKhamBenh()
        initPhieuDichVu_LoaiDichVu_ChiTietDichVu()
        initDMThuoc_LoHang_Thuoc()
        initDonThuoc()
        initHoaDonThanhToan()
