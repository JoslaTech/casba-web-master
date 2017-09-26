# Copyright 2017 Josla Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, flash, render_template, url_for, request, redirect,  session, jsonify
import ibm_db
import datetime
import json
from flask_socketio import SocketIO, emit
from watson_developer_cloud import ConversationV1
import urllib
import hashlib
from flask_mail import Mail, Message
import random
import string
import pandas
import ibm_db_dbi

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'casba-dinosaurs'

# Mail setup
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'casba@josla.com.ng'
app.config['MAIL_PASSWORD'] = 'casba-dinosaurs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# SocketIO
socketio = SocketIO(app, async_mode='eventlet')
thread = None

# Watson Conversation
conversation = ConversationV1(
  username="4a23fe86-b0f6-4e1c-8dab-e707c2547b8c",
  password="0qO4k0TbbBsf",
  version='2017-05-26'
)

workspace_id = '87e1fc89-276d-4acb-a691-74e6469b38db'

context = {}
last_response = ""

# DashDB
#Enter the values for you database connection
dsn_driver = "IBM DB2 ODBC DRIVER"
dsn_database = "BLUDB"
dsn_hostname = "dashdb-txn-flex-yp-lon02-71.services.eu-gb.bluemix.net"
dsn_port = "50000"
dsn_protocol = "TCPIP"
dsn_uid = "bluadmin"
dsn_pwd = "ZmFmNGYzOGZiN2Qz"

dsn = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "PROTOCOL=TCPIP;"
    "UID={3};"
    "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

conn = ibm_db.connect(dsn, "", "")
pconn = ibm_db_dbi.Connection(conn)

# Random password generator
def gen_random_string(char_set, length):
    if not hasattr(gen_random_string, "rng"):
        gen_random_string.rng = random.SystemRandom() # Create a static variable
    return ''.join([ gen_random_string.rng.choice(char_set) for _ in xrange(length) ])

password_charset = string.ascii_letters + string.digits

# User dictionary
user = {}
fundTransfer = {}

