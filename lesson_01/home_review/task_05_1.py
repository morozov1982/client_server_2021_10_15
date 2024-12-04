"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.
"""

import subprocess
import chardet

# решение Никиты Черенкова

ping_ya = subprocess.Popen(('ping', 'ya.ru'), stdout=subprocess.PIPE, encoding='utf-8')

for i, line in enumerate(ping_ya.stdout):
    ping_ya.kill() if i == 5 else print(line)


# решение Сергея Аверченкова

def ping_service(service):
    args = ['ping', service]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    count = 0

    for line in ping.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))

        if count == 4:
            break
        count += 1


ping_service('yandex.ru')
ping_service('youtube.com')
