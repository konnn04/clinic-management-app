let appointmentHistories = []

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
                            <span class="date-value"><strong>Ngày khám:</strong> ${appointment.ngayKham}</span>
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
        return appointment.id.toString().includes(searchTerm) ||
            appointment.ngayKham.includes(searchTerm) ||
            appointment.hoaDonThanhToan[0].tongTien.toString().includes(searchTerm);
    });

    renderAppointmentHistory(filteredAppointments);
}

function appointmentDetail(appointmentId) {
    const url = `/appointment/history/detail/${appointmentId}`;
    window.open(url, '_blank');
}
