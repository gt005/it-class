# -*- coding: utf-8 -*-
"""Send email via smtp_host."""

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

smtp_host = "mail.hosting.reg.ru"
login = "admin@it-class1158.site"
password = "wsx123451"

# функция отправки сообщений на почту
def send_mail_to_applicant(theme_letter, header_letter, text_letter, recipients_email):
    for email in recipients_email:
        html = f"""\
        <html>
          <head></head>
          <body>
        <img src="https://it-class1158.site/static/images/itclass-logo.png" width="150" height="150">
            <h1 style="text-align: center;">{header_letter}</h1><br>
               <p style="font-size: 18px;">{text_letter}</p>
        <hr>
        <p style="font-size: 18px;">Если у тебя остались какие-то вопросы нажми на вкладку ниже</p>
        <a href="mailto:admin@it-class1158.site?subject=Вопрос от участника">ЗАДАТЬ ВОПРОС</a>
        </p>
          </body>
        </html>
        """
        msg = MIMEMultipart()
        msg['Subject'] = Header(f"{theme_letter}", 'utf-8')
        msg['From'] = login
        msg['To'] = email
        part = MIMEText(html, 'html')
        msg.attach(part)
        s = smtplib.SMTP(smtp_host, 587)
        s.set_debuglevel(1)
        try:
            s.starttls()
            s.login(login, password)
            s.sendmail(login, recipients_email, msg.as_string())
        finally:
            print(msg)
            s.quit()

# функция отправки сообщений в телеграмм канал {"ok":true,"result":{"message_id":3,"chat":{"id":-1001380508914,"title":"\u0418\u0442-\u043a\u043b\u0430\u0441\u0441","username":"it_class1158","type":"channel"},"date":1595839792,"text":"test"}}
def send_telegram(text: str):
    token = "1098094286:AAEAKeTsr0GDh8LlxW_M0O2zQhPMy_wW1tg"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001380508914"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")
