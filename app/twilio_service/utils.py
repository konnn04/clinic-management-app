from flask import jsonify
from twilio.rest import Client

from app.twilio_service import account_SID, auth_toKen

def send_sms_otp(to, message=None):
    # Biến to là số dạng +84....
    try:
        account_sid = account_SID
        auth_token = auth_toKen
        service_id = "VA18177827d6c27261e647bd725fa4dbb0"

        client = Client(account_sid, auth_token)

        verification = client.verify.v2.services(service_id).verifications.create(to=to, channel="sms")

        return jsonify({
            "status": "success" if verification.status.__eq__("approved") else "failed",
            "message": "Da gui OTP"
        }), 200
    except Exception as ex:
        return jsonify({
            "status": "failed",
            "message": ex.msg
        }), 500


def verify_sms_otp(to,otp):
    try:
        account_sid = account_SID
        auth_token = auth_toKen
        service_id = "VA18177827d6c27261e647bd725fa4dbb0"

        client = Client(account_sid, auth_token)
        verification_checks = client.verify.v2.services(service_id).verification_checks.create(to=to, code=otp)
        print("Check in run")
        print(verification_checks.status)
        return {
            "status": "verified" if verification_checks.status.__eq__("approved") else "failed",
            "message": verification_checks
        }
    except Exception as ex:
        return {
            "status": "failed",
            "message": ex.msg
        }


