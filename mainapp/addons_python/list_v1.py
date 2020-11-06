import os
import shutil
import git
import pep8
import email
import email.mime.application
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

all_name_func = ['ft_even_index_list',
                     'ft_even_parts_list',
                     'ft_positive_list',
                     'ft_sl_list',
                     'ft_same_parts_list',
                     'ft_rev_list',
                     'ft_rev_par_list',
                     'ft_rshift_list',
                     'ft_super_shift_list']

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
        from media.checked_work import ft_even_index_list
    except:
        print("1.IMPORT FAILED")
    try:
        from media.checked_work import ft_even_parts_list
    except:
        print("2.IMPORT FAILED")
    try:
        from media.checked_work import ft_positive_list
    except:
        print("3.IMPORT FAILED")
    try:
        from media.checked_work import ft_sl_list
    except:
        print("4.IMPORT FAILED")
    try:
        from media.checked_work import ft_same_parts_list
    except:
        print("5.IMPORT FAILED")
    try:
        from media.checked_work import ft_rev_list
    except:
        print("6.IMPORT FAILED")
    try:
        from media.checked_work import ft_rev_par_list
    except:
        print("7.IMPORT FAILED")
    try:
        from media.checked_work import ft_rshift_list
    except:
        print("8.IMPORT FAILED")
    try:
        from media.checked_work import ft_super_shift_list
    except:
        print("9.IMPORT FAILED")


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
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_even_index_list.ft_even_index_list([1, 2, 3, 4, 5, 6, 7, 8]) != [1, 2, 3, 4, 5, 6, 7, 8][::2]\
                and ft_even_index_list.ft_even_index_list(["123",
                                                           "rtet",
                                                           "werwe",
                                                           "sfdds"]) != ['123',
                                                                         'rtet',
                                                                         'werwe',
                                                                         'sfdds'][::2]:
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
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_even_parts_list.ft_even_parts_list([1, 2, 3, 4, 5, 6, 7]) != [2, 4, 6] \
                and ft_even_parts_list.ft_even_parts_list([1, 1, 1, 1, 1]) != [] \
                and ft_even_parts_list.ft_even_parts_list([1, 1, 2, 1, 0]) != [2, 0] \
                and ft_even_parts_list.ft_even_parts_list([-2, 1, 2, 1, 0]) != [-2, 2, 0]:
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
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_positive_list.ft_positive_list([-1, -2, -3, -4, -5, -6, -67]) != 0 \
                and ft_positive_list.ft_positive_list([-1, -2, -3, -4, 5, -6, -67]) != 1 \
                and ft_positive_list.ft_positive_list([]) != 0 \
                and ft_positive_list.ft_positive_list([1, 1, 1, 1, 1]) != 5 \
                and ft_positive_list.ft_positive_list([-1, -2, -3, -4, -5, -6, 67]) != 1 \
                and ft_positive_list.ft_positive_list([1, -2, -3, -4, -5, -6, -67]) != 1:
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
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif ft_sl_list.ft_sl_list([1, 2, 3, 4, 5]) != 4 \
                and ft_sl_list.ft_sl_list([1, 2, 3, 4, 1]) != 3 \
                and ft_sl_list.ft_sl_list([5, 4, 3, 2, 1]) != 0 \
                and ft_sl_list.ft_sl_list([1, 1, 1, 1, 1, 1, 2]) != 1 \
                and ft_sl_list.ft_sl_list([1, 1, 1, 1, 0]) != 0:
            raise MyException
        list_errors.append("4. OK")
        print("---------------------TEST-04-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-04-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"4. KO ___{file_name}___")

    # -------------------------test05--------------------------

    try:
        file_name = all_name_func[4]
        print("\033[32m5. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        elif not ft_same_parts_list.ft_same_parts_list([1, 1, -2, 3, -4]) \
                and ft_same_parts_list.ft_same_parts_list([1, -2, 3, -4]):
            raise MyException
        list_errors.append("5. OK")
        print("---------------------TEST-05-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-05-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"5. KO ___{file_name}___")

    # -------------------------test06--------------------------

    try:
        file_name = all_name_func[5]
        print("\033[32m6. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        list_all = ([1, 2, 3, 4, 5], [4, 5, 1], ["qwe", "ert"], [1, 2, 3, 4, 5, 6])
        list_all_rev = ([1, 2, 3, 4, 5][::-1], [4, 5, 1][::-1], ['qwe', 'ert'][::-1], [1, 2, 3, 4, 5, 6][::-1])
        for i in range(len(list_all)):
            if id(ft_rev_list.ft_rev_list(list_all[i])) != id(list_all[i]):
                raise MyException
            if ft_rev_list.ft_rev_list(list_all_rev[i]) != list_all_rev[i]:
                raise MyException
        list_errors.append("6. OK")
        print("---------------------TEST-06-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-06-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"6. KO ___{file_name}___")

    # -------------------------test07--------------------------

    try:
        file_name = all_name_func[6]
        print("\033[32m7. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        list_all = ([1, 2, 3, 4, 5], [4, 5, 1], ["qwe", "ert"], [1, 2, 3, 4, 5, 6])
        list_all_rev = ([2, 1, 4, 3, 5], [5, 4, 1], ['ert', 'qwe'], [2, 1, 4, 3, 6, 5])
        for i in range(len(list_all)):
            if id(ft_rev_par_list.ft_rev_par_list(list_all[i])) != id(list_all[i]):
                raise MyException
            ft_rev_par_list.ft_rev_par_list(list_all[i])
            if ft_rev_par_list.ft_rev_par_list(list_all[i]) != list_all_rev[i]:
                raise MyException
        list_errors.append("7. OK")
        print("---------------------TEST-07-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-07-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"7. KO ___{file_name}___")

    # -------------------------test08--------------------------

    try:
        file_name = all_name_func[7]
        print("\033[32m8. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        list_all = ([1, 2, 3, 4, 5], [4, 5, 1], ["qwe", "ert"], [1, 2, 3, 4, 5, 6])
        list_all1 = ([1, 2, 3, 4, 5], [4, 5, 1], ["qwe", "ert"], [1, 2, 3, 4, 5, 6])
        list_all_rev = ([5, 1, 2, 3, 4], [1, 4, 5], ['ert', 'qwe'], [6, 1, 2, 3, 4, 5])
        for i in range(len(list_all)):
            if id(ft_rshift_list.ft_rshift_list(list_all[i])) != id(list_all[i]):
                raise MyException
            if ft_rshift_list.ft_rshift_list(list_all1[i]) != list_all_rev[i]:
                raise MyException
        list_errors.append("8. OK")
        print("---------------------TEST-08-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-08-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"8. KO ___{file_name}___")

    # -------------------------test09--------------------------

    try:
        file_name = all_name_func[8]
        print("\033[32m9. ", end="")
        fchecker = pep8.Checker(directory + file_name + ".py", show_source=False)
        file_errors = fchecker.check_all()
        file = open(directory + file_name + ".py", 'r')
        text = file.read()
        if file_errors != 0:
            raise MyException
        elif ' sum(' in text or ' len(' in text or 'split' in text or '[:' in text or ':]' in text:
            raise MyException
        list_all = (
            ([1, 2, 3, 4, 5], 2),
            ([4, 5, 1], -1),
            (["qwe", "ert"], 5),
            ([1, 2, 3, 4, 5, 6], 3)
        )

        list_all_rev = (
            [4, 5, 1, 2, 3],
            [5, 1, 4],
            ['ert', 'qwe'],
            [4, 5, 6, 1, 2, 3]
        )
        for i in range(len(list_all)):
            if ft_super_shift_list.ft_super_shift_list(*list_all[i]) != list_all_rev[i]:
                raise MyException
        list_errors.append("9. OK")
        print("---------------------TEST-09-SUCCESS---------------------")
    except:
        print("\033[31m---------------------TEST-09-FAILED---------------------\033[37m")
        global_errors += 1
        list_errors.append(f"9. KO ___{file_name}___")



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


    send_mail_to_applicant(f"Имя ученика: {student_name}<br>{link_git} <br>Список ошибок: {list_errors} <br><br>Итоговый балл: {end_score * 10}",
                           "ibkov@yandex.ru")

    try:
        send_mail_to_applicant(f"Список ошибок: {list_errors} <br><br>Итоговый балл: {end_score * 10}", e_mail)
    except:
        print("No file to feedback")

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), settings.MEDIA_ROOT + '/checked_work/')
    shutil.rmtree(path)

