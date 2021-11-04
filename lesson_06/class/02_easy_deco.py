""" Простейший декоратор-функция """

import time
import requests


def decorator(func):
    """ Сам декоратор """
    def wrapper():
        """ Обёртка """
        start = time.time()
        func()
        end = time.time()
        print(f'Время выполнения исходной функции: {round(end-start, 2)} секунд')
    return wrapper


@decorator
def get_wp():
    """ Получаем от сервера 200 - запрос успешно обработан """
    print('Выполняем расчёт')
    res = requests.get('https://google.com')
    return res


print(get_wp())
