""" Константы """

import logging

DEFAULT_PORT = 6789
DEFAULT_IP_ADDRESS = '127.0.0.1'
MAX_CLIENTS = 5
MAX_PACKAGE_BYTES = 1024
DEFAULT_ENCODING = 'utf-8'
LOGGING_LEVEL = logging.DEBUG

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

RESPONDEFAULT_IP_ADDRESSSE = 'responsedefault_ip_addressse'

PORT = 'port'

# Словари - ответы (копипаста):
RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {RESPONSE: 400, ERROR: None}