# Index page view
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'signupBVN' in request.form:
            sql = "SELECT * FROM CUSTOMER WHERE BVN = ?"
            stmt = ibm_db.prepare(conn, sql)
            param = request.form["signupBVN"],
            ibm_db.execute(stmt, param)
            if ibm_db.fetch_row(stmt) == False:
                sql = "SELECT * FROM CUSTOMER ORDER BY ID DESC fetch first 1 row only"
                stmt = ibm_db.exec_immediate(conn, sql)
                customer = 1
                while ibm_db.fetch_row(stmt) != False:
                    customer = customer + int(ibm_db.result(stmt, "ID"))
                # Save new customer info
                sql = "INSERT INTO CUSTOMER (ID, BVN, FIRSTNAME, LASTNAME, DATEOFBIRTH, PHONENUMBER, EMAIL, PASSWORD, CITY, DOC) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                stmt = ibm_db.prepare(conn, sql)
                param = customer, request.form["signupBVN"], request.form["inputFName"], request.form["inputLName"], request.form["inputDOB"], request.form["inputPhone"], request.form["inputEmail"], request.form["inputPassword"], request.form["inputLocation"], datetime.date.today(),
                ibm_db.execute(stmt, param)
                # Save security info for new customer
                sql = "INSERT INTO SECURITY (ID, BVN, SQ1, SA1, SQ2, SA2, SQ3, SA3) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                stmt = ibm_db.prepare(conn, sql)
                param = customer, request.form["signupBVN"], request.form["inputSQ1"], request.form["inputSA1"], request.form["inputSQ2"], request.form["inputSA2"], request.form["inputSQ3"], request.form["inputSA3"],
                ibm_db.execute(stmt, param)
                msg = Message('Welcome to CASBA', sender = 'casba@josla.com.ng', recipients = [str(request.form["inputEmail"])])
                msg.body = "Thank you for registering to use of Cognitive Banking (CogniBank) service. Enjoy the experience of using artifical intelligence to organise your finances."
                mail.send(msg)
                flash('You were successfully registered!')
                return redirect(url_for('index'))
            else:
                flash('You were already registered!')
                return redirect(url_for('index'))
        elif 'loginBVN' in request.form:
            sql = "SELECT * FROM CUSTOMER WHERE BVN = ?"
            stmt = ibm_db.prepare(conn, sql)
            param = request.form["loginBVN"],
            ibm_db.execute(stmt, param)
            if ibm_db.fetch_row(stmt) != False:
                # check if user credentials match
                if request.form["inputPassword"] == ibm_db.result(stmt, "PASSWORD"):
                    session['logged_in'] = True
                    user.update({'bvn': str(request.form["loginBVN"]), 'fName': str(ibm_db.result(stmt, "FIRSTNAME")), 'lName': str(ibm_db.result(stmt, "LASTNAME")), 'email': str(ibm_db.result(stmt, "EMAIL")) })
                    # sql = "SELECT * FROM ACCOUNT WHERE BVN = ?"
                    # stmt = ibm_db.prepare(conn, sql)
                    # param = request.form["loginBVN"],
                    # ibm_db.execute(stmt, param)
                    sql1 = "".join(["SELECT * FROM ACCOUNT WHERE BVN = ", str(request.form["loginBVN"])])
                    stmt1 = ibm_db.exec_immediate(conn, sql1)
                    userAccountDF = pandas.read_sql(sql1 , pconn)
                    sql2 = "".join(["SELECT * FROM CARD WHERE BVN = ", str(user['bvn'])])
                    stmt2 = ibm_db.exec_immediate(conn, sql2)
                    userCardDF = pandas.read_sql(sql2 , pconn)
                    if userAccountDF.empty:
                        user.update({'accountIn': 0})
                        if userCardDF.empty:
                            user.update({'#Card': 0})
                        return redirect(url_for('chat'))
                    else:
                        user.update({'accountIn': len(userAccountDF.index)})
                        userAccount = {}
                        for i in range(0, user["accountIn"]):
                            userAccount[i] = userAccountDF.iloc[i].tolist()
                        user.update({'Account': userAccount})
                        #print user["Account"][0][0]
                        if userCardDF.empty:
                            user.update({'#Card': 0})
                            return redirect(url_for('chat'))
                        else:
                            user.update({'#Card': len(userCardDF.index)})
                            userCard = {}
                            for i in range(0, user["#Card"]):
                                userCard[i] = userCardDF.iloc[i].tolist()
                            user.update({'Card': userCard})
                            #print user["Account"][0][0]
                            return redirect(url_for('chat'))
                else:
                    flash('Wrong credentials, please try again or create an account!')
                    return redirect(url_for('index'))
            else:
                flash('Wrong credentials, please try again or create an account!')
                return redirect(url_for('index'))
        elif 'passwordBVN' in request.form:
            sql = "SELECT * FROM SECURITY WHERE BVN = ?"
            stmt = ibm_db.prepare(conn, sql)
            param = request.form["passwordBVN"],
            ibm_db.execute(stmt, param)
            # check if security questions match
            if ibm_db.fetch_row(stmt) != False:
                if str(ibm_db.result(stmt, "SQ1")) == str(request.form["inputSQ1"]) and str(ibm_db.result(stmt, "SA1")) == str(request.form["inputSA1"]):
                    if str(ibm_db.result(stmt, "SQ2")) == str(request.form["inputSQ2"]) and str(ibm_db.result(stmt, "SA2")) == str(request.form["inputSA2"]):
                        if str(ibm_db.result(stmt, "SQ3")) == str(request.form["inputSQ3"]) and str(ibm_db.result(stmt, "SA3")) == str(request.form["inputSA3"]):
                            new_password = gen_random_string(password_charset, 6)
                            sql = "UPDATE CUSTOMER SET PASSWORD = ? WHERE BVN = ?"
                            stmt = ibm_db.prepare(conn, sql)
                            param = new_password, request.form["passwordBVN"],
                            ibm_db.execute(stmt, param)
                            sql = "SELECT * FROM CUSTOMER WHERE BVN = ?"
                            stmt = ibm_db.prepare(conn, sql)
                            param = request.form["passwordBVN"],
                            ibm_db.execute(stmt, param)
                            if ibm_db.fetch_row(stmt) != False:
                                msg = Message('Password Reset', sender = 'casba@josla.com.ng', recipients = [str(ibm_db.result(stmt, "EMAIL"))])
                                msg.body = ' '.join(["Here is your new password", new_password])
                                mail.send(msg)
                                flash('Your password has been reset! Please check your email.')
                                return redirect(url_for('index'))
                            else:
                                flash('You are not registered! Please try again or create an account.')
                                return redirect(url_for('index'))
                        else:
                            flash('Incorrect Security Question & Answer')
                            return redirect(url_for('index'))
                    else:
                        flash('Incorrect Security Question & Answer')
                        return redirect(url_for('index'))
                else:
                    flash('Incorrect Security Question & Answer')
                    return redirect(url_for('index'))
            else:
                flash('You are not a registered user! Please create an account.')
                return redirect(url_for('index'))
    else:
        return render_template('index.html')

