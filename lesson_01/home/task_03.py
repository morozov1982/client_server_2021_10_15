"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

first_bytes = b'attribute'  # можно - латиница
# second_bytes = b'класс'   # нельзя - кириллица (не ASCII)
# third_bytes = b'функция'  # нельзя - кириллица (не ASCII)
forth_bytes = b'type'       # можно - латиница


# как вариант
words = ('attribute', 'класс', 'функция', 'type')

for word in words:
    if word.isascii():
        print(word.encode('utf-8'))
    else:
        print(f'{word} - невозможно записать в байтовом типе')
