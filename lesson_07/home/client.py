""" Программа-клиент """

import sys
import json
import argparse
import logging
from time import time
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_decoded_message, send_message
from errors import ReqFieldMissingError, ServerError
import logs.client_log_config

from decos import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """ Функция - обработчик сообщений других пользователей, поступающих с сервера """
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """
    Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или "!!!" для завершения работы\n>>> ')

    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)

    message_dict = {
        ACTION: MESSAGE,
        TIME: time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }

    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def request_user(port=DEFAULT_PORT, user_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param port:
    :param user_name:
    :return:
    """

    request = {
        ACTION: PRESENCE,
        TIME: time(),
        PORT: port,
        USER: {
            ACCOUNT_NAME: user_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформированно {PRESENCE} сообщение для пользователя {user_name}')
    return request


@log
def get_server_response(data):
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
    """
    Создаёт парсер аргументов командной строки и читает параметры, возвращает 3 параметра
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: "listen" и "send"')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    """Загружаем параметры коммандной строки"""
    server_address, server_port, client_mode = args_parser()

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
                       f'порт: {server_port}, режим работы: {client_mode}')

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        send_message(client_socket, request_user())
        response = get_server_response(get_decoded_message(client_socket))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ от сервера {response}')
        print('Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as err:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {err.text}')
        sys.exit(1)
    except ReqFieldMissingError as err:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{err.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        while True:
            if client_mode == 'send':
                print('Режим работы - отправка сообщений.')

                try:
                    send_message(client_socket, create_message(client_socket))
                except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                print('Режим работы - приём сообщений.')

                try:
                    message_from_server(get_decoded_message(client_socket))
                except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
