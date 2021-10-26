""" Программа-клиент """

import sys
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT
from common.utils import get_decoded_message, send_message


def request_user(port=DEFAULT_PORT, user_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
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
    return request


def get_server_response(data):
    """
    Функция разбирает ответ сервера
    :param data:
    :return:
    """

    if RESPONSE in data:
        if data[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {data[ERROR]}'
    raise ValueError


def main():
    """Загружаем параметры коммандной строки"""
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_ip = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число, в диапазоне от 1024 до 65535.')
        print(f'{sys.argv[1]=} {sys.argv[2]}')
        sys.exit(1)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_message = request_user(port=server_port)
    send_message(client_socket, client_message)

    try:
        response = get_server_response(get_decoded_message(client_socket))
        print(response)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
