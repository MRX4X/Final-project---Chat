from time import sleep
from datetime import datetime
import socket
from threading import Thread
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Создание сокета с двухсторонней связью, работающим с ip адресами версии 4, по протоколу TCP,
sock.connect(('localhost', 55000))
#Подключение к серверу, по порту 550000
name_user=None
#Глобальная переменная имени клиента
class Login(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.welcome_label = QtWidgets.QLabel('Добро пожаловать в наш чат! Здесь вы можете общаться с другими пользователями в режиме реального времени.\nДля того, чтобы начать общение,войдите или зарегистрируйтесь, затем просто введите ваше сообщение в поле ввода и нажмите "Отправить".\nПрежде чем начать общение, пожалуйста, ознакомьтесь с правилами поведения в нашем чате:\nЗапрещено использование нецензурной лексики и оскорбительных выражений;\nНе размещайте ссылки на вредоносные сайты или файлы;\nУважайте права других пользователей и не нарушайте их конфиденциальность.')
        self.login_button = QtWidgets.QPushButton('Вход')
        self.register_button = QtWidgets.QPushButton('Регистрация')

        self.setMinimumSize(800, 600)
        self.setMaximumSize(1200, 900)
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        #Функция авторизации клиента
        #тут надо цикл и брейкать после успеха, а в случае не успеха повторять
        while True:
            login, password, ok = self.show_login_dialog()
            print(login,password,ok)
            if ok:
                sock.send(bytes("2", encoding='UTF-8'))
                #Передаем на сервер сообщение вызывающее условие для входа клиента
                sleep(1)
                sock.send(bytes(login, encoding='UTF-8'))
                #Отправляем логин клиента на сервер
                sleep(1)
                sock.send(bytes(password, encoding='UTF-8'))
                #Отправляем пароль на сервер
                register_chek = sock.recv(1024).decode()
                #Значение возвращаемое сервером, True - при успешной авторизации, False - при не успешной, и цикл начнет работу занова и авторизацию нудно будет пройти повторно
                print(register_chek)
                if register_chek=="True":
                    global name_user
                    name_user=login
                    #В качестве имени отправителя будет использоваться логин клиента
                    self.chat_window = ChatWindow()
                    self.chat_window.show()
                    # self.statusbar.showMessage('Вход выполнен успешно')
                    self.close()
                    break
                else:
                    QtWidgets.QMessageBox.warning(self, 'Ошибка входа', 'Неправильный логин или пароль')
                    # continue
                    #не корректный пароль или логин, должно в графическом интерфейсе должно появляться сообщение об ошибке

    def register(self):
        # Функция добавления (регистрации) нового аккаунта в базу данных
        login, password, ok = self.show_login_dialog()
        if ok:
            sock.send(bytes("1", encoding='UTF-8'))
            # Передаем на сервер сообщение вызывающее условие для регистрации клиента
            sleep(1)
            sock.send(bytes(login, encoding='UTF-8'))
            # Отправляем логин клиента на сервер
            sleep(1)
            sock.send(bytes(password, encoding='UTF-8'))
            # Отправляем пароль на сервер
            register_chek=sock.recv(1024).decode()
            # Значение возвращаемое сервером, True - при успешной регистрации.
            if register_chek=="True":
                # self.chat_window = ChatWindow()
                # self.chat_window.show()
                self.login()
                self.close()

    def show_login_dialog(self):
        login, password, ok = '', '', False
        dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()

        login_label = QtWidgets.QLabel('Логин:')
        login_edit = QtWidgets.QLineEdit()
        password_label = QtWidgets.QLabel('Пароль:')
        password_edit = QtWidgets.QLineEdit()
        password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(login_label)
        layout.addWidget(login_edit)
        layout.addWidget(password_label)
        layout.addWidget(password_edit)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            login = login_edit.text()
            password = password_edit.text()
            ok = True

        return login, password, ok



# class Register(QtWidgets.QWidget):
#     switch_window = QtCore.pyqtSignal()
#
#     def __init__(self):
#         super().__init__()
#
#         layout = QtWidgets.QVBoxLayout()
#
#         self.login_label = QtWidgets.QLabel('Логин:')
#         self.login_edit = QtWidgets.QLineEdit() #виджет для ввода логина и пароля, а также подтверждения пароля
#         self.password_label = QtWidgets.QLabel('Пароль:')
#         self.password_edit = QtWidgets.QLineEdit()
#         self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.password_confirmation_label = QtWidgets.QLabel('Подтверждение пароля:')
#         self.password_confirmation_edit = QtWidgets.QLineEdit()
#         self.password_confirmation_edit.setEchoMode(QtWidgets.QLineEdit.Password)
#
#         self.register_button = QtWidgets.QPushButton('Зарегистрироваться')
#
#         self.register_button.clicked.connect(self.register)
#
#         layout.addWidget(self.login_label)
#         layout.addWidget(self.login_edit)
#         layout.addWidget(self.password_label)
#         layout.addWidget(self.password_edit)
#         layout.addWidget(self.password_confirmation_label)
#         layout.addWidget(self.password_confirmation_edit)
#         layout.addWidget(self.register_button)
#
#         self.setLayout(layout)
#
#     def register(self):
#         # Код регистрации нового пользователя
#         sock.send("1".encode())
#         sock.send(self.login_edit.text().encode(()))
#         self.close()

class ChatWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1200, 900)
        self.list_users_hight = QtWidgets.QLabel('Участники переписки')
        self.list_users = QtWidgets.QLabel()
        self.message_box = QtWidgets.QTextBrowser() #виджет для отображения сообщений
        self.message_box.setReadOnly(True)
        th = Thread(target=self.reciever,daemon=True)
        th.start()
        #Создаем отдельный поток для принятия сообщений постоянно работющий отдельно от основного потока, пока не завершиться сама программа
        self.input_box = QtWidgets.QLineEdit() #виджет для ввода новых сообщений
        self.send_button = QtWidgets.QPushButton('Отправить')
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.list_users)
        self.layout.addWidget(self.message_box)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)


    def send_message(self):
        # Функция отправки сообщений на сервер
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Переменная хранящая занчений сегодняшней даты и времени
        sock.send(("green"+'|'+dt+' ' + '|' + name_user + '|' + ' ' + self.input_box.text()).encode())
        # Отправка сообщения а сервер: текущая дата, имя клиента из глобальной переменной, введенное сообщение в поле ввода в графическом интерфейсе

    def reciever(self):
        """
        Function to recieve message

        """
        # Функция принятия сообщений, запущенная в отдельном потоке
        while True:
            #Постоянно работающий цикл для принятия сообщений
            text = sock.recv(1024).decode()
            #Принимаем сообщения от сервера
            print(text)
            self.input_box.clear()
            new_text = text.split("!")
            print(new_text)
            new_color=new_text[0]
            #Очищаем строку ввода сообщений клиента, чтобы после отправки удобно было вводить новое сообщение
            self.message_box.append(f"<p style=\"color:{new_color}\">{new_text[3]}</p>")
            # Добавление сообщения в чат, белое большое окно
            # self.list_users.clear()
            self.list_users.setText(new_text[1])
            #Добавление ника пользователя в список пользователей сверху
            #Передаем текст от сервера в графический интерфейс отображения сообщений клиента


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())


