"""Модуль json_read"""

import json

print('----- использование метода load для чтения json-файла, как объекта -----')
print('----- преобразуем json-объект в python-объект (словарь) -----')
with open('mes_example_read.json', encoding='utf-8') as f_n:
    print(type(f_n))
    OBJ = json.load(f_n)
    print(type(OBJ))
    print(OBJ)

print(f'==> {type(f_n)} ==> json.load() ==> {type(OBJ)} ==>')

for section, commands in OBJ.items():
    print(f'{section}, {commands}')


print('----- использование метода loads для чтения json-файла, как строки -----')
print('----- преобразуем json-строку в python-объект (словарь) -----')
with open('mes_example_read.json', encoding='utf-8') as f_n:
    F_N_CONTENT = f_n.read()
    print(F_N_CONTENT)
    print(type(F_N_CONTENT))
    OBJ = json.loads(F_N_CONTENT)
    print(type(OBJ))

print(f'==> {type(f_n)} ==> {type(F_N_CONTENT)} ==> json.loads() ==> {type(OBJ)} ==>')

for section, commands in OBJ.items():
    print(f'{section}, {commands}')
