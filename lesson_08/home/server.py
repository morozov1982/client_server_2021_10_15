""" Программа-сервер """

import sys
import argparse
import logging
import select
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, ACCOUNT_NAME, MAX_CLIENTS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, \
    RESPONSE_400, DESTINATION, RESPONSE_200, EXIT  # добавил
from common.utils import get_decoded_message, send_message
import logs.server_log_config
from decos import log

SERVER_LOGGER = logging.getLogger('server')  # LOGGER


@log
def check_client_data(data, messages_list, client, clients, names):  # process_client_message
    """
    Обработчик сообщений от клиетов, принимает словарь - сообщение от клиента,
    проверяет корректность, возвращает словарь-ответ для клиента
    :param data:
    :param messages_list:
    :param client
    :param clients
    :param names
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {data}')  # data == message
    if ACTION in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data:  # and data[USER][ACCOUNT_NAME] == 'Guest':
        if data[USER][ACCOUNT_NAME] not in names.keys():
            names[data[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Это имя уже занято!'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in data and data[ACTION] == MESSAGE and \
            DESTINATION in data and TIME in data \
            and SENDER in data and MESSAGE_TEXT in data:
        messages_list.append(data)
        return
    elif ACTION in data and data[ACTION] == EXIT and ACCOUNT_NAME in data:
        client.remove(names[data[ACCOUNT_NAME]])
        names[data[ACCOUNT_NAME]].close()
        del names[data[ACCOUNT_NAME]]
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'Некорректный запрос!'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_sockets):  # поменял только имя последнего параметра
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_sockets:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_sockets:
        send_message(names[message[DESTINATION]], message)
        # немного поменял
        SERVER_LOGGER.info(f'Пользователю {message[DESTINATION]} отправлено сообщение от {message[SENDER]}')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_sockets:
        raise ConnectionError
    else:
        # немного поменял
        SERVER_LOGGER.error(f'Отправка сообщения невозможна!'
                            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере.')


@log
def args_parser():  # копипаста с мелкими изменениями
    """ Парсер аргументов командной строки """
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

    server_socket = socket(AF_INET, SOCK_STREAM)  # transport
    server_socket.bind((listen_address, listen_port))
    server_socket.settimeout(0.5)

    clients = []
    messages = []
    names = dict()  # добавлено

    server_socket.listen(MAX_CLIENTS)

    while True:
        try:
            client, client_address = server_socket.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        # немного изменеил имена
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
                    check_client_data(get_decoded_message(client_with_message),
                                      messages, client_with_message, clients, names)
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data_list)
            except Exception:
                SERVER_LOGGER.info(f'Связь с {i[DESTINATION]} была потеряна')  # немного поменял
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
