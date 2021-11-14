""" Кофнфиг клиентского логгера """

import sys
import os
import logging

sys.path.append('../')
from common.variables import LOGGING_LEVEL

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'data', 'client.log')

# <дата-время> <уровеньважности> <имямодуля> <сообщение>
CLIENT_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)-9s - %(filename)s - %(message)s')

# раскомментил
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
FILE_HANDLER = logging.FileHandler(PATH, encoding='utf-8')  # LOG_FILE
FILE_HANDLER.setFormatter(CLIENT_FORMATTER)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')  # отменятина
    LOGGER.info('Отладочная информация')
    LOGGER.debug('Информационное сообщение')
