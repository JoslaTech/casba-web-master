import os
import time
from flask import Flask, request
import hashlib
import requests
import json
from random import randint

app = Flask(__name__)


@app.route('/')
def index():
    # Initialize Payment
    clientid = "testSystem"
    action = "initialize"
    n = 32
    #sessionid = ''.join(["%s" % randint(0, 9) for num in range(0, n)])
    sessionid = "1562767627273877826782"
    print sessionid
    terminalid = "0000000001"
    #transactionid = ''.join(["", str(round(time.time()*1000))])
    transactionid ="123456789"
    print transactionid
    bank = "011"
    accountnumber = "2061718186"
    #serviceid = ''.join(["", str(time.time()*1000)])
    serviceid ="AC76374"
    amount = "3000"
    description = "TestPayment"
    merchantcode = "652435374"
    clientKey = "1234567890qwertyuiopasdfghjklzxcvbnmm1n2b3g4f5y6k7j8g9s0g1a2g3h4yk5"
    #macString = ''.join([sessionid, clientid, terminalid, transactionid, accountnumber, bank, serviceid, amount, description, merchantcode, clientKey])
    macString = sessionid+clientid+terminalid+transactionid+accountnumber+bank+serviceid+amount+description+merchantcode+clientKey
    #mac = hashlib.sha256(macString.encode("UTF-8")).hexdigest()
    mac = "edf3b05f3eb8c43a4745ea83817efdb56958ac8c7af904e2de491da4f3905d7b"
    print mac


    paymentInit=   {"clientid":clientid ,
                "action": action,
                "sessionid": sessionid,
                "mac": mac,
                "terminalid": terminalid,
                "transactionid": transactionid,
                "bank": bank,
                "accountnumber ": accountnumber,
                "serviceid": serviceid,
                "amount": amount,
                "description": description,
                "merchantcode": merchantcode}




    # transId = ''.join(["JE", str(time.time()), "bankIT"])
    # print transId
    #
    # terminalId = "0000000001"
    #
    # amount = 1000
    #
    # responseURL = request.base_url
    # print responseURL
    #
    # description = "Payment Description"
    #
    # secret_key = "DEMO_KEY"
    #
    # checksumString = ''.join([str(amount), terminalId, transId, responseURL, secret_key])
    # print checksumString
    # checksum = hashlib.sha256(checksumString).hexdigest()
    # print checksum


    print json.dumps(paymentInit)
    response = requests.post(''.join(["https://demo.etranzact.com/bankIT/service_bankitapi?json=", json.dumps(paymentInit)]))

    print response.json()

    # Send account details
    clientid = "testSystem"
    action = "newaccountinfo"
    requestid = "763546364734"
    sessionid = "156276762767273877826782"
    mac = "62836281927362bdbxgs8hsb276"
    firstname = "Sogo"
    lastname = "John"
    emailaddress = "sogo.john@gmail.com"
    passCode = "123456"

    sendAccount = {"clientid": clientid,
                   "action": action,
                   "terminalid": terminalid,
                   "transactionid": transactionid,
                   "bank": bank,
                   "accountnumber ": accountnumber,
                   "serviceid": serviceid,
                   "amount": amount,
                   "description": description,
                   "merchantcode": merchantcode}


    return '<h1>Hello World!</h1>'

port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))
