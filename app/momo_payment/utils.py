import json
import urllib.request
import urllib
import uuid
import base64
import requests
import hmac
import hashlib

from app.models import HoaDonThanhToan
from app.momo_payment import *


def create_confirm_signature(hoa_don: HoaDonThanhToan, response):
    accessKey = momo_accessKey
    secretKey = momo_secretKey

    amount = response.get('amount')
    extraData = response.get('extraData')
    message = response.get('message')
    requestId = response.get('requestId')
    orderId = response.get('orderId')
    orderInfo = response.get('orderInfo')
    orderType = response.get('orderType')
    partnerCode = response.get('partnerCode')
    payType = response.get('payType')
    responseTime = response.get('responseTime')
    transId = response.get('transId')
    resultCode = response.get('resultCode')

    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&message={message}&orderId={orderId}&orderInfo={orderInfo}&orderType={orderType}&partnerCode={partnerCode}&payType={payType}&requestId={requestId}&responseTime={responseTime}&resultCode={resultCode}&transId={transId}"

    h = hmac.new(bytes(secretKey, 'utf-8'), bytes(rawSignature, 'utf-8'), hashlib.sha256)
    signature = h.hexdigest()
    return signature


def create_request_data(hoa_don: HoaDonThanhToan, extra_data: str = ""):
    accessKey = momo_accessKey
    secretKey = momo_secretKey

    redirectUrl = momo_redirectUrl
    ipnUrl = momo_ipnUrl + hoa_don.hashed_id

    partnerCode = "MOMO"
    orderInfo = "pay with MoMo"

    amount = str(round(hoa_don.tongTien))
    orderId = hoa_don.hashed_id

    requestId = hoa_don.hashed_id

    requestType = "captureWallet"
    extra_data = extra_data.encode("ascii")
    extraData = base64.b64encode(extra_data)
    extraData = extraData.decode("ascii")

    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()

    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    data = json.dumps(data)
    return data


def post_request(data):
    endpoint = momo_endpoint
    clen = len(data)
    response = requests.post(endpoint, data=data,
                             headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})
    return response
