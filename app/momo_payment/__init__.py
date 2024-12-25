import os

momo_accessKey = os.getenv("MOMO_ACCESS_KEY")
momo_secretKey = os.getenv("MOMO_SECRET_KEY")
momo_endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
momo_redirectUrl = "https://fa5a-2405-4802-9041-bb40-19ba-a2b-ba26-5306.ngrok-free.app/staff"
momo_ipnUrl = "https://fa5a-2405-4802-9041-bb40-19ba-a2b-ba26-5306.ngrok-free.app/payment/result/"
