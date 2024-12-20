function sendOtp() {
    const info = document.getElementById('info').value;

    if (!info) {
        alert('Vui lòng nhập email/số điện thoai trước khi lấy OTP!');
        return;
    }

    fetch('/send-otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({info}),
    })
        .then(response => {
            if (response.ok) {
                alert('OTP đã được gửi đến email của bạn!');
            }

            else if(response.status === 401){
                window.location.href = '/register'
            }

            else {
                alert('Có lỗi xảy ra khi gửi OTP. Vui lòng thử lại!');
            }
        })
        .catch(error => {
            alert('Có lỗi xảy ra: ' + error.message);
        });
}