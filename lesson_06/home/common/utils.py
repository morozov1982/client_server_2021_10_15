""" Утилиты """

import json
from common.variables import MAX_PACKAGE_BYTES, DEFAULT_ENCODING

from decos import log


@log
def get_decoded_message(data):
    """
    Утилита приёма и декодирования сообщения
    Принимает байты, выдаёт словарь,
    если принято что-то другое возвращает ошибку значения
    :param data:
    :return:
    """

    encoded_data = data.recv(MAX_PACKAGE_BYTES)

    if isinstance(encoded_data, bytes):
        json_data = encoded_data.decode(DEFAULT_ENCODING)
        response = json.loads(json_data)

        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def send_message(socket, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param socket:
    :param message:
    :return:
    """

    json_message = json.dumps(message)
    encoded_message = json_message.encode(DEFAULT_ENCODING)
    socket.send(encoded_message)
