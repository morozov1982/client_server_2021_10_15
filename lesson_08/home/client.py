""" Программа-клиент """

import sys
import json
import argparse
import logging
import threading
from time import time, sleep
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, \
    DESTINATION, EXIT
from common.utils import get_decoded_message, send_message
from errors import IncorrectDataReceivedError, ReqFieldMissingError, ServerError
import logs.client_log_config

from decos import log

CLIENT_LOGGER = logging.getLogger('client')  # другое имя


@log
def create_exit_message(account_name):  # копипаста с мелкими изменениями
    """ Функция создаёт словарь с сообщением о выходе """
    return {
        ACTION: EXIT,
        TIME: time(),
        ACCOUNT_NAME: account_name
    }


@log
def message_from_server(sock, username):  # my_username
    """ Функция - обработчик сообщений других пользователей, поступающих с сервера """
    while True:
        try:
            message = get_decoded_message(sock)  # get_message
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == username:
                print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                                   f'\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')
        except IncorrectDataReceivedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение!')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Соединение с сервером разорвано!')
            break


@log
def create_message(sock, account_name='Guest'):
    """
    Функция запрашивает кому отправить сообщение и само сообщение,
    а также отправляет полученные данные на сервер
    :param sock:
    :param account_name:
    :return:
    """
    to_user = input('Введите имя получателя: ')
    message = input('Введите сообщение для отправки: ')

    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time(),
        MESSAGE_TEXT: message
    }

    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        CLIENT_LOGGER.critical('Соединение с сервером разорвано!')
        sys.exit(1)


# переместил сюда, мне так удобней
def print_help():
    """ Функция выводит справку по использованию """
    print('Поддерживаемые команды:')
    print('message - отправить сообщение (кому и текст будет запрошены отдельно).')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def user_interactive(sock, username):
    """
    Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения
    :param sock:
    :param username:
    :return:
    """
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            sleep(0.5)
            break
        else:
            print('Команда не распознана, попробуйте снова.\nhelp - вывести поддерживаемые команды.')


@log
def request_user(user_name):  # create_presence, убрал порт за ненадобностью
    """
    Функция генерирует запрос о присутствии клиента
    :param user_name:
    :return:
    """

    request = {
        ACTION: PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: user_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформированно {PRESENCE} сообщение для пользователя {user_name}')
    return request


@log
def get_server_response(data):  # process_response_ans, ничего не поменялось
    """
    Функция разбирает ответ сервера на сообщение о присутствии, возращает 200, если все ОК,
    или генерирует исключение при ошибке
    :param data:
    :return:
    """
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {data}')
    if RESPONSE in data:
        if data[RESPONSE] == 200:
            return '200 : OK'
        elif data[RESPONSE] == 400:
            raise ServerError(f'400 : {data[ERROR]}')
    raise ReqFieldMissingError


@log
def args_parser():
    """ Парсер аргументов коммандной строки """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name


def main():
    """ Загружаем параметры коммандной строки """
    server_address, server_port, client_name = args_parser()

    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_name}')

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
                       f'порт: {server_port}, имя пользователя: {client_name}')

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)  # transport
        client_socket.connect((server_address, server_port))
        send_message(client_socket, request_user(client_name))
        response = get_server_response(get_decoded_message(client_socket))  # answer
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ от сервера {response}')
        print('Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as err:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {err.text}')
        sys.exit(1)
    except ReqFieldMissingError as err:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {err.missing_field}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_from_server, args=(client_socket, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(client_socket, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
