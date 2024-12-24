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
        showToast("Lỗi", "Vui lòng nhập số điện thoại hoặc email!", "error", 5000)
        $("#getOtpButton").prop('disabled', false);
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
                    showToast("Thành công", "Mã OTP đã được gửi đến số điện thoại hoặc email của bạn!", "success", 5000)
                    let countdown = 60;
                    const interval = setInterval(() => {
                        if (countdown > 0) {
                            $("#getOtpButton").text(`Vui lòng chờ ${countdown--} giây`);
                        } else {
                            clearInterval(interval);
                            $("#getOtpButton").prop('disabled', false).text('Gửi OTP');
                        }
                    }, 1000);
                } else if (response.status === 401) {
                    window.location.href = '/register?need-register=true';
                } else if (response.status === 500) {
                    msg = await response.json()
                    $("#getOtpButton").prop('disabled', false);
                    showToast("Lỗi", `Có lỗi xảy ra khi gửi OTP. Vui lòng thử lại! <br> ${msg.message}`, "error", 5000)
                }
            })
            .catch(error => {
                $("#getOtpButton").prop('disabled', false);
                showToast("Lỗi", "Có lỗi xảy ra khi gửi OTP. Vui lòng thử lại!<br>" + error, "error", 5000)
            });
    } else {
        $("#getOtpButton").prop('disabled', false);
        showToast("Lỗi", "Số điện thoại hoặc email không hợp lệ!", "error", 5000)
    }
}

$("#getOtpButton").click(function () {
    $(this).prop('disabled', true);
    sendOtp();
    // setTimeout(() => {
    //     $(this).prop('disabled', false);
    // }, 3000);
});