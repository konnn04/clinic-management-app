let appointmentHistories = []

document.addEventListener('DOMContentLoaded', () => {
    const args = new URLSearchParams(window.location.search);
    const msg = args.get('success');
    if (msg) {
        showToast('Thông báo', "Đã đặt lịch thành công!", 'success', 5000);
    }
    getAppointmentHistory()
    getAppointmentList()
})

async function getAppointmentHistory() {
    try {
        const response = await fetch('/api/appointment/history', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        if (!response.ok) {
            throw new Error('Fetch error')
        }
        const data = await response.json()
        // console.log(data)
        if (data) {
            appointmentHistories = data // Store the fetched appointment histories
            // console.log('Lịch sử khám bệnh:', appointmentHistories)
            renderAppointmentHistory(appointmentHistories)
        } else {
            console.error('Không tìm thấy lịch sử khám bệnh!')
        }
    } catch (error) {
        console.error('Lỗi khi gọi API:', error.message)
        alert('Không thể lấy lịch sử khám bệnh. Vui lòng thử lại sau!')
    }
}

function renderAppointmentHistory(appointments) {
    const container = document.getElementById('appointment-history');
    container.innerHTML = '';

    if (appointments.length === 0) {
        container.innerHTML = '<p>Bạn không có đơn khám bệnh nào.</p>';
    } else {
        appointments.forEach(appointment => {
            const appointmentElement = document.createElement('div');
            appointmentElement.classList.add('appointment-item');
            console.log(appointment)
            const tongTien = new Intl.NumberFormat('vi-VN').format(appointment.hoaDonThanhToan.tongTien);
            appointmentElement.innerHTML = `
                        <div class="info">
                            <span class="id-value"><strong>Mã khám bệnh:</strong> #${appointment.id}</span>
<!--                            <span class="date-value"><strong>Ngày khám:</strong> ${appointment.ngayKham}</span>-->
                            <span class="total-value"><strong>Tổng tiền:</strong> ${tongTien} VNĐ</span>
                        </div>
                        <div style=" display: flex; flex-direction: column; align-items: center">
                            <div class=${appointment.hoaDonThanhToan.trangThai == true ? "text-success" : "text-danger"} id="payment">${appointment.hoaDonThanhToan.trangThai == true ? "Đã thanh toán" : "Chưa thanh toán"}</div>
                            <button class="details-button" onclick="appointmentDetail(${appointment.id})">Xem chi tiết</button>
                        </div>
                    `;
            container.appendChild(appointmentElement);
        });
    }
}

function filterAppointments() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const filteredAppointments = appointmentHistories.filter(appointment => {
        console.log(appointment.hoaDonThanhToan)
        return appointment.id.toString().includes(searchTerm) ||
            // appointment.ngayKham.includes(searchTerm) ||
            appointment.hoaDonThanhToan.tongTien.toString().includes(searchTerm);
    });

    renderAppointmentHistory(filteredAppointments);
}

function appointmentDetail(appointmentId) {
    const url = `/appointment/history/detail/${appointmentId}`;
    window.open(url, '_blank');
}

async function getAppointmentList() {
    try {
        const response = await fetch(`/api/patient/get-appointment-list`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        if (!response.ok) {
            showToast('Thông báo', 'Lỗi khi lấy danh sách lịch khám bệnh!', 'error', 5000)
            throw new Error('Fetch error')
        }

        const data = await response.json()
        // console.log(data)
        $("#appointment-list").empty()
        if (data.length == 0) {
            $("#appointment-list").append(`
                <p class="text-center p-3">Bạn không có lịch hẹn nào</p>
            `)
            return
        }

        
        data.forEach(appointment => {
            $("#appointment-list").append(`
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <div class="fw-bold">Mã hẹn: ${appointment.id}</div>
                            <div>Ngày hẹn: ${appointment.ngayHen}</div>
                            <div>Ca hẹn: ${appointment.caHen}</div>
                            <div>Trạng thái: ${appointment.trangThai} </div>
                        </div>
                        ${appointment.coTheHuy == true ? `<button class="btn btn-danger" onclick="cancelAppointment(${appointment.id})">Hủy</button>` : ''}
                    </li>
                `)
        })
    } catch (error) {
        console.error('Lỗi khi gọi API:', error.message)
        // alert('Không thể lấy thông tin chi tiết lịch khám bệnh. Vui lòng thử lại sau!')
        showToast('Thông báo', 'Không thể lấy thông tin chi tiết lịch khám bệnh. Vui lòng thử lại sau!', 'error', 5000)
    }
}

async function cancelAppointment(lichKham_id) {
    try {
        const response = await fetch(`/api/cancel-appointment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                lichKham_id: lichKham_id
            })
        })

        if (!response.ok) {
            showToast('Thông báo', 'Lỗi khi hủy lịch khám bệnh!', 'error', 5000)
            throw new Error('Fetch error')
        }

        const data = await response.json()
        if (data['status'] == 'success') {
            showToast('Thông báo', 'Hủy lịch khám bệnh thành công!', 'success', 5000)
            getAppointmentList()
        } else {
            showToast('Thông báo', 'Hủy lịch khám bệnh thất bại!', 'error', 5000)
        }

    } catch (error) {
        console.error('Lỗi khi gọi API:', error.message)
        showToast('Thông báo', 'Không thể hủy lịch khám bệnh. Vui lòng thử lại sau!', 'error', 5000)
    }
}
