function validateInput(info) {

    const phoneRegex = /^[0-9]{9,11}$/;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (phoneRegex.test(info) || emailRegex.test(info)) {
        return true;
    }

    return false;
}

function sendOtp() {
    const info = document.getElementById('info').value;

    if (!info) {
        alert('Vui lòng nhập email/số điện thoai trước khi lấy OTP!');
        return;
    }
    if (validateInput(info)) {
        fetch('/send-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({info}),
        })
            .then(async (response) => {
                if (response.ok) {
                    alert('OTP đã được gửi đến email/SĐT của bạn!');
                } else if (response.status === 401) {
                    window.location.href = '/register'
                } else if (response.status === 500) {
                    msg = await response.json()
                    showToast("Lỗi", `Có lỗi xảy ra khi gửi OTP. Vui lòng thử lại! <br> ${msg.message}`, "error", 5000)
                }
            })
            .catch(error => {
                alert('Có lỗi xảy ra: ' + error.message);
            });
    } else {
        alert("Vui lòng nhập số điện thoại hoặc email hợp lệ!");
    }


}