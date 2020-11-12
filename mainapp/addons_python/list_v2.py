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

all_name_func = ['ft_strtlist',
                 'ft_join',
                 'ft_rmstrspc',
                 'ft_rmstrchar',
                 'ft_sumlst',
                 'ft_sum_even_lst',
                 'ft_sum_even_part_lst',
                 'ft_odd_even_separator_lst',
                 'ft_pos_neg_separator_lst',
                 'ft_odd_even_analysis_lst',
                 'ft_pos_neg_analysis_lst'
                 ]

directory = settings.MEDIA_ROOT + '/checked_work/'

def checker_list_v1(link_git, student_name, e_mail):
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
        from media.checked_work import ft_strtlist
    except:
        print("1.IMPORT FAILED")
    try:
        from media.checked_work import ft_join
    except:
        print("2.IMPORT FAILED")
    try:
        from media.checked_work import ft_rmstrspc
    except:
        print("3.IMPORT FAILED")
    try:
        from media.checked_work import ft_rmstrchar
    except:
        print("4.IMPORT FAILED")
    try:
        from media.checked_work import ft_sumlst
    except:
        print("5.IMPORT FAILED")
    try:
        from media.checked_work import ft_sum_even_lst
    except:
        print("6.IMPORT FAILED")
    try:
        from media.checked_work import ft_sum_even_part_lst
    except:
        print("7.IMPORT FAILED")
    try:
        from media.checked_work import ft_odd_even_separator_lst
    except:
        print("8.IMPORT FAILED")
    try:
        from media.checked_work import ft_pos_neg_separator_lst
    except:
        print("9.IMPORT FAILED")
    try:
        from media.checked_work import ft_odd_even_analysis_lst
    except:
        print("10.IMPORT FAILED")
    try:
        from media.checked_work import ft_pos_neg_analysis_lst
    except:
        print("11.IMPORT FAILED")

    list_errors = []
    end_score = 0
    global_errors = 0

    # -------------------------test01--------------------------
    try:
        file_name = all_name_func[0]
        print("\033[32m1. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' list(' in text or ' len(' in text or 'split' in text:
            raise MyException
        elif ft_strtlist.ft_strtlist("123") != ['1', '2', '3'] and \
                ft_strtlist.ft_strtlist("jhgdf") != ['j', 'h', 'g', 'd', 'f']:
            raise MyException
        list_errors.append("1. OK")
        print("---------------------TEST-01-SUCCESS---------------------")
    except:

        print(
            "\033[31m---------------------TEST-01-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"1. KO ___{file_name}___")

    # -------------------------test02--------------------------

    try:
        file_name = all_name_func[1]
        print("\033[32m2. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif '.join(' in text or ' len(' in text or ' split' in text or \
                ' replace(' \
                in text or 'sep=' in text:
            raise MyException
        elif ft_join.ft_join([" ", "asdf"]) != "  asdf" and \
                ft_join.ft_join(["123", "asdf", "sldmc"],
                                "...?") != "123...?asdf...?sldmc"\
                and ft_join.ft_join(["123", "asdf", "sldmc"]) != "123 asdf sldmc":
            raise MyException
        list_errors.append("2. OK")
        print("---------------------TEST-02-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-02-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"2. KO ___{file_name}___")

    # -------------------------test03--------------------------

    try:
        file_name = all_name_func[2]
        print("\033[32m3. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' replace(' in text or ' pop(' in text or 'split' in text or '[' \
                                                                          ':' in text or ':]' in text or ' len(' in text:
            raise MyException
        elif ft_rmstrspc.ft_rmstrspc("asd 1234fj") != "asd1234fj" and \
                ft_rmstrspc.ft_rmstrspc(" asd   1234 fj ") != "asd1234fj":
            raise MyException
        list_errors.append("3. OK")
        print("---------------------TEST-03-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-03-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"3. KO ___{file_name}___")

    # -------------------------test04--------------------------

    try:
        file_name = all_name_func[3]
        print("\033[32m4. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' replace(' in text or ' len(' in text or 'split' in text or '[' \
                                                                          ':' in text or ':]' in text:
            raise MyException
        elif ft_rmstrchar.ft_rmstrchar("erfb lkjh", " ") != "erfblkjh" and \
                ft_rmstrchar.ft_rmstrchar("e,.rfb lk.jh?/", ",./") != \
                "erfb lkjh?" and ft_rmstrchar.ft_rmstrchar("e,.rfb lk.jh?/",
                                                           [",", "."]) != \
                "erfb lkjh?/":
            raise MyException
        list_errors.append("4. OK")
        print("---------------------TEST-04-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-04-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"4. KO ___{file_name}___")

    # -------------------------test05--------------------------

    try:
        file_name = all_name_func[4]
        print("\033[32m5. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_sumlst.ft_sumlst([1, 2, 3, 4]) != 10 and ft_sumlst.ft_sumlst([
            1, 2.2, 3, 4.5]) != 10.7 and ft_sumlst.ft_sumlst([1.1, 2.0, 3.0,
                                                              4]) != 10.1:
            raise MyException
        list_errors.append("5. OK")
        print("---------------------TEST-05-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-05-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"5. KO ___{file_name}___")

    # -------------------------test06--------------------------

    try:
        file_name = all_name_func[5]
        print("\033[32m6. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_sum_even_lst.ft_sum_even_lst([1, 2, 3, 4, 5, 6]) != 9 and \
                ft_sum_even_lst.ft_sum_even_lst([1.1, 2.3, 3, 4.98, 5.4, 6]) != \
                9.5 and ft_sum_even_lst.ft_sum_even_lst([0, 22, 37.0, 84,
                                                         12]) != 49.0:
            raise MyException
        list_errors.append("6. OK")
        print("---------------------TEST-06-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-06-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"6. KO ___{file_name}___")

    # -------------------------test07--------------------------

    try:
        file_name = all_name_func[6]
        print("\033[32m7. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_sum_even_part_lst.ft_sum_even_part_lst(
                [1, 2, 2, 2, 2, 4, 1110]) \
                != 1122 and ft_sum_even_part_lst.ft_sum_even_part_lst([1, 3,
                                                                       5, 7,
                                                                       9]) != 0 \
                and ft_sum_even_part_lst.ft_sum_even_part_lst([2, -2, 2, -2, -5, -4]) != -4:
            raise MyException
        list_errors.append("7. OK")
        print("---------------------TEST-07-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-07-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"7. KO ___{file_name}___")

    # -------------------------test08--------------------------

    try:
        file_name = all_name_func[7]
        print("\033[32m8. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        list_all = (
            [1, 2, 3, 4, 5], [4, 5, 1, 4, 1, 2], [1, 1, 1, 1],
            [10, 10, 10, 10], [2.2, 2.3, 111.111, 2.0])
        list_all_rev = (
            [[2, 4], [1, 3, 5]], [[4, 4, 2], [5, 1, 1]], [[], [1, 1, 1, 1]],
            [[10, 10, 10, 10], []], [[2.0], [2.2, 2.3, 111.111]])
        for i in range(len(list_all)):
            if ft_odd_even_separator_lst.ft_odd_even_separator_lst(list_all[
                                                                       i]) \
                    != \
                    list_all_rev[i]:
                raise MyException
        list_errors.append("8. OK")
        print("---------------------TEST-08-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-08-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"8. KO ___{file_name}___")

    # -------------------------test09--------------------------

    try:
        file_name = all_name_func[8]
        print("\033[32m9. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        list_all = (
            [-1, 2, -3, -4, 5, 0], [4, 5, 1, 4, 0, 1, 2], [1, 1, 1, 1],
            [-1, -2, -3, -3],
            [-10, -10, 10, 10, 0, 0, 0, 0], [-2.2, 2.3, -111.111, 2.0, 0, 0],
            [0, 0, 0, 0], [0])

        list_all_rev = (
            [[-1, -3, -4], [0], [2, 5]], [[], [0], [4, 5, 1, 4, 1, 2]],
            [[], [], [1, 1, 1, 1]],
            [[-1, -2, -3, -3], [], []],
            [[-10, -10], [0, 0, 0, 0], [10, 10]],
            [[-2.2, -111.111], [0, 0], [2.3, 2.0]],
            [[], [0, 0, 0, 0], []], [[], [0], []])
        for i in range(len(list_all)):
            if ft_pos_neg_separator_lst.ft_pos_neg_separator_lst(list_all[
                                                                     i]) != \
                    list_all_rev[i]:
                raise MyException
        list_errors.append("9. OK")
        print("---------------------TEST-09-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-09-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"9. KO ___{file_name}___")
    # -------------------------test10--------------------------
    try:
        file_name = all_name_func[9]
        print("\033[32m10. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            ft_odd_even_analysis_lst.ft_odd_even_analysis_lst([1,2,3,4,5,6,7,3,2,1,2,4,5,6,54,32,1,245,32,12,-4,-6,-12,45])
        s = f.getvalue()
        if s != """Анализ списка:
Количество четных чисел: 14,\t\tКоличество нечетных чисел: 10
Максимальная четная цифра: 54,\t\tМаксимальная нечетная цифра: 245,
Минимальная четная цифра: -12,\t\tМинимальная нечетная цифра: 1,
Сумма четных чисел: 134,\t\tСумма нечетных чисел: 316,
""":
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            ft_odd_even_analysis_lst.ft_odd_even_analysis_lst([1, 2, 3, 4, 5, 6, 7, 3, 5, 6, 54, 32, 1, 2, 12, -4, -6, -12, 45])
        s = f.getvalue()
        if s != """Анализ списка:
Количество четных чисел: 11,\t\tКоличество нечетных чисел: 8
Максимальная четная цифра: 54,\t\tМаксимальная нечетная цифра: 45,
Минимальная четная цифра: -12,\t\tМинимальная нечетная цифра: 1,
Сумма четных чисел: 96,\t\tСумма нечетных чисел: 70,
""":
            raise MyException
        list_errors.append("10. OK")
        print("---------------------TEST-10-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-10-FAILED"
            "---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"10. KO ___{file_name}___")

    # -------------------------test11--------------------------
    try:
        file_name = all_name_func[10]
        print("\033[32m11. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py",
                                show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        f = io.StringIO()
        with redirect_stdout(f):
            ft_pos_neg_analysis_lst.ft_pos_neg_analysis_lst([-1,2,3,-5,-756,-23,-235,345,34,123,11,56,-65,0,0,324,23,4,5])
        s = f.getvalue()
        if s != """Положительные:	Отрицательные:
Количество чисел: 11,	Количество чисел: 6,
Максимальная цифра: 345,	Максимальная цифра: -1,
Минимальная цифра: 2,	Минимальная цифра: -756,
Сумма чисел: 930,	Сумма чисел: -1085,
Среднее значение: 84.5	Среднее значение: -180.8

Количество нулей: 2
""":
            raise MyException
        list_errors.append("11. OK")
        print("---------------------TEST-11-SUCCESS---------------------")
    except:
        print(
            "\033[31m---------------------TEST-11-FAILED"
            "---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"11. KO ___{file_name}___")

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
            list_errors[i] = "<font color=\"#fa8e47\">" + list_errors[
                i] + "</font>"
        elif "OK" in list_errors[i]:
            list_errors[i] = "<font color=\"#32CD32\">" + list_errors[
                i] + "</font>"
    list_errors = "<br>" + "<br>".join(list_errors)


    send_mail_to_applicant(f"Имя ученика: {student_name}<br>{link_git} <br>Список ошибок: {list_errors} <br><br>Итоговый балл: {end_score * 10}",
                           "ibkov@yandex.ru")

    try:
        send_mail_to_applicant(f"Список ошибок: {list_errors} <br><br>Итоговый балл: {end_score * 10}", e_mail)
    except:
        print("No file to feedback")

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), settings.MEDIA_ROOT + '/checked_work/')
    shutil.rmtree(path)
