# -*- coding: utf-8 -*-

"""
    notification
    ~~~~~~~~~~~~

    Implements notification(mail)

    :author:    Feei <feei@feei.cn>
    :homepage:  https://github.com/FeeiCN/gsil
    :license:   GPL, see LICENSE for more details.
    :copyright: Copyright (c) 2018 Feei. All rights reserved
"""
import random
import smtplib
import traceback
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import get
from .log import logger


class Notification(object):
    def __init__(self, subject, to=None):
        """
        Initialize notification class
        :param subject:
        :param to:
        """
        self.subject = subject
        if to is None:
            self.to = get('mail', 'to')
        else:
            self.to = to

    def notification(self, html):
        """
        Send notification use by mail
        :param html:
        :return:
        """
        # 随机挑选一个邮箱来发送，避免由于发送量过大导致被封
        mails = get('mail', 'mails').split(',')
        mail = random.choice(mails)
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = '{0} <{1}>'.format(mail, get('mail', 'from'))
        msg['To'] = self.to

        text = MIMEText(html, 'html', 'utf-8')
        msg.attach(text)

        try:
            s = smtplib.SMTP(get('mail', 'host'), get('mail', 'port'))
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(mail, get('mail', 'password'))
            s.sendmail(mail, self.to, msg.as_string())
            s.quit()
            return True
        except SMTPException:
            logger.critical('Send mail failed')
            traceback.print_exc()
            return False
