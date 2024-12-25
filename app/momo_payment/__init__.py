import os

momo_accessKey = os.getenv("MOMO_ACCESS_KEY")
momo_secretKey = os.getenv("MOMO_SECRET_KEY")
momo_endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"

# Nếu 2 dòng này không hoạt động thì thay trực tiếp domain của web vào
# momo_redirectUrl = f"{os.getenv("MOMO_SECRET_KEY")}/staff"
# momo_ipnUrl = f"{os.getenv("MOMO_SECRET_KEY")}/payment/result/"

momo_redirectUrl = f"https://eff2-2405-4802-9041-bb40-f54a-660a-5e3e-7e60.ngrok-free.app/staff"
momo_ipnUrl = f"https://eff2-2405-4802-9041-bb40-f54a-660a-5e3e-7e60.ngrok-free.app/payment/result/"