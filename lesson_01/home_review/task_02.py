"""
2. Каждое из слов «class», «function», «method»
записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

BYTES_1 = b'class'
BYTES_2 = b'function'
BYTES_3 = b'method'

ALL_BYTES = (BYTES_1, BYTES_2, BYTES_3)

print('*' * 70)

for item in ALL_BYTES:
    print(f'{item=} || тип: {type(item)} || длина: {len(item)} символов')

print('*' * 70)
