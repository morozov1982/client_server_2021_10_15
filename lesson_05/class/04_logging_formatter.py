"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import sys
import logging

APP_LOG = logging.getLogger('app')
APP_LOG.setLevel(logging.INFO)

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.INFO)

FILE_HANDLER = logging.FileHandler('app_4.log', encoding='utf-8')
FILE_HANDLER.setLevel(logging.ERROR)

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

APP_LOG.addHandler(STREAM_HANDLER)
APP_LOG.addHandler(FILE_HANDLER)
APP_LOG.setLevel(logging.DEBUG)

APP_LOG.debug('Отладочная информация')
APP_LOG.info('Информационное сообщение')
APP_LOG.warning('Предупреждение')
APP_LOG.error('Ошибка')
APP_LOG.critical('Критическое сообщение')
