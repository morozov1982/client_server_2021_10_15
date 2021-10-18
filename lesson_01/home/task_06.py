"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

import locale
import chardet

lines = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as file:  # намеренно не указал encoding='utf-8', чтобы задание вообще имело смысл ;-)
    for line in lines:
        file.write(line)
        file.write('\n')

print(f'Кодировка по умолчанию: {locale.getpreferredencoding()}\n')

# with open('test_file.txt', 'r', encoding='utf-8') as file:  # естественно вернёт ошибку
with open('test_file.txt', 'rb') as file:
    forced_encoding = 'utf-8'
    file_encoding = chardet.detect(file.read())['encoding']
    file.seek(0)  # ;-)

    for line in file:
        print_line = line.decode(file_encoding).encode(forced_encoding).decode(forced_encoding)
        print(print_line, end='')

