""" Простейшее логирование """

import logging

LOG = logging.getLogger('app.main')

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)-9s - %(message)s")

FILE_HANDLER = logging.FileHandler("app.main.log", encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setFormatter(FORMATTER)
    LOG.addHandler(STREAM_HANDLER)
    LOG.debug('Отладочное сообщение')
