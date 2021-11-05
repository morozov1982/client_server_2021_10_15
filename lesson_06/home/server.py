""" Программа-сервер """

import sys
import json
import argparse
import logging
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CLIENTS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE
from common.utils import get_decoded_message, send_message
from errors import IncorrectDataReceivedError
import logs.server_log_config

from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def check_client_data(data):
    """
    Обработчик сообщений от клиетов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param data:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {data}')
    if ACTION in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,  # внёс правки
        ERROR: 'Bad Request'
    }


@log
def args_parser():
    """
    Парсер аргументов командной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    """
    Загрузка параметров командной строки, если нет параметров,
    то задаём значения по умолчанию.
    сначала обрабатываем порт:
    server.py -a 127.0.0.1 -p 6789
    :return:
    """
    parser = args_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a  # тоже переименовал, логичнее, чем listen_ip
    listen_port = namespace.p

    # проверяем номер порта
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((listen_address, listen_port))
    server_socket.listen(MAX_CLIENTS)

    while True:
        client, client_address = server_socket.accept()
        SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}')
        try:
            client_data = get_decoded_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {client_data}')
            response = check_client_data(client_data)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataReceivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
