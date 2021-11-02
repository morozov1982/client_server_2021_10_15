""" Форматирование """

import sys
import logging

WORD = 'CRITICAL'
len(WORD)

print('{:9} #text'.format(WORD))
print(f'{WORD:11} #text')

LOG = logging.getLogger('my_logger')
STREAM_HANDLER = logging.StreamHandler(sys.stdout)

FORMAT_3 = '%(levelname)-13s #text'
FORMATTER = logging.Formatter(FORMAT_3)
STREAM_HANDLER.setFormatter(FORMATTER)

LOG.addHandler(STREAM_HANDLER)
LOG.setLevel(logging.CRITICAL)

LOG.critical('Критическое сообщение')
