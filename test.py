from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com
account_sid = "ACc0b77c83e0937c028a84c3045071d53b"
auth_token  = "29e3e43d78cfee2e89cb0d06cae84a6e"
verify_sid = "VA7f2edaccf04ee1eb2fd679c57d0a1c37"

verified_number = "0772816986"

client = Client(account_sid, auth_token)

# verification = client.verify.v2.services(verify_sid) \
#   .verifications \
#   .create(to=verified_number, channel="sms")
# print(verification.status)

# otp_code = input("Please enter the OTP:")

# verification_check = client.verify.v2.services(verify_sid) \
#   .verification_checks \
#   .create(to=verified_number, code=otp_code)
# print(verification_check.status)
verification = client.verify.v2.services(
    "VAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
).verifications.create(to="+84772816986", channel="sms",locale="vi")

print(verification.status)