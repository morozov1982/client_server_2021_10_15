"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
"""


# оптимизируем: избавляемся от повторов кода (от лишних print-ов), можно даже импортировать в других задачах
def print_value_and_type(items: tuple):  # преподаватель использовал list
    for item in items:
        print(f'{item=} || тип: {type(item)}')


# преподаватель настаивает на том, чтобы объявленные вначале переменные были константами
WORD_1 = 'разработка'
WORD_2 = 'сокет'
WORD_3 = 'декоратор'
WORD_TUPLE = (WORD_1, WORD_2, WORD_3)

print('*' * 50)

print_value_and_type(WORD_TUPLE)

print('*' * 50)

UNICODE_WORD_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
UNICODE_WORD_2 = '\u0441\u043e\u043a\u0435\u0442'
UNICODE_WORD_3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
UNICODE_WORD_TUPLE = (UNICODE_WORD_1, UNICODE_WORD_2, UNICODE_WORD_3)

print('*' * 50)

print_value_and_type(UNICODE_WORD_TUPLE)

print('*' * 50)
