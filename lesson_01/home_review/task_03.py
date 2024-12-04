"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

VAR_1 = 'attribute'
VAR_2 = 'класс'
VAR_3 = 'функция'
VAR_4 = 'type'

WORDS = (VAR_1, VAR_2, VAR_3, VAR_4)

# вариант 1
for word in WORDS:
    try:
        bytes(word, 'ascii')
    except UnicodeEncodeError:
        print(f'Слово "{word}" невозможно записать в виде байтовой строки')


# вариант 2
for word in WORDS:
    try:
        word.encode('ascii')
    except UnicodeEncodeError:
        print(f'Слово "{word}" невозможно записать в виде байтовой строки')


# вариант 3
for word in WORDS:
    try:
        expr_obj = f"b'{word}'"
        eval(expr_obj)  # eval('1 + 2') вернёт 3
    except SyntaxError:
        print(f'Слово "{word}" невозможно записать в виде байтовой строки')


# вариант 4
for word in WORDS:
    for char in word:
        if ord(char) > 127:
            print(f'Слово "{word}" невозможно записать в виде байтовой строки')
            break
