# -----------------------------------------------------------
# program that contains all functions
#
# 2022 Alexey Kudelko, Moscow, Russia
#
# email: flexivanov237@gmail.com
# -----------------------------------------------------------


import pathlib
import json
from pymysql import cursors
from config import user, host, password, db_name, reminder_txt_dir, vk_token
import random
from vk_api.longpoll import VkLongPoll
import vk_api
import copy
import string
import os
import pymysql


def random_x_digit_number_generate(length):
    letters = string.ascii_letters
    rand_name = ''.join(random.choice(letters) for i in range(length))
    return str(rand_name)


try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,

    )
    print("successfully connected...")
    print("#" * 20)

except Exception as ex:
    print("Connection refused...")
    print(ex)


def create_people(table_name, ima, data, gorod, prof, uvl, srok):
    try:
        with connection.cursor() as cursor:
            create_ppl = 'INSERT INTO project3.%s (Имя, Дата_рождения, Город, Специализация, Увлечения, Срок_напоминания) ' \
                         "VALUES ('%s', '%s', '%s', '%s', '%s', %s);"

            cursor.execute(create_ppl % (table_name, ima, data, gorod, prof, uvl, srok,))
            connection.commit()
            print('created sucsefuly')


    except Exception as ex:
        print("Connection refused...")
        print(ex)


def change_data_table(table_name, what_change, idshnik, to_what):
    try:
        with connection.cursor() as cursor:
            identify_change = "UPDATE project3.%s" \
                              " SET" \
                              "    %s = '%s' " \
                              " WHERE id = %d"

            cursor.execute(identify_change % (table_name, what_change, to_what, idshnik))
            connection.commit()
            print('it changed succesfully')


    except Exception as ex:
        print("Connection refused...")
        print(ex)


def show_table(msg):
    try:
        with connection.cursor() as cursor:
            create_ttable = "SELECT * FROM %s"
            x = msg
            cursor.execute(create_ttable % x)
            print('it showed succesfully')

            result = cursor.fetchall()

            n = []
            for row in result:
                n.append(row)
                print("\n")
            return n


    except Exception as ex:
        print("Connection refused...")
        print(ex)


def create_table():  # функция для создания таблицы
    try:
        with connection.cursor() as cursor:

            create_ttable = "CREATE TABLE project3.%s (id INT AUTO_INCREMENT PRIMARY KEY, Имя varchar(20), Дата_рождения " \
                            " DATE, " \
                            " Город  varchar(50), Специализация varchar(50), Увлечения varchar (50), Срок_напоминания " \
                            " SMALLINT)"
            x = random_x_digit_number_generate(8)
            cursor.execute(create_ttable % x)
            print('table cret succful')
            return x


    except Exception as ex:
        print("Connection refused...")
        print(ex)


def create_timers(imya_name, name_term):  # манипуляция со словарями для дальнейшей работы с ними
    nuzn_perm = copy.deepcopy(name_term)
    for _ in range(0, len(imya_name)):
        nam = imya_name[_]['Имя']
        nuzn_perm[nam] = 0
    print(nuzn_perm)
    return [nuzn_perm, name_term, imya_name]


def create_dft(tablename):  # манипуляция со словарями
    try:
        with connection.cursor() as cursor:
            create_listtable = "SELECT Имя FROM project3.%s "
            cursor.execute(create_listtable % tablename)
            my_result1 = cursor.fetchall()

            f = {}
            for _ in range(0, len(my_result1)):  # создается словарь с именами людей и нулями для произведение отсчета
                l = my_result1[_]['Имя']
                f[l] = 0

            vals = "SELECT Срок_напоминания FROM project3.%s "
            cursor.execute(vals % tablename)
            my_result = cursor.fetchall()

            for _ in range(0, len(f)):
                nd = my_result1[_]['Имя']
                f[nd] = my_result[_]['Срок_напоминания']

            return [my_result1, f]

    except Exception as ex:
        print("Connection refused...")
        print(ex)


