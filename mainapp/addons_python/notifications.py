# -*- coding: utf-8 -*-

import requests
from django.core.mail import EmailMultiAlternatives

login = "admin@it-class1158.site"


# функция отправки сообщений на почту
def send_mail_to_applicant(theme_letter, header_letter, text_letter,
                           recipients_email):
    for email in recipients_email:
        html_content = f"""\
        <html>
          <head></head>
          <body>
        <img src="https://it-class1158.ru/itclass/static/images/logo_it_class-5.png"
        width="150" height="100">
            <h1 style="text-align: center;">{header_letter}</h1><br>
               <p style="font-size: 18px;">{text_letter}</p>
        <hr>
        <p style="font-size: 18px;">Если у тебя остались какие-то вопросы нажми на вкладку ниже</p>
        <a href="mailto:admin@it-class1158.site?subject=Вопрос от участника">ЗАДАТЬ ВОПРОС</a>
        </p>
          </body>
        </html>
        """
        subject, from_email, to = theme_letter, login, email
        text_content = text_letter
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_mail_to_admin(theme_letter, header_letter, text_letter,
                           recipients_email):
    for email in recipients_email:
        html_content = f"""\
        <html>
          <head></head>
          <body>
        <img src="https://it-class1158.ru/itclass/static/images/logo_it_class-5.png"
        width="150" height="100">
            <h1 style="text-align: center;">{header_letter}</h1><br>
               <p style="font-size: 18px;">{text_letter}</p>
        <hr>
        <a href="https://it-class1158.ru/check_list/">Перейти на страницу модерации</a>
        </p>
        </body>
        </html>
        """
        subject, from_email, to = theme_letter, login, email
        text_content = text_letter
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# функция отправки сообщений в телеграмм канал {"ok":true,"result":{"message_id":3,"chat":{"id":-1001380508914,"title":"\u0418\u0442-\u043a\u043b\u0430\u0441\u0441","username":"it_class1158","type":"channel"},"date":1595839792,"text":"test"}}
def send_telegram(text: str):
    token = "1098094286:AAGmN7YpguBfJOiPgXLyx-OtPW15pQ76ESU"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001380508914"
    # channel_id = -1001134619840  # тестовый канал
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")
