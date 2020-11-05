import os
import zipfile
import pandas as pd
import requests  # импортируем модуль
import traceback
from django.conf import settings



def get_csv_file_stepic(link):
    try:
        os.remove(settings.MEDIA_ROOT + "/other/class-13135-grade-book.csv")
    except:
        pass
    f = open(settings.MEDIA_ROOT + '/other/file_bd.zip', "wb")  # открываем файл для записи, в режиме wb
    ufr = requests.get(link)  # делаем запрос
    f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
    f.close()
    z = zipfile.ZipFile(settings.MEDIA_ROOT + '/other/file_bd.zip', 'r')
    z.extractall(path=settings.MEDIA_ROOT + '/other/')
    os.remove(settings.MEDIA_ROOT + "/other/file_bd.zip")
    print("File_update")

def get_info_for_all_class():
    df = pd.DataFrame(pd.read_csv(settings.MEDIA_ROOT + "/other/class-13135-grade-book.csv", header=0))
    df = df.loc[:, "ЕГЭ Тренировка 1 Q1":"total"]
    del df["total"]
    count_tasks = df.shape[1]
    df["total"] = df.loc[:].sum(axis=1)
    df["procent_success"] = round(df["total"] / count_tasks * 100)
    df["count_tasks"] = count_tasks
    for i in range(1, 28):
        df[f"ЕГЭ {i}"] = 0.0
    temp = []
    for i in df.columns:
        if i.startswith("ЕГЭ Тренировка "):
            temp.append(int(i[15:i.find("Q")]))
    index_list = [-1]
    for i in range(len(temp) - 1):
        if temp[i] != temp[i + 1]:
            index_list.append(i)
    index_list.append(len(temp) - 1)
    for i in range(len(index_list) - 1):
        df_temp = df.iloc[:, [i for i in range(index_list[i] + 1, index_list[i + 1] + 1)]]
        df[f"ЕГЭ {df_temp.columns[0][15:df_temp.columns[0].find('Q') - 1]}"] = df_temp.loc[:].sum(axis=1)
    df_all_class = df.loc[:, 'ЕГЭ 1':'ЕГЭ 27'].copy()
    return [int(i) for i in df_all_class.sum()]

def get_stepic_info(id_puple):
    try:
        df = pd.DataFrame(pd.read_csv(settings.MEDIA_ROOT + "/other/class-13135-grade-book.csv", header=0))
        df1 = pd.DataFrame(pd.read_csv(settings.MEDIA_ROOT + "/other/id_stepic_id_site.csv", header=0, delimiter=";"))
        id_for_site = {df1.iloc[i]["id_site"]: df1.iloc[i]["id_stepic"] for i in range(df1.shape[0])}
        temp_df_id = df["user_id"]
        df = df.loc[:, "ЕГЭ Тренировка 1 Q1":"total"]
        del df["total"]
        count_tasks = df.shape[1]
        df["total"] = df.loc[:].sum(axis=1)
        df["procent_success"] = round(df["total"] / count_tasks * 100)
        df["count_tasks"] = count_tasks
        for i in range(1, 28):
            df[f"ЕГЭ {i}"] = 0.0
        temp = []
        for i in df.columns:
            if i.startswith("ЕГЭ Тренировка "):
                temp.append(int(i[15:i.find("Q")]))
        index_list = [-1]
        for i in range(len(temp) - 1):
            if temp[i] != temp[i + 1]:
                index_list.append(i)
        index_list.append(len(temp) - 1)
        for i in range(len(index_list) - 1):
            df_temp = df.iloc[:, [i for i in range(index_list[i] + 1, index_list[i + 1] + 1)]]
            df[f"ЕГЭ {df_temp.columns[0][15:df_temp.columns[0].find('Q') - 1]}"] = df_temp.loc[:].sum(axis=1)
        df.insert(0, "user_id", temp_df_id)
        return [int(df.loc[df['user_id'] == id_for_site[id_puple]][i]) for i in
                df.loc[df['user_id'] == id_for_site[id_puple]].columns]
    except KeyError:
        traceback.print_exc()
        return []
    except FileNotFoundError:
        traceback.print_exc()
        return []