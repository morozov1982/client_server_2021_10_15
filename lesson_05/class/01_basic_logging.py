"""
Журналирование (логгирование) с использованием модуля logging.
Базовая настройка (не подходит для нашего проекта)
"""

import logging


logging.basicConfig(
    filename="app_01.log",
    # %(levelname)s - уровень важности
    # %(asctime)s - дата попадания записи в журнал
    # %(message)s - текст сообщения
    format="%(levelname)s %(asctime)s %(message)s",
    # level=logging.DEBUG
    level=logging.INFO
)

LOG = logging.getLogger('app.basic')

LOG.debug('Отладочная информация')
LOG.info('Информационное сообщение')
LOG.warning('Предупреждение')
LOG.critical('Критическое сообщение')
