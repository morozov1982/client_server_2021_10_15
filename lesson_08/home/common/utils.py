""" Утилиты """

import sys
import json

from common.variables import MAX_PACKAGE_BYTES, DEFAULT_ENCODING
from errors import IncorrectDataReceivedError, NonDictInputError
from decos import log
sys.path.append('../')  # всё-таки скопировал


@log
def get_decoded_message(data):  # get_message(client)
    """
    Утилита приёма и декодирования сообщения: принимает байты, выдаёт словарь,
    если принято что-то другое возвращает ошибку значения
    :param data:
    :return:
    """
    encoded_data = data.recv(MAX_PACKAGE_BYTES)  # encoded_response

    if isinstance(encoded_data, bytes):
        json_data = encoded_data.decode(DEFAULT_ENCODING)  # json_response
        response = json.loads(json_data)

        if isinstance(response, dict):
            return response
        raise IncorrectDataReceivedError
    raise IncorrectDataReceivedError


@log
def send_message(socket, message):  # как в оригинале
    """
    Утилита кодирования и отправки сообщения: принимает словарь и отправляет его
    :param socket:
    :param message:
    :return:
    """
    if not isinstance(message, dict):
        raise NonDictInputError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(DEFAULT_ENCODING)
    socket.send(encoded_message)
