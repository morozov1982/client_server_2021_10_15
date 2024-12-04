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


# перезапись файла в нужной кодировке
def encoding_convert():
    with open('test_file.txt', 'rb') as file:
        content_bytes = file.read()

    detected = detect(content_bytes)
    encoding = detected['encoding']
    content_text = content_bytes.decode(encoding)

    with open('test_file.txt', 'w', encoding='utf-8') as file:
        file.write(content_text)


encoding_convert()

with open('test_file.txt', 'r', encoding='utf-8') as file:
    CONTENT = file.read()
print(CONTENT)
