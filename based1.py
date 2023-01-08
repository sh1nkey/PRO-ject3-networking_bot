import pathlib
from pymysql import cursors
from config1 import user, host, password, db_name, reminder_txt_dir, vk_token
import random
from vkbot1 import sending_message_func
from vk_api.longpoll import VkLongPoll
import vk_api
import copy
import string
import re
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
        cursorclass=pymysql.cursors.DictCursor
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


def create_table(): #функция для создания таблицы
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


def create_timers(imya_name, imya_srok):
    nuzn_perm = copy.deepcopy(imya_srok)
    for _ in range(0, len(imya_name)):
        nam = imya_name[_]['Имя']
        nuzn_perm[nam] = 0
    print(nuzn_perm)
    return [nuzn_perm, imya_srok,  imya_name]



def create_dft(tablename):
    try:
        with connection.cursor() as cursor:
            create_listtable = "SELECT Имя FROM project3.%s "
            cursor.execute(create_listtable % tablename)
            print('tablelist cret succfukk')
            my_result1 = cursor.fetchall()

            f = {}
            for _ in range(0, len(my_result1)): #создается словарь с именами людей и нулями для произведение отсчета
                l = my_result1[_]['Имя']
                f[l] = 0


            vals = "SELECT Срок_напоминания FROM project3.%s "
            cursor.execute(vals % tablename)
            print('tablist updt succfully')
            my_result = cursor.fetchall()

            for _ in range(0, len(f)):
                nd = my_result1[_]['Имя']
                f[nd] = my_result[_]['Срок_напоминания']

            print(f)
            return [my_result1, f]

    except Exception as ex:
        print("Connection refused...")
        print(ex)

def generate_name_for_timer_txt(self):
    n_new = 'Napominalka-{}'.format(self)
    return n_new





class Napominalka():
    def __init__(self, nuzn_perm, imya_srok, imya_name, vk_id):
        self.vk_id = vk_id
        self.nuzn_list = nuzn_perm
        self.imya_srok = imya_srok
        self.imya_name = imya_name



    def append_totxt(self):
        c_name = generate_name_for_timer_txt(self.vk_id)

        pas = pathlib.Path(reminder_txt_dir +'/{}.txt'.format(c_name))

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
        listofdots = []
        for _ in range(0, len(x) + 1):
            if x[_] == "'":
                listofdots.append(_)
            elif x[_] == "}":
                break
        list_of_names0 = []
        list_of_names1 = []
        for _ in range (0, len(listofdots)):
            if _ % 2 == 0:
                list_of_names0.append(x[listofdots[_]: listofdots[_ + 1]])

        for _ in list_of_names0:
            adding = _[1:]
            list_of_names1.append(adding)

        s = [int(s) for s in re.findall(r'-?\d+\.?\d*', x)]
        for _ in s:
            if _ == 4938:
                s.remove(_)


        first_numlist = [s[x] for x in range (0, len(s)//2)]
        s_ready = s[len(s)//2 :]


        sending_massive = []
        print(s_ready, '\n', first_numlist)
        for _ in range (0, len(s_ready)):

            if first_numlist[_] < s_ready[_]:
                first_numlist[_] += 1



            elif first_numlist[_] >= s_ready[_]:
                first_numlist[_] -= first_numlist[_]
                sending_massive.append(list_of_names1[_])


        rewrite_count = {}
        for _ in range (0, len(list_of_names1)):
            rewrite_count[list_of_names1[_]] = first_numlist[_]

        str_beg = 0
        for _ in range (0, len(x)):
            if x[_] == '[':
                str_beg = _

        rewrite = str(rewrite_count) + x[str_beg:]

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

def cheking_sending_timer_func():
    users_to_be_sent_list, sending_people_list = rewriting_data_timer_func()
    print('id list:', users_to_be_sent_list, 'sending list:', sending_people_list)

    sd = ''
    try:
        if len(sending_people_list) > 0:
            for _ in sending_people_list:
                if len(_) == 0:
                    continue
                id = users_to_be_sent_list[sending_people_list.index(_)]
                print('slindex:', sending_people_list.index(_))
                for _1 in _:
                    print('_::::')
                    sd = sd + '\n' + "Не забудь написать человеку [{}]!".format(_1)
                sending_message_func(id, sd)
                sd = ''
    except vk_api.exceptions.ApiError:
        pass

cheking_sending_timer_func()

'''
функция удаления пользователей из таблицы будет доступна в будущих обновлениях
'''
# def delete_people(tname, del_name):
#     try:
#         with connection.cursor() as cursor:
#             del_name_int = int(del_name)
#             t = [tname, str(del_name_int), tname, tname, tname, ]
#
#
#             cursor.execute('DELETE FROM project3.symbol=? WHERE id = symbol=?; ALTER TABLE project3.symbol=? DROP id; ' \
#                       'ALTER TABLE project3.symbol=? ADD id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST; ' \
#                       'ALTER TABLE project3.symbol=? AUTO_INCREMENT = 1; set @n=0; update t1 set id=(@n:=@n+1);', [t])
#             connection.commit()
#             print('dltd sucsefuly')


    # except Exception as ex:
    #     print("Connection refused...")
    #     print(ex)









