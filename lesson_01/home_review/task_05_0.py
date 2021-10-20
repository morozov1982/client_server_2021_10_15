"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.
"""

import subprocess
from chardet import detect

ARGS = [['ping', '-c', '5', 'yandex.ru'], ['ping', '-c', '5', 'youtube.com']]

for arg in ARGS:
    PING = subprocess.Popen(arg, stdout=subprocess.PIPE)
    for line in PING.stdout:
        result = detect(line)
        print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
