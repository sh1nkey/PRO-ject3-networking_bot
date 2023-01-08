# -----------------------------------------------------------
# the main program for the bot to work
#
# 2022 Alexey Kudelko, Moscow, Russia
#
# email flexivanov237@gmail.com
# -----------------------------------------------------------






import vk_api,  pathlib, os
from vk_api.longpoll import VkLongPoll, VkEventType
from based import create_table, show_table, change_table, comparing, create_people, delete_people, create_dft, Napominalka, \
    create_timers


vk_session = vk_api.VkApi(token='vk1.a.fN2xUHC6V5pciRzSeTYo67DUTqLNeaHAzuhafpgnkgBqWb-O858OEWBCKRAN_CD-Osu67MATaJvcgNa_uB8KWvWmQd1JfqlqA0iptV62yl-X_vt4KiVmacwEZIq_hm7mwgkLY_FUFMKEkrM0ISAwycPkhuONRP8vU0BzAH1qrNONPhvkrriO-xq-XNTphb2V')
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def send_some_message(id,text):
    vk_session.method("messages.send", {"user_id":id, "message":text, "random_id": 0})


def checking():
    id_list, sending_list = comparing()
    print('id list:', id_list, 'sending list:', sending_list)
    sd = ''
    try:
        if len(sending_list) > 0:
            for _ in sending_list:
                if len(_) == 0:
                    continue
                id = id_list[sending_list.index(_)]
                print('slindex:', sending_list.index(_))
                for _1 in _:
                    print('_::::')
                    sd = sd + '\n' + "Не забудь написать человеку [{}]!".format(_1)
                send_some_message(id, sd)
                sd = ''
    except vk_api.exceptions.ApiError:
        pass


change_list = []
tne = ''
running = 0



for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg= event.text.lower()
            id = event.user_id
            print(id)
            if msg == "привет":
                send_some_message(id, "Давай сразу к делу. Инструкция:\n (Команды писать без квадратных скобочек)\n\n-создать "
                                      "таблицу, "
                                      "в которой будут размещаться данные:\n[!создатьтаблицу]\n\n"
                                      "-чтобы посмотреть содержание таблицы, надо ввести ее название, которое состоит из 8-ми символов: [idsmHkPk]\n\n-чтобы добавить человека, надо написать эту команду, например: [создать ddldfdls Иван_Иванович 2000-01-13 Село_Иваново корововед увлекается_аниме 14] \
\nИз ограничений разве что строгое расположение пробелов: их ставить только между категориями. Внутри категории использовать  \
нижнее подчеркивание (_). Вот кстати категории: [номер имя_фамилия дата_рождения город специальность увлечения срок напоминания]\n\n-Чтобы задать ячейку, в которой вам нужно что-то изменить, пишем: [изменить название_таблицы категория порядковый_номер_человека].' \
'Например:[изменить qwerTyui Имя 2]\n\nЧтобы поменять данные в этой ячейке пишем: [на то_на_что_меняем]. Например: [на Андрей]' \
'\n\n-чтобы заставить программу напоминать вам о том, чтобы время от времени писать определенным людям, то пишем: [отсчет "
                                      "название_таблички]. Например: [отсчет qwertyUi]\nНе беспокойтесь, если вы обновите свою таблицу, то и список тоже обновится :) ")
            if msg == "!создатьтаблицу":
                send_some_message(id, "таблица готова!\n ее имя:" + create_table())
            if len(msg) == 8:
                send_some_message(id, "Вот содержание таблицы {}\n:".format(msg))
                full = list(show_table(msg))
                sd = ''
                for _ in range(0, len(full)):
                    n = list(show_table(msg)[_].values())
                    print(n)
                    sd = sd + '\n'+"["+str(n[0])+']'+" "+"["+str(n[1])+']'+" "+"["+str(n[2])+']'+" "+"["+str(n[3])+']'+ \
                        " "+"["+str(n[4])+']'+" "+"["+str(n[5])+']'+" "+"["+str(n[6])+']'+'\n'
                send_some_message(id, sd)


            if msg[0] == 'и':
                table_name = msg[9:17]
                tne = msg[9:17]
                change_list.append(table_name)
                idshnik = 0
                what_change = msg[18:-2]
                change_list.append(what_change)
                if msg[-2] == ' ':
                    idshnik = int(msg[-1])
                else:
                    idshnik = int(str(msg[-2] + '' + msg[-1]))
                change_list.append(idshnik)
                send_some_message(id, "Хорошо, на что вы хотите изменить? ")
                if len(change_list) > 3:
                    change_list.clear()

            if msg[0:2] == "на":
                to_what = msg[3:]
                change_table(change_list[0], change_list[1], change_list[2], to_what)
                send_some_message(id, "Изменено успешно! ")
                change_list.clear()

                checking_path = pathlib.Path('C:/Users/User/Desktop/testing/{}.txt'.format('Napominalka-' + str(id)))
                if os.path.exists(checking_path):
                    running = 1


            if msg[0] == 'у':
                tname = msg[8:16]
                if msg[-2] == ' ':
                    del_name = int(msg[-1])
                else:
                    del_name = int(msg[-2] + '' + msg[-1])
                print(type(del_name))
                print(del_name)
                delete_people(tname, del_name)
                send_some_message(id, "человек удален ")


            if msg[0] == 'о' or running == 1:  # создать и запустить отсчет
                tname = msg[7:]
                if running == 1:
                    tname = tne
                retu = create_dft(tname)
                par_3 = create_timers(retu[0], retu[1])
                print('PAR_3', par_3)
                nap = Napominalka(par_3[0], par_3[1], par_3[2], str(id))
                nap.append_totxt()
                if running == 0:
                    send_some_message(id, 'список создан!')
                if running == 1:
                    running = 0



            if msg[0] == 'с':
                probel_list = []
                d = -1
                for i in msg:
                    d += 1
                    if i == " ":
                        probel_list.append(d)
                    if len(probel_list) == 7:
                        break
                print('probellist:', probel_list)
                table_name  = msg[probel_list[0]:probel_list[1]]
                yima = msg[probel_list[1]:probel_list[2]]
                data = msg[probel_list[2]:probel_list[3]]
                gorod = msg[probel_list[3]:probel_list[4]]
                prof = msg[probel_list[4]:probel_list[5]]
                uvl = msg[probel_list[5]:probel_list[6]]
                if msg[-2] == ' ':
                    srok = msg[-1]
                else:
                    srok = int(str(msg[-2] + '' + msg[-1]))
                print('dannie:', table_name, yima, data, gorod, prof, uvl, srok)
                create_people(table_name, yima, data, gorod, prof, uvl, srok)
                send_some_message(id, "Готово! ")











