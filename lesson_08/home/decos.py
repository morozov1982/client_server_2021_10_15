""" Декораторы """

import logging
import sys
import os.path
import traceback
import inspect

import logs.server_log_config
import logs.client_log_config

# if sys.argv[0].find('server') == -1:  # в моём случае не сработает, так как в пути есть папка client_server
# if os.path.basename(sys.argv[0]).find('server') == -1:  # так работает корректно
# if os.path.basename(sys.argv[0]) == 'server.py':  # ну или ...
if sys.argv[0].find('server.py') == -1:  # или так, оставлю пока этот вариант
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func):  # log(func_to_log):
    """ Функция-декоратор для логирования """
    def log_wrapper(*args, **kwargs):  # log_saver
        res = func(*args, **kwargs)
        LOGGER.debug(f'Вызвана функция: {func.__name__}, с параметрами: {args}, {kwargs}. '
                     f'Из модуля: {func.__module__}.'
                     f'Вызов из функции: {traceback.format_stack()[0].strip().split()[-1]}. '  # копипаста, не стал убирать
                     f'Вызов из функции: {inspect.stack()[1][3]}.')                            # тоже, не стал убирать
        return res
    return log_wrapper
