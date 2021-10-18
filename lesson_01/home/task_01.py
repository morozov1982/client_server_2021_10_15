"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
"""

first_string = 'разработка'
second_string = 'сокет'
third_string = 'декоратор'

print('*' * 50)

print(f'{first_string=} || тип: {type(first_string)}')
print(f'{second_string=}     || тип: {type(second_string)}')
print(f'{third_string=}  || тип: {type(third_string)}')

print('*' * 50)

first_string = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
second_string = '\u0441\u043e\u043a\u0435\u0442'
third_string = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

print('*' * 50)

print(f'{first_string=} || тип: {type(first_string)}')
print(f'{second_string=}     || тип: {type(second_string)}')
print(f'{third_string=}  || тип: {type(third_string)}')

print('*' * 50)
