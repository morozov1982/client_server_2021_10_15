""" Кофнфиг серверного логгера """

import sys
import os
import logging
import logging.handlers
from common.variables import LOGGING_LEVEL
sys.path.append('../')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'data', 'server.log')

# <дата-время> <уровеньважности> <имямодуля> <сообщение>
SERVER_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)-9s - %(filename)s - %(message)s')

# по заданию: "Журналирование должно производиться в лог-файл"
# поэтому закомментил
# STREAM_HANDLER = logging.StreamHandler(sys.stderr)
# STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
# STREAM_HANDLER.setLevel(logging.ERROR)

# На стороне сервера настроить ежедневную ротацию лог-файлов
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='D')
FILE_HANDLER.setFormatter(SERVER_FORMATTER)

LOGGER = logging.getLogger('server')
# LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')
    LOGGER.info('Отладочная информация')
    LOGGER.debug('Информационное сообщение')
