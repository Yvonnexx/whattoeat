from flask import jsonify, request
from datetime import datetime
from email.mime.text import MIMEText
from ordering import app

import smtplib

RECEIVER = 'yvonne_xiao@symantec.com'
SENDER = 'yvonne_xiao@symantec.com'
SUBJECT = 'Incoming order from {fname} {lname}'
CONTENT = ('Order details:\n\tUser name: {fname} {lname}\n'
           '\tEmail: {email}\n\tPick Up Time: {employeeid}\n'
           '\tOffice No.: {officeno}\n'
           '\tOrder:\n{menu}\n\tUser instruction: {msg}\n'
           '\tOrder time: {time}')


@app.route('/order', methods=['POST'])
def process_order():
    incoming = request.form
    fname, lname, email, employeeid, officeno, msg, menu = '', '', '', '', '', '', ''
    for key, value in incoming.iteritems(multi=True):
        if key == 'fname':
            fname = value
        elif key == 'lname':
            lname = value
        elif key == 'email':
            email = value
        elif key == 'employeeid':
            employeeid = value
        elif key == 'officeno':
            officeno = value
        elif key == 'msg':
            msg = value
        elif key == 'menu':
            menu += '\t\t' + value + '\n'

    subject = SUBJECT.format(
        fname=fname,
        lname=lname,
    )
    content = CONTENT.format(
        fname=fname,
        lname=lname,
        email=email,
        employeeid=employeeid,
        officeno=officeno,
        menu=menu,
        msg=msg,
        time=datetime.now(),
    )

    # Prepare the email
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECEIVER

    # The actual mail send
    server = smtplib.SMTP('exsp-zone.relay.symantec.com:25')
    server.sendmail(SENDER, RECEIVER, msg.as_string())
    server.quit()
    str = "Thanks for your order!"+"\n"+"Your order has been received!"
    return str
