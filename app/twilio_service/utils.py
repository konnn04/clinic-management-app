from twilio.rest import Client

from app.twilio_service import account_SID, auth_toKen

def send_sms_otp(to, message=None):
    # Biến to là số dạng +84....
    account_sid = account_SID
    auth_token = auth_toKen
    service_id = "VA18177827d6c27261e647bd725fa4dbb0"

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(service_id).verifications.create(to=to, channel="sms")

    print(verification)


def verify_sms_otp(to,otp):
    account_sid = account_SID
    auth_token = auth_toKen
    service_id = "VA18177827d6c27261e647bd725fa4dbb0"

    client = Client(account_sid, auth_token)
    verification_checks = client.verify.v2.services(service_id).verification_checks.create(to=to, code=otp)
    return verification_checks.status

# send_sms_otp(to="+84344778045")
verify_sms_otp(to="+84344778045", otp=6354)