#Создать функциональность для переходов между различными окнами и обработки пользовательского ввода.
#Добавим методы для перехода между окнами. Для этого создадим функцию, которая будет скрывать текущее окно и открывать экран входа
#Используем метод setCurrentWidget объекта stackedWidget, чтобы переключаться между различными экранами.

def show_login_screen(self):
    self.stackedWidget.setCurrentWidget(self.login_screen)

#Создать анологичную ф-ю для перехода к экрану регистрации

def show_registration_screen(self):
    self.stackedWidget.setCurrentWidget(self.registration_screen)

#Метод, который будет скрывать текущее окно и открывать экран чата

def show_chat_screen(self):
    self.stackedWidget.setCurrentWidget(self.chat_screen)

#Теперь, когда мы можем переключаться между различными экранами, добавим обработчики событий для кнопок входа, регистрации и отправки сообщений в чат
#Создать для обработки событий нажатия кнопки входа

def handle_login_button(self):
    username = self.login_username_input.text()
    password = self.login_password_input.text()
    # здесь должна быть логика проверки введенных данных и авторизации пользователя
    self.show_chat_screen()


#Добавим обработчик событий для кнопки регистрации

def handle_registration_button(self):
    username = self.registration_username_input.text()
    password = self.registration_password_input.text()

    #Функция обрабатывает нажатие кнопки "Зарегистрироваться" на странице регистрации. Она получает значения, введенные пользователем в поля "Логин" и "Пароль", и должна выполнить проверку их корректности, а затем зарегистрировать пользователя в системе. Пока что эта проверка и регистрация не реализованы, вместо этого функция вызывает метод show_login_screen, который переключает отображаемую страницу на страницу авторизации.
    # здесь должна быть логика проверки введенных данных и регистрации пользователя
    #вызываем метод, чтобы переключиться на экран чата
    #Метод,  чтобы переключиться на экран входа

    self.show_login_screen()

#Добавим обработчик событий для кнопки отправки сообщения
#Создать ф-ю для обработки событий нажатия кнопки отправки сообщения
#Ф-я обрабатывает нажатие кнопки "Отправить" на странице чата. Она получает текст сообщения, введенный пользователем в поле ввода сообщения, и должна отправить его на сервер и отобразить в чате. Пока что эта функция не реализована, вместо этого она просто очищает поле ввода сообщения.

def handle_send_message_button(self):
    message = self.chat_input.text()
    # здесь должна быть логика отправки сообщения на сервер и отображения его в чате
    self.chat_input.setText('')