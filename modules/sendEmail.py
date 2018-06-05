# coding: utf-8

import smtplib
import baseinfo
import time
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText


def send_Mail(testReport, result):

    f = open(testReport, 'rb')
    # 读取测试报告正文
    mail_body = f.read()
    f.close()
    try:
        smtp = smtplib.SMTP(baseinfo.mail_server, 25)
        sender = baseinfo.mail_sender
        password = baseinfo.mail_password
        receiver = baseinfo.mail_receiver
        smtp.login(sender, password)
        msg = MIMEMultipart()
        text = MIMEText(mail_body, 'html', 'utf-8')
        text['Subject'] = Header('App自动化测试报告', 'utf-8')
        msg.attach(text)

        currentTime = time.strftime('%Y-%m-%d %H:%M:%S')
        msg['Subject'] = Header('[App自动化执行结果：'+result+']'+' 执行时间：'+currentTime, 'utf-8')
        msg_file = MIMEText(mail_body, 'html', 'utf-8')
        msg_file['Content-Type'] = 'application/octet-stream'
        msg_file['Content-Description'] = 'attachment; filename="testReport%s.html"' % currentTime
        msg.attach(msg_file)
        msg['From'] = sender
        msg['To'] = ','.join(receiver)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        return True
    except smtplib.SMTPException as e:
        print str(e)
        return False
