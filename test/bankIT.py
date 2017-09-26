import os
import time
from flask import Flask, request
import hashlib
import requests

app = Flask(__name__)


@app.route('/')
def index():
    transId = ''.join(["JE", str(time.time()), "bankIT"])
    print transId

    terminalId = "0000000001"

    amount = 1000

    responseURL = request.base_url
    print responseURL

    description = "Payment Description"

    secret_key = "DEMO_KEY"

    checksumString = ''.join([str(amount), terminalId, transId, responseURL, secret_key])
    print checksumString
    checksum = hashlib.sha256(checksumString).hexdigest()
    print checksum

    response = requests.post("http://demo.etranzact.com/bankIT/", data={'TERMINAL_ID': terminalId, 'TRANSACTION_ID': transId, 'AMOUNT': amount, 'DESCRIPTION': description, 'RESPONSE_URL': responseURL, 'CHECKSUM': checksum})
    return response.content
    #return '<h1>Hello World!</h1>'

port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))
