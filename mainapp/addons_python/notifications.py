# -*- coding: utf-8 -*-
"""Send email via smtp_host."""

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


# функция отправки сообщений на почту
def send_mail_to_applicant(theme_letter, header_letter, text_letter, recipients_email):
    pass


# функция отправки сообщений в телеграмм канал {"ok":true,"result":{"message_id":3,"chat":{"id":-1001380508914,"title":"\u0418\u0442-\u043a\u043b\u0430\u0441\u0441","username":"it_class1158","type":"channel"},"date":1595839792,"text":"test"}}
def send_telegram(text: str):
    pass
