"""
Журналирование (логгирование) с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import sys
import logging

LOG = logging.getLogger('basic')

CRIT_HAND = logging.StreamHandler(sys.stderr)
CRIT_HAND.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(levelname)-10s %(asctime)s %(message)s")

CRIT_HAND.setFormatter(FORMATTER)

LOG.addHandler(CRIT_HAND)
LOG.setLevel(logging.DEBUG)

LOG.info('Информационное сообщение')
