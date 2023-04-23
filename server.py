from threading import Thread
import socket
import psycopg2

conn_bd_user = psycopg2.connect(dbname='user_for_chat', user='denis', password='7278', host='localhost')
#Подключение созданной базы данных для хранения данных о пользователях
cur = conn_bd_user.cursor()
#Объект содержащая результат запроса


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Создание сокета с двухсторонней связью, работающим с ip адресами версии 4, по протоколу TCP,
sock.bind(('', 55000))
#Определям порт на котором будет работать сервер и хост-интерфейс
sock.listen(10)
#Максимальное количество соединениц в очереди

list_user_spisok=[]
clients = set()
#Множество сокетов для подключения
def connection(soc_cl):
    #Функция отправки поступающих сообщений клиентам
    while True:
        #Постоянный прием сообщений обеспечивается бесконечным циклом
        print('Начало соединения, функция connection')
        message = soc_cl.recv(1024).decode()
        print(message)
        list_message=message.split('|')
        list_message_chat=[]
        list_message_chat.append(list_message[1])
        list_message_chat.append(list_message[2])
        list_message_chat.append(list_message[3])
        print(list_message)
        list_user=[]
        list_user.append(list_message[2])
        print(list_user)
        list_str = " ".join(list_user)
        print(list_str)
        # global list_user
        list_str_user = " ".join(list_user_spisok)
        list_message_chat_user=" ".join(list_message_chat)
        print(list_message_chat_user)
        print(list_str_user)
        print('аааааааааааааа')
        user_color=list_message[0]
        #Принимаем сообщения от клиентов
        global clients
        #Глобальная переменная для доступа к данным из функции
        if not(message):
            continue
        print('Перед циклом функция connection')
        for i in clients:
            #Перебираем ip клиентов из множества
            i.send((user_color+"!"+"Подключенные пользователи - "+list_str_user+"!"+list_str+"!"+list_message_chat_user).encode())
            #Отправка сообщения на каждого из клиентов в множестве
            print(message)
            print('Отправка после каждого сообщения')

def autorisation(conn):
    # Функция регистрации и авторизации клиентов
    while True:
        # Постоянная неперывная регистрация обеспечивается бесконечным циклом на принятие подключений
        message_user=conn.recv(1024).decode()
        # Принятие сообщений от пользователя с раскодировкой
        print(message_user)
        if message_user=='1':
            #Если клиент выбрал регистрацию, то с его стороны отправится единица на сервер для начала условия регистрации
            user_mas_reg=[]
            #Список, хранящий логин и пароль клиента, для удобного дальнейшего использования
            login_user_reg = conn.recv(1024).decode()
            #Логин, отправленный со стороны клиента, с ракодировкой
            print(login_user_reg)
            user_mas_reg.append(login_user_reg)
            #Добавление логина в список
            pass_user_reg = conn.recv(1024).decode()
            #Пароль, отправленный со стороны клиента
            print(pass_user_reg)
            user_mas_reg.append(pass_user_reg)
            #Добавление пароля в список
            print(user_mas_reg)
            insert_query = """ INSERT INTO user_for_chat (login_user, pass_user)
                                          VALUES (%s, %s)"""
            # Добавление логина и пароля в базу данных, с помощью языка sql
            item_tuple = (user_mas_reg[0], user_mas_reg[1])
            #Передаем параметры в sql - запрос на добавление
            cur.execute(insert_query, item_tuple)
            conn_bd_user.commit()
            #Используем транзакции, для сохранения изменений
            print("1 элемент (строка) успешно добавлен")
            conn.send('True'.encode())
            #Отправляем True при успешном добавлении нового пользователя в базу данных
            continue

        if message_user=='2':
            # Если клиент выбрал вход, то с его стороны отправится двойка на сервер для начала условий входа
            user_mas = []
            # Список, хранящий логин и пароль клиента, для удобного дальнейшего использования
            login_user = conn.recv(1024).decode()
            # Логин, отправленный со стороны клиента, с ракодировкой
            user_mas.append(login_user)
            # Добавление логина в список
            pass_user = conn.recv(1024).decode()
            # Пароль, отправленный со стороны клиента
            user_mas.append(pass_user)
            # Добавление пароля в список
            print(user_mas)
            cur.execute("SELECT login_user, pass_user from user_for_chat where login_user = %s", [login_user])
            #Отправление запроса на выборку данных из базы данных
            purchase_user = cur.fetchone()
            conn_bd_user.commit()
            if user_mas[0]==purchase_user[0] and user_mas[1]==purchase_user[1]:
                #Условие сравнения переданного имени и пароля от пользователя с значениями выборки из базы данных
                conn.send('True'.encode())
                #Отправляем True при успешной проверке
                global list_user_spisok
                list_user_spisok.append(user_mas[0])
                th1 = Thread(target=connection, args=(conn,), daemon=True)
                th1.start()
                # Создаем отдельный поток для принятия сообщений
                break
            else:
                conn.send('Вы не правильно ввели логин или пароль, перезагрузите клиент'.encode())


