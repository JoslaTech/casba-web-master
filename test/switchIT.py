import os
import time
from flask import Flask, request
import hashlib
import requests
from xml.etree.ElementTree import Element, SubElement, tostring

app = Flask(__name__)


@app.route('/')
def index():
    destination = "2001220212"
    endpoint = "A"
    pin = "0012"
    bankCode = "033"
    amount = "1000"
    currency = "NGN"
    reference = ''.join(["JE", str(time.time()), "switchIT"])

    fundTransferAccount = Element('fundTransferAccount')
    destination = SubElement(fundTransferAccount, 'destination')
    destination.text = "2001220212"
    endpoint = SubElement(fundTransferAccount, 'endpoint')
    endpoint.text = "A"
    pin = SubElement(fundTransferAccount, 'pin')
    pin.text = "0012"
    bankCode = SubElement(fundTransferAccount, 'bankCode')
    bankCode.text = "033"
    amount = SubElement(fundTransferAccount, 'amount')
    amount.text = "1000"
    currency = SubElement(fundTransferAccount, 'currency')
    currency.text = "NGN"
    reference = SubElement(fundTransferAccount, 'reference')
    reference.text = ''.join(["JE", str(time.time()), "switchIT"])

    # print tostring(fundTransferAccount)
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    response = requests.post("https://staging.etranzact.com/FundGatePlus/doc.wsdl", data=fundTransferAccount,  )
    print response.content
    return '<h1>Hello World!</h1>'

port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))
