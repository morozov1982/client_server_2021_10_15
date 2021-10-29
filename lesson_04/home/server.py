""" Программа-сервер """

import sys
import json
from socket import socket, AF_INET, SOCK_STREAM

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CLIENTS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE
from common.utils import get_decoded_message, send_message


def check_client_data(data):
    """
    Обработчик сообщений от клиетов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента
    :param data:
    :return:
    """

    if ACTION in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,  # внёс правки
        ERROR: 'Bad Request'
    }


def main():
    """
    Загрузка параметров командной строки, если нет параметров,
    то задаём значения по умолчанию.
    сначала обрабатываем порт:
    server.py -a 127.0.0.1 -p 6789
    :return:
    """

    try:
        if '-a' in sys.argv:
            listen_ip = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_ip = ''
    except IndexError:
        print('Укажите после параметра "-a" адрес, который будет слушать сервер!')
        sys.exit(1)

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT

        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('Укажите после параметра "-p" номер порта!')
        sys.exit(1)
    except ValueError:
        print('В качастве порта может быть указано только число, в диапазоне от 1024 до 65535.')
        sys.exit(1)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((listen_ip, listen_port))
    server_socket.listen(MAX_CLIENTS)

    while True:
        client, client_addr = server_socket.accept()
        try:
            client_data = get_decoded_message(client)
            print(client_data)
            response = check_client_data(client_data)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
