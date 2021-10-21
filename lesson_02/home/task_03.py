"""
3. Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
    a. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
       второму — целое число, третьему — вложенный словарь,
       где значение каждого ключа — это целое число с юникод-символом,
       отсутствующим в кодировке ASCII (например, €);
    b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
       При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
       а также установить возможность работы с юникодом: allow_unicode = True;
    c. Реализовать считывание данных из созданного файла
       и проверить, совпадают ли они с исходными.
"""
from pprint import pprint

import yaml
import os


DATA_DIR_NAME = 'data'
OUTPUT_FILE_NAME = 'file.yaml'
OUTPUT_FILE_PATH = os.path.join(DATA_DIR_NAME, OUTPUT_FILE_NAME)


FIRST_LIST = ['Beaver', 'Hamster', 'Handcar', 'Hydrogen peroxide', 'Perm']
SECOND_NUMBER = 5
THIRD_DICT = {'Beaver': '1. Бобёр', 'Hamster': '2. Хомяк', 'Handcar': '3. Дрезина',
              'Hydrogen peroxide': '4. Перекись водорода', 'Perm': '5. Химическая завивка'}
DATA_TO_YAML = {'funny_words': FIRST_LIST, 'number': SECOND_NUMBER, 'translation': THIRD_DICT}


# c
def check_data(data_1, data_2):
    return data_1 == data_2


def write_to_yaml(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def read_from_yaml(file_name):
    with open(file_name, encoding='utf-8') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
        return content


write_to_yaml(OUTPUT_FILE_PATH, DATA_TO_YAML)

yaml_data = read_from_yaml(OUTPUT_FILE_PATH)
pprint(yaml_data)
print('=' * 55)

is_equal = check_data(DATA_TO_YAML, yaml_data)
print(f'Данные совпадают: {is_equal}')
