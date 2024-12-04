"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

from chardet import detect

LINES_LIST = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as file:
    for line in LINES_LIST:
        file.write(f'{line}\n')
# file.close()  # зачем?


with open('test_file.txt', 'rb') as file:
    CONTENT = file.read()
ENCODING = detect(CONTENT)['encoding']
print(ENCODING)

with open('test_file.txt', 'r', encoding=ENCODING) as file:
    CONTENT = file.read()

print(CONTENT)