# Chat page view
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # check if user is logged in
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        session['unique_conversation_id'] = str(user_ip) + "__" + str(user_agent)
        context["conversation_id"] = str(hashlib.sha256(session['unique_conversation_id'].encode('utf-8')).hexdigest())
        if request.method == "POST":
            if 'cardNo' in request.form:
                sql = "SELECT * FROM CARD WHERE CARDNO = ?"
                stmt = ibm_db.prepare(conn, sql)
                param = request.form["cardNo"],
                ibm_db.execute(stmt, param)
                if ibm_db.fetch_row(stmt) == False:
                    sql = "SELECT * FROM CARD ORDER BY ID DESC fetch first 1 row only"
                    stmt = ibm_db.exec_immediate(conn, sql)
                    card = 1
                    while ibm_db.fetch_row(stmt) != False:
                        card = card + int(ibm_db.result(stmt, "ID"))
                    # Save new customer card info
                    sql = "INSERT INTO CARD (ID, BVN, ACCNO, CARDNO, CARDVENDOR, CARDTYPE, CVC, EXPIRY) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    stmt = ibm_db.prepare(conn, sql)
                    param = card, user["bvn"], request.form["cardAccountNo"], request.form["cardNo"], request.form["cardVendor"], request.form["cardType"], request.form["cvc"], request.form["cardExpiry"],
                    ibm_db.execute(stmt, param)
                    msg = Message('CASBA: New Card', sender = 'casba@josla.com.ng', recipients = [str(user["email"])])
                    msg.body = "You have added a new card"
                    mail.send(msg)
                    flash('You have successfully added a card!')
                    sql2 = "".join(["SELECT * FROM CARD WHERE BVN = ", str(user['bvn'])])
                    stmt2 = ibm_db.exec_immediate(conn, sql2)
                    userCardDF = pandas.read_sql(sql2 , pconn)
                    if userCardDF.empty:
                        user.update({'#Card': 0})
                        return redirect(url_for('chat'))
                    else:
                        user.update({'#Card': len(userCardDF.index)})
                        userCard = {}
                        for i in range(0, user["#Card"]):
                            userCard[i] = userCardDF.iloc[i].tolist()
                        user.update({'Card': userCard})
                        #print user["Account"][0][0]
                        return redirect(url_for('chat'))
                    return render_template('chat.html', userJS=json.dumps(user), user=user, async_mode=socketio.async_mode)
                else:
                    flash('You have card already registered!')
                    return render_template('chat.html', userJS=json.dumps(user), user=user, async_mode=socketio.async_mode)
            elif 'accountNo' in request.form:
                sql = "SELECT * FROM ACCOUNT WHERE ACCNO = ?"
                stmt = ibm_db.prepare(conn, sql)
                param = request.form["accountNo"],
                ibm_db.execute(stmt, param)
                if ibm_db.fetch_row(stmt) == False:
                    sql = "SELECT * FROM ACCOUNT ORDER BY ID DESC fetch first 1 row only"
                    stmt = ibm_db.exec_immediate(conn, sql)
                    account = 1
                    while ibm_db.fetch_row(stmt) != False:
                        account = account + int(ibm_db.result(stmt, "ID"))
                    # Save new customer info
                    sql = "INSERT INTO ACCOUNT (ID, BVN, ACCNO, ACCBANK, ACCNAME, ACCTYPE, ACCBALANCE) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    stmt = ibm_db.prepare(conn, sql)
                    param = account, user["bvn"], request.form["accountNo"], request.form["accountBank"], request.form["accountName"], request.form["accountType"], request.form["accountBalance"],
                    ibm_db.execute(stmt, param)
                    msg = Message('CASBA: New Account', sender = 'casba@josla.com.ng', recipients = [str(user["email"])])
                    msg.body = "You have added a new account"
                    mail.send(msg)
                    flash('You were successfully setup an account!')
                    sql1 = "".join(["SELECT * FROM ACCOUNT WHERE BVN = ", str(user['bvn'])])
                    stmt1 = ibm_db.exec_immediate(conn, sql1)
                    userAccountDF = pandas.read_sql(sql1 , pconn)
                    if userAccountDF.empty:
                        user.update({'accountIn': 0})
                        return redirect(url_for('chat'))
                    else:
                        user.update({'accountIn': len(userAccountDF.index)})
                        userAccount = {}
                        for i in range(0, user["accountIn"]):
                            userAccount[i] = userAccountDF.iloc[i].tolist()
                        user.update({'Account': userAccount})
                        #print user["Account"][0][0]
                        return redirect(url_for('chat'))
                    return render_template('chat.html', userJS=json.dumps(user), user=user, async_mode=socketio.async_mode)
                else:
                    flash('You have account already registered!')
                    return render_template('chat.html', userJS=json.dumps(user), user=user, async_mode=socketio.async_mode)
            else:
                flash('Unsuccessful account setup!')
                return render_template('chat.html', userJS=json.dumps(user), user=user, async_mode=socketio.async_mode)
        else:
            return render_template('chat.html', userJS=json.dumps(user), user=user, async_mode=socketio.async_mode)

