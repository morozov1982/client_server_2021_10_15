""" Простейший декоратор-функция """

import time
from functools import wraps


def decorator(func):
    """ Сам декоратор """
    @wraps(func)
    def wrapper():
        """ Обёртка """
        print('Выполняется функция-обёртка')
        time.sleep(2)
        print(f'Просто ссылка на экземпляр оборачиваемой функции: {func}')
        time.sleep(2)
        print('Запускаем оборачиваемую (исходную) функцию ...')
        time.sleep(2)
        f = func
        time.sleep(2)
        print('Выходим из обёртки')
        return f

    return wrapper


@decorator
def some_text():
    """ Какая-то логика """
    print('Вычисления')


# some_text()

# some_text = decorator(some_text)
# some_text()

# ========================================
# получаем имя функции
# print(type(some_text), some_text.__name__)
# print(type(some_text), some_text.__doc__)

# ========================================
# как получить результат функции (добавить return, см. выше)
print(some_text())