while True:
    #Постоянное принятие подключений клиентов, позволяет выполнить бесконечный цикл
    conn, addr = sock.accept()
    #
    print(conn, addr)
    print(f'Подключился:{addr}')
    clients.add(conn)
    #Добавление клиента в множество клиентов для хранения
    autorisation(conn)
    #В функцию авторизации и входа передаем
    print('После регистрации, перед созданием потока с сообщениями, в котором функция отправки сообщений клиентам')








# СЕРВЕР БЕЗ РЕГИСТРАЦИИ, ТОЛЬКО ПРИНИМАЕТ И ОТПРАВЛЯЕТ СООБЩЕНИЯ.
# from threading import Thread
# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет для сервера
# sock.bind(('localhost', 55000))
# sock.listen(10)
#
# clients = set() #Множество сокетов для подключения
# def connection(soc_cl):
#     while True:
#         massage = soc_cl.recv(1024)
#         global clients
#         for i in clients:
#             i.send(massage)
#
#
# while True:
#     conn, addr = sock.accept()
#     print(f'Подключился:{addr}')
#     clients.add(conn)
#     if conn:
#         th = Thread(target=connection, args=(conn,), daemon=True)
#         th.start()


































# from threading import Thread
# import socket
# import psycopg2
#
# conn_bd_user = psycopg2.connect(dbname='user_for_chat', user='denis', password='7278', host='localhost')
# cur = conn_bd_user.cursor()
#
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет для сервера
# sock.bind(('localhost', 55001))
# sock.listen(10)
#
#
# clients = set() #Множество сокетов для подключения
# def connection(soc_cl):
#     while True:
#         print('Начало соединения, функция connection')
#         massage = soc_cl.recv(1024)
#         global clients
#         print('Перед циклом функция connection')
#         for i in clients:
#             i.send(massage)
#             print('Отправка после каждого сообщения')
#
# def autorisation(conn):
#     while True:
#         # conn.send('Выберите, хотите вы зарегистрироваться - 1 или войти - 2'.encode())
#         message_user=conn.recv(1024).decode()
#         print('Начало регистрации, перед выбором регистрации или входа')
#         if message_user=='1':
#             print(111)
#             conn.send('Введите логин и пароль для регистрации'.encode())
#             conn.send('Введите логин'.encode())
#             user_mas_reg=[]
#             login_user_reg= conn.recv(1024).decode()
#             user_mas_reg.append(login_user_reg)
#             conn.send('Введите пароль'.encode())
#             pass_user_reg = conn.recv(1024).decode()
#             user_mas_reg.append(pass_user_reg)
#             print(user_mas_reg)
#             insert_query = """ INSERT INTO user_for_chat (login_user, pass_user)
#                                           VALUES (%s, %s)"""
#             item_tuple = (user_mas_reg[0], user_mas_reg[1])
#             cur.execute(insert_query, item_tuple)
#             conn_bd_user.commit()
#             print("1 элемент (строка) успешно добавлен")
#             conn.send('Вы успешно зарегистрировались, повторите ввод логина и пароля для входа'.encode())
#
#             # conn.send('Введите логин'.encode())
#             # user_mas_vxod = []
#             # login_user_vxod = conn.recv(1024).decode()
#             # user_mas_vxod.append(login_user_vxod)
#             # conn.send('Введите пароль'.encode())
#             # pass_user_vxod = conn.recv(1024).decode()
#             # user_mas_vxod.append(pass_user_vxod)
#             # print(user_mas_vxod)
#             # cur.execute("SELECT login_user, pass_user from user_for_chat where login_user = %s", [login_user_vxod])
#             # purchase_user = cur.fetchone()
#             # conn_bd_user.commit()
#
#             # if user_mas_vxod[0]==purchase_user[0] and user_mas_vxod[1]==purchase_user[1]:
#             conn.send('Вы успешно вошли, подключение к чату осуществленно'.encode())
#             break
#             # else:
#             #     conn.send('Вы не правильно ввели логин или пароль, перезагрузите клиент'.encode())
#
#         if message_user=='2':
#             conn.send('Введите логин и пароль для входа'.encode())
#             conn.send('Введите логин'.encode())
#             user_mas = []
#             login_user = conn.recv(1024).decode()
#             user_mas.append(login_user)
#             conn.send('Введите пароль'.encode())
#             pass_user = conn.recv(1024).decode()
#             user_mas.append(pass_user)
#             print(user_mas)
#             cur.execute("SELECT login_user, pass_user from user_for_chat where login_user = %s", [login_user])
#             purchase_user = cur.fetchone()
#             conn_bd_user.commit()
#             if user_mas[0]==purchase_user[0] and user_mas[1]==purchase_user[1]:
#                 conn.send('Логин и пароль введен верно, подключение осуществленно'.encode())
#                 break
#             else:
#                 conn.send('Вы не правильно ввели логин или пароль, перезагрузите клиент'.encode())
#
#
# while True:
#     conn, addr = sock.accept()
#     print(f'Подключился:{addr}')
#     clients.add(conn)
#     autorisation(conn)
#     print('После регистрации, перед созданием потока с сообщениями, в котором функция отправки сообщений клиентам')
#     if conn:
#         th1 = Thread(target=connection, args=(conn,), daemon=True)
#         th1.start()
