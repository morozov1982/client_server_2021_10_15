"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import logging

LOG = logging.getLogger('app')

FILE_HANDLER = logging.FileHandler('app_5.log', encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

FILE_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

PARAMS = {'host': 'www.python.org', 'port': 80}
# LOG.info("Параметры подключения: %(host)s, %(port)d", PARAMS)
# можно использовать f-строки
LOG.info(f"Параметры подключения: {PARAMS['host']}, {PARAMS['port']}")
