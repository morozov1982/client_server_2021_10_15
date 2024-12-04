"""Модуль modules"""

import subprocess
import chardet   # необходима предварительная инсталляция!

ARGS = ['ping', 'yandex.ru']
YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)

# for line in YA_PING.stdout:
#     print(line)

for line in YA_PING.stdout:
    result = chardet.detect(line)  # позволяет определить кодировку байт
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
