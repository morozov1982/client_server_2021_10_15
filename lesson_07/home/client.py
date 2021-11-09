""" Программа-клиент """

import sys
import json
import argparse
import logging
from time import time
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT
from common.utils import get_decoded_message, send_message
from errors import ReqFieldMissingError
import logs.client_log_config

from decos import log

CLIENT_LOGGER = logging.getLogger('client')


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
    Функция разбирает ответ сервера
    :param data:
    :return:
    """
    CLIENT_LOGGER.debug(f'Разбор ответа от сервера: {data}')
    if RESPONSE in data:
        if data[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {data[ERROR]}'
    raise ValueError


@log
def args_parser():
    """
    Создаёт парсер аргументов командной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    """Загружаем параметры коммандной строки"""
    parser = args_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr  # решиил всё-таки переименовать, логичнее, чем server_ip
    server_port = namespace.port

    # проверяем номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address} , порт: {server_port}')

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        client_message = request_user(port=server_port)
        send_message(client_socket, client_message)
        response = get_server_response(get_decoded_message(client_socket))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {response}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as err:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{err.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
