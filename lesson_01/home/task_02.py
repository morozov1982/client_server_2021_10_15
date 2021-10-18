"""
2. Каждое из слов «class», «function», «method»
записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

first_bytes = b'class'
second_bytes = b'function'
third_bytes = b'method'

all_bytes = (first_bytes, second_bytes, third_bytes)

print('*' * 70)

for item in all_bytes:
    print(f'{item=} || тип: {type(item)} || длина: {len(item)} символов')

print('*' * 70)
