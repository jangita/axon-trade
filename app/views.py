from flask import request
from app import app
from os import environ
import hmac
import hashlib
import requests
import datetime
import binascii


def hmac_sha256(key, message):
    byte_key = key.encode()
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest()


@app.route("/test", methods=['GET'])
def test():
    api_key = environ['binance_api_key']
    api_secret = environ['binance_api_secret']

    headers = {'X-MBX-APIKEY': api_key}

    params = 'timestamp=' + \
        str(int(datetime.datetime.now().timestamp() * 1000))

    signature = hmac_sha256(api_secret, params)

    url = 'https://api.binance.com/api/v3/account?' + \
        params + '&signature=' + signature

    response = requests.get(url, headers=headers)
    return response.text, 200


@app.route("/a", methods=['GET'])
def a():
    api_key = environ['binance_api_key']
    api_secret = environ['binance_api_secret']

    headers = {'X-MBX-APIKEY': api_key}
    json = request.get_json()

    symbol = json['symbol']
    side = json['side']
    quantity = json['quantity']

    params = 'symbol=' + symbol + '&side=' + side + \
        '&quantity=' + quantity + '&type=MARKET&timestamp=' + \
        str(int((datetime.datetime.now() - datetime.timedelta(hours=-4)).timestamp() * 1000))

    signature = hmac_sha256(api_secret, params)

    params = params + '&signature=' + signature
    url = 'https://api.binance.com/api/v3/order/test'
    response = requests.post(url, headers=headers, data=params)
    return response.text, 200
