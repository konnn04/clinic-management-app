import os

momo_accessKey = os.getenv("MOMO_ACCESS_KEY")
momo_secretKey = os.getenv("MOMO_SECRET_KEY")
momo_endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
momo_redirectUrl = f"{os.getenv('BASE_URL')}/staff"
momo_ipnUrl = f"{os.getenv('BASE_URL')}/payment/result/"
