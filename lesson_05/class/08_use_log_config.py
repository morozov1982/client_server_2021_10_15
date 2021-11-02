"""
Журналирование (логгирование) с использованием модуля logging
Вынесение настройки логгирования в отдельный модуль
"""

import logging
import l07_log_config

LOG = logging.getLogger('app.main')


def main():
    """ Тестовая главная функция """
    LOG.debug('Старт приложения')


if __name__ == '__main__':
    main()
