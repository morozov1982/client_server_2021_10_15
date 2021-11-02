"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import logging

LOG = logging.getLogger('app.main')

FILE_HANDLER = logging.FileHandler("app.log", encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

FILE_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

LOG.info('Информационное сообщение')