# Log out control
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')

# Websocket
@socketio.on('my event')
def handleMessage(message):
    from_human_message = str(message["data"])
    global context
    global response

    bot_response = "...."
    intent = "...."
    entity = "...."
    entity_value = "...."
    try:
        context["conversation_id"] = str(hashlib.sha256(session['unique_conversation_id'].encode('utf-8')).hexdigest())
        response = conversation.message(workspace_id=workspace_id, message_input={'text': urllib.unquote(from_human_message)}, context=context)
        context = response["context"]
        print context

        if len(json.loads(json.dumps(response, indent=2))['intents']) > 0:
            intent = json.loads(json.dumps(response, indent=2))['intents'][0]['intent']
            if intent == "hello":
                if len(json.loads(json.dumps(response, indent=2))['entities']) > 0:
                    entity = json.loads(json.dumps(response, indent=2))['entities'][0]['entity']
                    if entity == "bank":
                        entity_value = json.loads(json.dumps(response, indent=2))['entities'][0]['value']
                        try:
                            bot_response = ' '.join(response["output"]["text"]).replace(entity_value, "Kenneth")
                        except Exception as ex:
                            print("exception :( ", ex)
                    elif entity == "sys-number":
                        entity_value = json.loads(json.dumps(response, indent=2))['entities'][0]['value']
                        if 'destination_bank' in json.loads(json.dumps(response, indent=2))['context']:
                            try:
                                bot_response = ' '.join(response["output"]["text"]).replace(str(json.loads(json.dumps(response, indent=2))['context']['destination_bank']), "Kenneth")
                            except Exception as ex:
                                print("exception :( ", ex)
                        else:
                            try:
                                bot_response = ' '.join(response["output"]["text"])
                                bot_response = bot_response.replace(entity_value, "Kenneth")
                            except Exception as ex:
                                print("exception :( ", ex)
                    else:
                        try:
                            bot_response = ' '.join(response["output"]["text"])
                        except Exception as ex:
                            print("exception :( ", ex)
                else:
                    try:
                        bot_response = ' '.join(response["output"]["text"])
                    except Exception as ex:
                        print("exception :( ", ex)
            elif intent == "capabilities":
                try:
                    bot_response = ' '.join(response["output"]["text"])
                except Exception as ex:
                    print("exception :( ", ex)
            elif intent == "fund_transfer":
                try:
                    bot_response = ' '.join(response["output"]["text"])
                except Exception as ex:
                    print("exception :( ", ex)
            else:
                try:
                    bot_response = ' '.join(response["output"]["text"])
                except Exception as ex:
                    print("exception :( ", ex)
        else:
            try:
                bot_response = ' '.join(response["output"]["text"])
            except Exception as ex:
                print("exception :( ", ex)


    except Exception as ex:
        print("watson exception :( ", ex)

    print("\n\nBOT SAYS: " + json.dumps(response))

    # sometimes the fucking bot doesn't answer what it should.
    if len(bot_response) < 2:
        bot_response = "I couldn't understand that. You can type 'help' for example"

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': bot_response, 'intent': intent, 'entity': entity, 'entity_value': entity_value, 'user': user, 'count': session['receive_count']})

# Server
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	#app.run(host='0.0.0.0', port=int(port))
    socketio.run(app, host='0.0.0.0', port=int(port), debug=True)
