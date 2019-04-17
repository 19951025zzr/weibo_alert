#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from flask import jsonify

from config import mail_pass, mail_user, sender, mail_host, subject


def send_email(article, receiver_name, receiver_add):
    message = MIMEText(article, _charset='utf-8')
    message['From'] = Header("微博", 'utf-8')  # 设置显示在邮件里的发件人
    message['To'] = Header(receiver_name, 'utf-8')  # 设置显示在邮件里的收件人

    message['Subject'] = Header(subject, 'utf-8')  # 设置主题和格式

    try:
        smtpobj = smtplib.SMTP_SSL(mail_host, 465)  # 本地如果有本地服务器，则用localhost ,默认端口２５,腾讯的（端口465或587）
        smtpobj.set_debuglevel(1)
        smtpobj.login(mail_user, mail_pass)  # 登陆QQ邮箱服务器
        smtpobj.sendmail(sender, receiver_add, message.as_string())  # 发送邮件
        smtpobj.quit()  # 退出
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False

def response_json(errno, msg, result=None):
    tmp = {
        'errno': errno,
        'msg': msg
    }

    if result is not None:
        tmp['result'] = result

    response_data = jsonify(tmp)
    # 准许跨域
    response_data.headers['Access-Control-Allow-Origin'] = 'http://192.168.3.25:9500'
    response_data.headers['Access-Control-Allow-Credentials'] = 'True'
    response_data.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS,GET"

    return response_data


if __name__ == '__main__':
    send_email('我是xxx', '哈哈', 'xxxxxxxxx@qq.com')