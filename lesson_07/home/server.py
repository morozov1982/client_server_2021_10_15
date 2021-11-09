""" Программа-сервер """

import sys
import json
import argparse
import logging
import select
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CLIENTS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_decoded_message, send_message
import logs.server_log_config
from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def check_client_data(data, messages_list, client):
    """
    Обработчик сообщений от клиетов, принимает словарь - сообщение от клиента,
    проверяет корректность, возвращает словарь-ответ для клиента
    :param data:
    :param messages_list:
    :param client
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {data}')
    if ACTION in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in data and data[ACTION] == MESSAGE and \
            TIME in data and MESSAGE_TEXT in data:
        messages_list.append((data[ACCOUNT_NAME], data[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,  # внёс правки
            ERROR: 'Bad Request'
        })
        return


@log
def args_parser():
    """
    Парсер аргументов командной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    сначала обрабатываем порт: server.py -a 127.0.0.1 -p 6789
    :return:
    """
    listen_address, listen_port = args_parser()

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((listen_address, listen_port))
    server_socket.settimeout(0.5)

    clients = []
    messages = []

    server_socket.listen(MAX_CLIENTS)

    while True:
        try:
            client, client_address = server_socket.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        recv_data_list = []
        send_data_list = []
        error_list = []

        try:
            if clients:
                recv_data_list, send_data_list, error_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    check_client_data(get_decoded_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