def generate_name_for_timer_txt(self):
    name_new = 'Napominalka-{}'.format(self)
    return name_new


class Reminder():
    def __init__(self, nuzn_perm, name_term, imya_name, vk_id):
        self.vk_id = vk_id
        self.nuzn_list = nuzn_perm
        self.imya_srok = name_term
        self.imya_name = imya_name

    def append_totxt(self):
        c_name = generate_name_for_timer_txt(self.vk_id)

        pas = pathlib.Path(reminder_txt_dir + '/{}.txt'.format(c_name))

        w = open(pas, 'w')
        w.write(str(self.nuzn_list) + str(self.imya_name) + str(self.imya_srok))
        w.close()


def rewriting_data_timer_func():
    list_papok = os.listdir(reminder_txt_dir)
    list_of_users = []
    list_of_people = []
    for i in list_papok:
        r = open(reminder_txt_dir + '/{}'.format(i), 'r')
        x = r.read()
        r.close()
        timer_dic = json.loads(x[0:x.find("}") + 1].replace("\'", "\""))  # тут текстовая версия словаря переводится в словарную
        name_dic = json.loads(x[x.find("["):x.find("]") + 1].replace("\'", "\""))
        limit_dic = json.loads(x[x.find("]") + 1:-1].replace("\'", "\"") + "}")

        sending_massive = []
        for _ in timer_dic:

            if timer_dic[_] < limit_dic[_]:
                timer_dic[_] += 1

            elif timer_dic[_] >= limit_dic[_]:
                timer_dic[_] -= limit_dic[_]
                sending_massive.append(_)

        rewrite = str(timer_dic) + str(name_dic) + str(limit_dic)
        w = open(reminder_txt_dir + '/{}'.format(i), 'w')
        w.write(rewrite)
        w.close()

        id_user = i[12:21]

        list_of_users.append(str(id_user))
        list_of_people.append(sending_massive)

    return list_of_users, list_of_people


vk_session = vk_api.VkApi(token=vk_token)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def sending_message_func(id, text):
    vk_session.method("messages.send", {"user_id": id, "message": text, "random_id": 0})


def cheking_sending_timer_func():  # отправляет напоминания
    users_to_be_sent_list, sending_people_list = rewriting_data_timer_func()

    try:
        if len(sending_people_list) > 0:
            for _ in sending_people_list:
                sd = 'Не забудь написать человеку '
                control_str_variable = 27
                if len(_) == 0:  # эта строка скипает пустой списо
                    continue
                elif len(_) > 1:
                    sd = 'Не забудь написать людям '
                    control_str_variable = 25
                id = users_to_be_sent_list[sending_people_list.index(_)]
                for _1 in _:
                    sd += "[{}], ".format(_1)
                sd_list = list(sd)
                sd_list[-2] = '!'
                sd = ''.join(sd_list)
                sending_message_func(id, sd)
                print('человеку: ', id, '\n отправлены: ', sd[control_str_variable: -1])
    except vk_api.exceptions.ApiError:
        pass


if __name__ == "__main__":
    cheking_sending_timer_func()

'''
функция удаления пользователей из таблицы будет доступна в будущих обновлениях
'''
# def delete_people(tname, del_name):
#     try:
#         with connection.cursor() as cursor:
#             s =f'DELETE FROM project3.{tname} WHERE id = {del_name}; ALTER TABLE project3.{tname} DROP id; ' \
#                            f'ALTER TABLE project3.{tname} ADD id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST; ' \
#                            f'ALTER TABLE project3.{tname} AUTO_INCREMENT = 1; set @n=0; update t1 set id=(@n:=@n+1);'
#             s = filter(None, s.split(';'))
#             for i in s:
#                 # strip() removes leading and trailing white spaces
#                 # semicolon is re-added per line for query run
#                 cur.execute(i.strip() + ';')
#             connection.commit()
#             print('dltd sucsefuly')
#
#
#     except Exception as ex:
#         print("Connection refused...")
#         print(ex)
