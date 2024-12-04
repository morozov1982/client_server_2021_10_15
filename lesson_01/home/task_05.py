"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.
"""

import subprocess
import chardet

ARGS_YA = ['ping', 'yandex.ru']
ARGS_YT = ['ping', 'youtube.com']

YA_PING = subprocess.Popen(ARGS_YA, stdout=subprocess.PIPE)
YT_PING = subprocess.Popen(ARGS_YT, stdout=subprocess.PIPE)

print(f'{"*" * 50}\n\tutf-8\n{"*" * 50}')

# ну это-то мы в классе сделали ;-)
for line in YA_PING.stdout:
    line_info = chardet.detect(line)
    line = line.decode(line_info['encoding']).encode('utf-8')
    print(line.decode('utf-8'))

print(f'{"*" * 50}\n\twindows-1251\n{"*" * 50}')

# тут немного поэкспериментировал
for line in YT_PING.stdout:
    line_info = chardet.detect(line)
    line = line.decode(line_info['encoding']).encode('cp1251')  # попробовал как вариант, тоже работает
    # print(line)  # ну а что не посмотреть-то ;-)
    # line = line.decode(line_info['encoding']).encode('utf-8')
    print(line.decode('cp1251'))  # естественно здесь соответствующая кодировка
    # print(line.decode('utf-8'))
