import os
import shutil
import git
import pep8
import email
import email.mime.application
from contextlib import redirect_stdout
import io
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

all_name_func = ['TrafficLights',
                 'Button',
                 'Balance',
                 'OddEvenSeparator',
                ]

directory = settings.MEDIA_ROOT + '/checked_work/'

def checker(link_git, name_student, e_mail):
    git.Repo.clone_from(link_git, settings.MEDIA_ROOT + '/checked_work/')
    smtp_host = "mail.hosting.reg.ru"
    login = "admin@it-class1158.site"
    password = "wsx123451"


    def send_mail_to_applicant(result, recipients_emails):
        html = f"""\
        <html>
          <head></head>
          <body>
        <img src="https://it-class1158.ru/itclass/static/images/itclass-logo1.png" width="150" height="150">
               <p style="font-size: 18px;">{result}</p>
          </body>
    
        </html>
        """
        msg = MIMEMultipart()
        msg['Subject'] = Header('Результаты провеки ДЗ', 'utf-8')
        msg['From'] = login
        msg['To'] = recipients_emails
        part = MIMEText(html, 'html')
        msg.attach(part)

        if recipients_emails == 'ibkov@yandex.ru':
            for file in all_name_func:
                try:
                    filename = directory + file + '.py'
                    fp = open(filename, 'rb')
                    att = email.mime.application.MIMEApplication(fp.read(), _subtype="py")
                    fp.close()
                    att.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(att)
                except:
                    pass

        s = smtplib.SMTP(smtp_host, 587)
        s.set_debuglevel(1)
        try:
            s.starttls()
            s.login(login, password)
            s.sendmail(login, recipients_emails, msg.as_string())
        finally:
            print("Letter send to address: " + recipients_emails + '\n\n\n')
            s.quit()


    class MyException(Exception):
        pass


    try:
        from media.checked_work.TrafficLights import TrafficLights
    except:
        print("1.IMPORT FAILED")
    try:
        from media.checked_work.Button import Button
    except:
        print("2.IMPORT FAILED")
    try:
        from media.checked_work.Balance import Balance
    except:
        print("3.IMPORT FAILED")
    try:
        from media.checked_work.OddEvenSeparator import OddEvenSeparator
    except:
        print("3.IMPORT FAILED")

    list_errors = []
    end_score = 0
    global_errors = 0

    # -------------------------test01--------------------------
    try:
        file_name = all_name_func[0]
        print("\033[32m1. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif 'class' not in text:
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            bell = TrafficLights()
            bell.red_light()
            bell.red_light()
            bell.red_light()
        s = f.getvalue()
        if s != "red\nred\nred\n":
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            bell = TrafficLights()
            bell.red_light()
            bell.red_light()
        s = f.getvalue()
        if s != "red\nred\n":
            raise MyException

        list_errors.append("1. OK")
        print("---------------------TEST-01-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-01-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"1. KO ___{file_name}___")

    # -------------------------test02--------------------------
    try:
        file_name = all_name_func[1]
        print("\033[32m2. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif 'class' not in text:
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            button = Button()
            button.click()
            button.click()
            print(button.click_count())
            button.click()
            print(button.click_count())
        s = f.getvalue()
        if s != "2\n3\n":
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            button = Button()
            button.click()
            button.click()
            print(button.click_count())
            button.reset()
            button.click()
            print(button.click_count())
        s = f.getvalue()
        if s != "2\n1\n":
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            button = Button()
            button.click()
            print(button.click_count())
            print(button.click_count())
            print(button.click_count())
            print(button.click_count())
        s = f.getvalue()
        if s != "1\n1\n1\n1\n":
            raise MyException

        list_errors.append("2. OK")
        print("---------------------TEST-02-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-02-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"2. KO ___{file_name}___")

    # -------------------------test03--------------------------
    try:
        file_name = all_name_func[2]
        print("\033[32m3. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif 'class' not in text:
            raise MyException
        balance = Balance()
        balance.add_right(10)
        balance.add_left(9)
        balance.add_left(2)
        if balance.result() != "L":
            raise MyException
        balance = Balance()
        balance.add_right(10)
        balance.add_left(5)
        balance.add_left(5)
        if balance.result() != "=":
            raise MyException
        balance.add_left(1)
        if balance.result() != "L":
            raise MyException
        balance = Balance()
        balance.add_right(999)
        balance.add_left(111)
        balance.add_left(5)
        if balance.result() != "R":
            raise MyException
        balance.add_left(888)
        if balance.result() != "L":
            raise MyException
        list_errors.append("3. OK")
        print("---------------------TEST-03-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-03-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"3. KO ___{file_name}___")

    # -------------------------test04--------------------------
    try:
        file_name = all_name_func[3]
        print("\033[32m4. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif 'class' not in text:
            raise MyException
        separator = OddEvenSeparator()
        separator.add_number(1)
        separator.add_number(5)
        separator.add_number(6)
        separator.add_number(8)
        separator.add_number(3)
        separator.even()
        separator.odd()
        if separator.even() != [6, 8]:
            raise MyException
        if separator.odd() != [1, 5, 3]:
            raise MyException
        separator.add_number(6)
        if separator.even() != [6, 8, 6]:
            raise MyException
        list_errors.append("4. OK")
        print("---------------------TEST-04-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-04-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"4. KO ___{file_name}___")

    print()
    for i in list_errors:
        if i[-2:] == 'OK':
            print(f'\033[32m{i}', end=" ")
        else:
            print(f'\033[31m{i}', end=" ")

    for i in list_errors:
        if i[-2:] == 'OK':
            end_score += 1
        else:
            break
    print("\n\n")
    print(f"\033[33mFinal score for work: {end_score * 10}")

    for i in range(len(list_errors)):
        if "KO" in list_errors[i]:
            list_errors[i] = "<font color=\"#fa8e47\">" + list_errors[i] + "</font>"
        elif "OK" in list_errors[i]:
            list_errors[i] = "<font color=\"#32CD32\">" + list_errors[i] + "</font>"
    list_errors = "<br>" + "<br>".join(list_errors)

    send_mail_to_applicant(f"Имя ученика: {name_student}<br>{link_git}<br>Список ошибок: {list_errors} <br><br>Итоговый балл: {end_score * 10}",
                               "ibkov@yandex.ru")

    try:
        # file = open(directory + "email.txt")
        # e_mail = file.read()
        send_mail_to_applicant(f"Список ошибок: {list_errors} <br><br>Итоговый балл: {end_score * 10}", e_mail)
    except:
        print("No file to feedback")

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), settings.MEDIA_ROOT + '/checked_work/')
    shutil.rmtree(path)
