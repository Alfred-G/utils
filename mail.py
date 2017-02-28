# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:38:00 2017

@author: Alfred
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr


class Mail():
    """
    1
    """

    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.server = smtplib.SMTP(host, timeout=30)

    def send(self, to, title, txt, file_path):
        """
        1
        """

        msg = MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = formataddr(parseaddr(' <%s>' % self.user))
        msg["To"] = ','.join(to)

        text = MIMEText(txt)
        msg.attach(text)

        if file_path:
            attach = MIMEApplication(open(file_path, 'rb').read())
            attach.add_header(
                'Content-Disposition', 'attachment',
                filename=os.path.basename(file_path)
            )
            msg.attach(attach)

        self.server.login(self.user, self.password)
        self.server.sendmail(self.user, to, msg.as_string())
        self.server.close()
