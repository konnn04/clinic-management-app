let appointmentHistories = []

async function getAppointmentHistoryDetail() {
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
        console.log(data)

        if (data.appointment_histories) {
            appointmentHistories = data.appointment_histories // Store the fetched appointment histories
            console.log('Lịch sử khám bệnh:', appointmentHistories)
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
        container.innerHTML = '<p>Không có đơn khám bệnh nào.</p>';
    } else {
        appointments.forEach(appointment => {
            const appointmentElement = document.createElement('div');
            appointmentElement.classList.add('appointment-item');
            appointmentElement.innerHTML = `
                        <div class="info">
                            <span class="id-value"><strong>Mã khám bệnh:</strong> #${appointment.id}</span>
                            <span class="date-value"><strong>Ngày khám:</strong> ${appointment.date}</span>
                            <span class="total-value"><strong>Tổng tiền:</strong> ${appointment.total} VNĐ</span>
                        </div>
                        <button class="details-button" onclick="openAppointmentDetail(${appointment.id})">Xem chi tiết</button>
                    `;
            container.appendChild(appointmentElement);
        });
    }
}

function filterAppointments() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const filteredAppointments = appointmentHistories.filter(appointment => {
        return appointment.id.toString().includes(searchTerm) ||
            appointment.date.includes(searchTerm) ||
            appointment.total.includes(searchTerm);
    });

    renderAppointmentHistory(filteredAppointments);
}

function openAppointmentDetail(appointmentId) {
    const url = `/api/appointment/history/detail/${appointmentId}`;
    window.open(url, '_blank');
}
