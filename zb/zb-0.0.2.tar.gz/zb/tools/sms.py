# -*- coding: utf-8 -*-
"""
Send Message Service
====================================================================
"""

import requests
from retrying import retry
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@retry(stop_max_attempt_number=6)
def server_chan_push(title, content, key=None):
    """使用server酱推送消息到微信，关于server酱，
    请参考：http://sc.ftqq.com/3.version

    :param title: str
        消息标题
    :param content: str
        消息内容，最长64Kb，可空，支持MarkDown
    :param key: str
        从[Server酱](https://sc.ftqq.com/3.version)获取的key
    :return: None
    """
    if not key:
        raise ValueError("请配置key，如果还没有key，"
                         "可以到这里申请一个：http://sc.ftqq.com/3.version")
    url = 'https://sc.ftqq.com/%s.send' % key
    requests.post(url, data={'text': title, 'desp': content})


@retry(stop_max_attempt_number=6)
def bear_push(title, content, send_key=None):
    """使用PushBear推送消息给所有订阅者微信，关于PushBear，
    请参考：https://pushbear.ftqq.com/admin/#/

    :param title: str
        消息标题
    :param content: str
        消息内容，最长64Kb，可空，支持MarkDown
    :param send_key: str
        从[PushBear](https://pushbear.ftqq.com/admin/#/)获取的通道send_key
    :return: None
    """
    if not send_key:
        raise ValueError("请配置通道send_key，如果还没有，"
                         "可以到这里创建通道获取：https://pushbear.ftqq.com/admin/#/")
    api = "https://pushbear.ftqq.com/sub"
    requests.post(api, data={'text': title, 'desp': content, "sendkey": send_key})


# 邮件发送器，支持发送附件。
# --------------------------------------------------------------------

class EmailSender:
    def __init__(self, from_, pw, service='qq'):
        self.from_ = from_  # 用于发送email的邮箱
        self.pw = pw  # 发送email的邮箱密码
        self.smtp = smtplib.SMTP()
        if service == 'qq':
            self.smtp.connect('smtp.exmail.qq.com')
            self.smtp.login(self.from_, self.pw)
        elif service == '163':
            self.smtp.connect('smtp.163.com')
            self.smtp.login(self.from_, self.pw)
        else:
            print('目前仅支持163和qq邮箱！')

    def _construct_msg(self, to, subject, content, files=None):
        """构造email信息

        parameters
        ---------------
        subject     邮件主题
        content     邮件文本内容
        files       附件（list）
                    可以是相对路径下的文件，也可以是绝对路径下的文件；
                    推荐使用绝对路径。

        return
        --------------
        msg         构造好的邮件信息
        """
        msg = MIMEMultipart()
        msg['from'] = self.from_
        msg['to'] = to
        msg['subject'] = subject
        txt = MIMEText(content)
        msg.attach(txt)

        # 添加附件
        if files is not None:
            for file in files:
                f = MIMEApplication(open(file, 'rb').read())
                f.add_header('Content-Disposition', 'attachment',
                             filename=os.path.split(file)[-1])
                msg.attach(f)

        return msg

    @retry(stop_max_attempt_number=6)
    def send_email(self, to, subject, content, files=None):
        """登录邮箱，发送msg到指定联系人

        :param to: str: 收件人邮箱
        :param subject: str: 主题
        :param content: str: 内容
        :param files:  list: 附件列表
        :return: None
        """
        smtp = self.smtp
        msg = EmailSender._construct_msg(self, to, subject, content, files=files)
        smtp.sendmail(self.from_, to, str(msg))

    def quit(self):
        smtp = self.smtp
        smtp.quit()  # 退出登录
